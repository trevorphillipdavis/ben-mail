"""Read-only Nylas client boundary."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .config import NylasConfig
from .models import EmailAddress, EmailMessageSummary


@dataclass(frozen=True)
class RecentMessagesRequest:
    limit: int = 10

    def __post_init__(self) -> None:
        if self.limit < 1 or self.limit > 50:
            raise ValueError("limit must be between 1 and 50")


class NylasError(Exception):
    """Base error for Nylas provider failures."""


class NylasConfigurationError(NylasError):
    """Raised when local configuration is missing or invalid."""


class NylasApiError(NylasError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


class NylasNetworkError(NylasError):
    """Raised when Nylas cannot be reached."""


class HttpTransport(Protocol):
    def get_json(self, url: str, headers: dict[str, str]) -> dict[str, Any]:
        ...


class UrlLibHttpTransport:
    def get_json(self, url: str, headers: dict[str, str]) -> dict[str, Any]:
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
            return json.loads(body)
        except HTTPError as error:
            raise NylasApiError(error.code, _http_error_message(error)) from error
        except URLError as error:
            raise NylasNetworkError(f"Could not reach Nylas: {error.reason}") from error
        except TimeoutError as error:
            raise NylasNetworkError("Timed out while contacting Nylas.") from error


class NylasEmailClient:
    def __init__(self, config: NylasConfig, transport: HttpTransport | None = None) -> None:
        self._config = config
        self._transport = transport or UrlLibHttpTransport()

    @property
    def is_configured(self) -> bool:
        return not self._config.missing_required_values()

    def list_recent_messages(self, request: RecentMessagesRequest) -> list[EmailMessageSummary]:
        missing = self._config.missing_required_values()
        if missing:
            missing_values = ", ".join(missing)
            raise NylasConfigurationError(
                f"Nylas configuration is incomplete. Missing: {missing_values}"
            )

        query = urlencode({"limit": request.limit})
        base_uri = self._config.api_uri.rstrip("/")
        url = f"{base_uri}/v3/grants/{self._config.grant_id}/messages?{query}"
        payload = self._transport.get_json(
            url,
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Accept": "application/json",
            },
        )
        return [_message_from_nylas(item) for item in payload.get("data", [])]


def _message_from_nylas(data: dict[str, Any]) -> EmailMessageSummary:
    return EmailMessageSummary(
        id=str(data["id"]),
        provider="nylas",
        subject=data.get("subject"),
        from_=_addresses(data.get("from", [])),
        to=_addresses(data.get("to", [])),
        date=data.get("date"),
        snippet=data.get("snippet"),
        unread=data.get("unread"),
    )


def _addresses(values: list[dict[str, Any]]) -> list[EmailAddress]:
    return [
        EmailAddress(address=str(value.get("email", "")), name=value.get("name"))
        for value in values
        if value.get("email")
    ]


def _http_error_message(error: HTTPError) -> str:
    body = error.read().decode("utf-8", errors="replace")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = {}

    provider_message = (
        payload.get("error", {}).get("message")
        or payload.get("message")
        or body.strip()
        or "Nylas request failed."
    )

    if error.code == 401:
        return "Nylas rejected the API key or authorization header."
    if error.code == 403:
        return "Nylas denied access to this grant or scope."
    if error.code == 404:
        return "Nylas could not find the grant or requested resource."
    if error.code == 429:
        return "Nylas rate limit reached. Try again later."
    return f"Nylas request failed with HTTP {error.code}: {provider_message}"
