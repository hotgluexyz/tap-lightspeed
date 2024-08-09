"""REST client handling, including LightspeedStream base class."""

from typing import Any, Dict, Optional

import requests
from pendulum import parse
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.streams import RESTStream


class LightspeedStream(RESTStream):
    """Lightspeed stream class."""

    @property
    def url_base(self):
        language = self.config.get("language")
        return f'{self.config.get("base_url")}/{language}'

    replication_filter_field = None
    limit = 250

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
        if len(list(self.parse_response(response))) > self.limit:
            next_page_token = previous_token + 1
            return next_page_token

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["limit"] = self.limit
        if next_page_token:
            params["page"] = next_page_token
        start_date = self.get_starting_time(context)
        if start_date and self.replication_key and self.replication_filter_field:
            params[self.replication_filter_field] = start_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return params

    def clean_false_values(self, row):
        for field, value in row.items():
            if isinstance(value, list):
                row[field] = [self.clean_false_values(val) if isinstance(val, dict) else val for val in value]
            elif isinstance(value, dict):
                row[field] = self.clean_false_values(value)
            else:
                # clean false values from non boolean fields
                field_type = (
                    self.schema["properties"].get(field, {}).get("type", [""])[0]
                )
                if field_type != "boolean" and value == False:
                    row[field] = None
        return row

    def post_process(self, row, context):
        row = self.clean_false_values(row)
        return row
