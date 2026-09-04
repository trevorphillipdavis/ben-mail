"""Local search over exported Email service snapshots."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .export import DEFAULT_EXPORT_DIR


@dataclass(frozen=True)
class MessageSearchRequest:
    account_id: str = "default"
    query: str | None = None
    sender: str | None = None
    unread: bool | None = None
    limit: int = 10
    export_dir: Path = DEFAULT_EXPORT_DIR

    def __post_init__(self) -> None:
        if self.limit < 1 or self.limit > 100:
            raise ValueError("limit must be between 1 and 100")


def search_exported_messages(request: MessageSearchRequest) -> list[dict[str, Any]]:
    export_path = latest_export_path(request.account_id, request.export_dir)
    if export_path is None:
        raise FileNotFoundError(f"No exports found for account '{request.account_id}'.")

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    matches = [
        message
        for message in payload.get("messages", [])
        if _matches_query(message, request.query)
        and _matches_sender(message, request.sender)
        and _matches_unread(message, request.unread)
    ]
    return matches[: request.limit]


def latest_export_path(account_id: str, export_dir: Path = DEFAULT_EXPORT_DIR) -> Path | None:
    account_dir = export_dir / account_id
    if not account_dir.exists():
        return None
    exports = sorted(account_dir.glob("recent-messages-*.json"), key=lambda path: path.name)
    return exports[-1] if exports else None


def _matches_query(message: dict[str, Any], query: str | None) -> bool:
    if not query:
        return True
    haystack = " ".join(
        str(value or "")
        for value in [
            message.get("subject"),
            message.get("snippet"),
            _address_text(message.get("from", [])),
            _address_text(message.get("to", [])),
        ]
    ).lower()
    return query.lower() in haystack


def _matches_sender(message: dict[str, Any], sender: str | None) -> bool:
    if not sender:
        return True
    return sender.lower() in _address_text(message.get("from", [])).lower()


def _matches_unread(message: dict[str, Any], unread: bool | None) -> bool:
    if unread is None:
        return True
    return message.get("unread") is unread


def _address_text(addresses: list[dict[str, Any]]) -> str:
    return " ".join(
        " ".join(str(value or "") for value in [address.get("name"), address.get("address")])
        for address in addresses
    )
