"""REST client handling, including SimplesatStream base class."""

from __future__ import annotations

import typing as t
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import parse_qsl

import requests
from requests import Response
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BaseHATEOASPaginator
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
_TToken = t.TypeVar("_TToken")


class SimplesatPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response: Response) -> str | None:
        data = response.json()
        return data.get("next")


class SimplesatStream(RESTStream):
    """Simplesat stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.simplesat.io/api/v1"

    next_page_token_jsonpath = "$.next"  # noqa: S105

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Simplesat-Token",
            value=self.config.get("auth_token", ""),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        return SimplesatPaginator()

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:  # sourcery skip: dict-assign-update-to-union
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if self.config.get("page_size", False):
            params["page_size"] = self.config["page_size"]
        if next_page_token:
            params.update(parse_qsl(next_page_token.query))
        return params

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: _TToken | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request"""
        if self.rest_method == "POST":
            fields = {}
            if self.config.get("start_date"):
                fields["start_date"] = self.config.get("start_date")
            return fields
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

