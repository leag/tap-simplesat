"""simplesat tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_simplesat import streams


class TapSimplesat(Tap):
    """simplesat tap class."""

    name = "tap-simplesat"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.SimplesatStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.AnswersStream(self),
            streams.QuestionsStream(self),
            streams.ResponsesStream(self),
            streams.SurveysStream(self),
        ]


if __name__ == "__main__":
    TapSimplesat.cli()
