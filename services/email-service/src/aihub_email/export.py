"""Local export helpers for Email service outputs."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path

from .models import EmailMessageSummary


DEFAULT_EXPORT_DIR = Path("exports")


def message_to_dict(message: EmailMessageSummary) -> dict:
    data = asdict(message)
    data["from"] = data.pop("from_")
    return data


def write_message_export(
    messages: list[EmailMessageSummary],
    account_id: str,
    output_path: str | Path | None = None,
) -> Path:
    destination = Path(output_path) if output_path else _default_output_path(account_id)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "account_id": account_id,
        "message_count": len(messages),
        "messages": [message_to_dict(message) for message in messages],
    }
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination


def _default_output_path(account_id: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return DEFAULT_EXPORT_DIR / account_id / f"recent-messages-{timestamp}.json"
