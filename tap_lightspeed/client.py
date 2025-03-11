"""REST client handling, including LightspeedStream base class."""

from typing import Any, Dict, Iterable, Optional, Callable
from pytz import timezone
from datetime import datetime
import urllib3
import requests
from pendulum import parse
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.streams import RESTStream
from singer_sdk.exceptions import RetriableAPIError, FatalAPIError
import backoff
import copy
from time import sleep
from cached_property import cached_property
from tap_lightspeed.exceptions import TooManyRequestsError
from http.client import ImproperConnectionState, RemoteDisconnected
import singer
from singer import StateMessage


class LightspeedStream(RESTStream):
    """Lightspeed stream class."""

    @property
    def url_base(self):
        language = self.config.get("language")
        return f'{self.config.get("base_url")}/{language}'

    replication_filter_field = None
    end_date_param = "updated_at_max"
    limit = 250
    extra_retry_statuses = [429, 404] # there are temporary 404 for order endpoints

    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("api_key"),
            password=self.config.get("api_secret"),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        previous_token = previous_token or 1
        if len(list(self.parse_response(response))) == self.limit:
            next_page_token = previous_token + 1
            return next_page_token

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date
    
    @cached_property
    def end_date(self):
        end_date = self.config.get("end_date")
        if end_date is not None:
            try:
                end_date = parse(end_date)
                end_date = end_date.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except:
                self.logger.info(f"Failed while trying to parse end_date {end_date}, fetching data without end_date")
                end_date = None
        return end_date

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["limit"] = self.limit
        if next_page_token:
            params["page"] = next_page_token
        start_date = self.get_starting_time(context)
        if self.replication_key:
            if start_date and self.replication_filter_field:
                params[self.replication_filter_field] = start_date.astimezone(timezone('UTC')).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            if self.end_date:
                params[self.end_date_param] = self.end_date
        return params

    def clean_values(self, row, field_meta = None):
        for field, value in row.items():
            # clean false values from non boolean fields
            meta = (
                self.schema["properties"].get(field, {})
            )

            if isinstance(value, list):
                row[field] = [self.clean_values(val, meta) if isinstance(val, dict) else val for val in value]
            elif isinstance(value, dict):
                row[field] = self.clean_values(value, meta)
            else:
                if field_meta:
                    meta = field_meta.get("properties").get(field, {}) if field_meta.get("properties") else field_meta.get("items", dict()).get("properties", dict()).get(field, dict())

                field_type = meta.get("type", [""])[0]

                if isinstance(value, str) and field_type == "number":
                    row[field] = float(value) if value else None
                
                # Lightspeed API sometimes will return integer values as True or False.
                # Absent any documentation on why, the tap converts them to None
                if isinstance(value, bool) and field_type == "integer":
                    row[field] = None

                # Lightspeed sometimes returns nullish values as empty strings
                if value == "" and field_type in ["integer", "number"]:
                    row[field] = None

                if field_type != "boolean" and value == False:
                    row[field] = None
        return row

    def post_process(self, row, context):
        row = self.clean_values(row)
        return row

    def request_decorator(self, func: Callable) -> Callable:
        decorator: Callable = backoff.on_exception(
            backoff.expo,
            (
                RetriableAPIError,
                TooManyRequestsError,
                ImproperConnectionState,
                ConnectionError,
                RemoteDisconnected,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
                urllib3.exceptions.HTTPError,
                TimeoutError
            ),
            max_tries=10,
            factor=3,
        )(func)
        return decorator
    
    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        next_page_token: Any = None
        finished = False
        decorated_request = self.request_decorator(self._request)
        throttle_seconds = self.config.get("throttle_seconds", 1.3)
        try:
            throttle_seconds = float(throttle_seconds)
        except:
            self.logger.info(f"Not able to convert {throttle_seconds} to a float, using throttle default value 1.3 seconds")
            throttle_seconds = 1.3

        while not finished:
            prepared_request = self.prepare_request(
                context, next_page_token=next_page_token
            )
            # Wait between requests to avoid hitting 429
            self.logger.info(f"Waiting between requests to avoid rate limits for {throttle_seconds} seconds")
            sleep(throttle_seconds)

            resp = decorated_request(prepared_request, context)
            yield from self.parse_response(resp)
            previous_token = copy.deepcopy(next_page_token)
            next_page_token = self.get_next_page_token(
                response=resp, previous_token=previous_token
            )
            if next_page_token and next_page_token == previous_token:
                raise RuntimeError(
                    f"Loop detected in pagination. "
                    f"Pagination token {next_page_token} is identical to prior token."
                )
            # Cycle until get_next_page_token() no longer returns a value
            finished = not next_page_token

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")  
            self.logger.info(f"Hit 429. Retry-After: {retry_after}")

            try:
                retry_time = parse(retry_after)
                retry_after = (retry_time - datetime.now(timezone("UTC"))).total_seconds()
                retry_after = max(1, int(retry_after))  
            except Exception:
                retry_after = 60  # Fallback in case of parsing errors

            msg = self.response_error_message(response)
            self.logger.info(f"Response status code 429 too many requests, sleeping for {retry_after} seconds...")
            sleep(retry_after)
            self.logger.info("Trying request again...")
            raise TooManyRequestsError(msg, response)

        if response.status_code in self.extra_retry_statuses or 500 <= response.status_code < 600:
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)
        elif 400 <= response.status_code < 500:
            msg = self.response_error_message(response)
            raise FatalAPIError(msg)

    def _write_state_message(self) -> None:
        """Write out a STATE message with the latest state."""
        tap_state = self.tap_state

        if tap_state and tap_state.get("bookmarks"):
            for stream_name in tap_state.get("bookmarks").keys():
                if tap_state["bookmarks"][stream_name].get("partitions"):
                    tap_state["bookmarks"][stream_name] = {"partitions": []}

        singer.write_message(StateMessage(value=tap_state))
        
    def get_replication_key_signpost(self, context: Optional[dict]) -> Optional[Any]:
        return None
