"""Local summaries for exported Email service snapshots."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .export import DEFAULT_EXPORT_DIR
from .search import latest_export_path


@dataclass(frozen=True)
class ExportSummary:
    account_id: str
    export_path: str
    exported_at: str | None
    message_count: int
    unread_count: int
    top_senders: list[tuple[str, int]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "export_path": self.export_path,
            "exported_at": self.exported_at,
            "message_count": self.message_count,
            "unread_count": self.unread_count,
            "top_senders": [
                {"sender": sender, "count": count} for sender, count in self.top_senders
            ],
        }


def summarize_latest_export(
    account_id: str = "default",
    export_dir: Path = DEFAULT_EXPORT_DIR,
    top: int = 10,
) -> ExportSummary:
    if top < 1 or top > 50:
        raise ValueError("top must be between 1 and 50")

    export_path = latest_export_path(account_id, export_dir)
    if export_path is None:
        raise FileNotFoundError(f"No exports found for account '{account_id}'.")

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    messages = payload.get("messages", [])
    senders = Counter(_first_sender(message) for message in messages)
    return ExportSummary(
        account_id=account_id,
        export_path=str(export_path),
        exported_at=payload.get("exported_at"),
        message_count=len(messages),
        unread_count=sum(1 for message in messages if message.get("unread") is True),
        top_senders=senders.most_common(top),
    )


def summarize_export_file(
    export_path: str | Path,
    top: int = 10,
) -> ExportSummary:
    if top < 1 or top > 50:
        raise ValueError("top must be between 1 and 50")

    path = Path(export_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    messages = payload.get("messages", [])
    senders = Counter(_first_sender(message) for message in messages)
    return ExportSummary(
        account_id=payload.get("account_id", "unknown"),
        export_path=str(path),
        exported_at=payload.get("exported_at"),
        message_count=len(messages),
        unread_count=sum(1 for message in messages if message.get("unread") is True),
        top_senders=senders.most_common(top),
    )


def _first_sender(message: dict[str, Any]) -> str:
    senders = message.get("from", [])
    if not senders:
        return "(unknown sender)"
    first = senders[0]
    return first.get("address") or first.get("name") or "(unknown sender)"
