"""Lightspeed tap class."""

import inspect
from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_lightspeed import streams


class TapLightspeed(Tap):
    """Lightspeed tap class."""

    name = "tap-lightspeed"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "base_url",
            th.StringType,
            required=True,
        ),
        th.Property(
            "language",
            th.StringType,
            required=True,
        ),
        th.Property("api_key", th.StringType, required=True),
        th.Property("api_secret", th.StringType, required=True),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [
            cls(self)
            for _, cls in inspect.getmembers(streams, inspect.isclass)
            if cls.__module__ == "tap_lightspeed.streams"
        ]


if __name__ == "__main__":
    TapLightspeed.cli()
