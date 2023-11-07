"""Tests standard tap features using the built-in SDK tests library."""

from os import environ

from singer_sdk.testing import get_tap_test_class

from tap_simplesat.tap import TapSimplesat

SAMPLE_CONFIG = {
    "auth_token": environ.get("SIMPLESAT_API_KEY"),
}


# Run standard built-in tap tests from the SDK:
TestTapsimplesat = get_tap_test_class(
    tap_class=TapSimplesat,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
