"""Local daily review generation from live Email snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
import json
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .accounts import configured_account_ids
from .config import NylasConfig
from .export import DEFAULT_EXPORT_DIR, write_message_export
from .nylas_client import NylasEmailClient, RecentMessagesRequest


DEFAULT_REVIEW_DIR = Path("reviews")
DEFAULT_TIMEZONE = "America/New_York"

ACTION_KEYWORDS = (
    "action required",
    "approval",
    "approve",
    "confirm",
    "deadline",
    "due",
    "failed",
    "invoice",
    "overdue",
    "past due",
    "payment",
    "required",
    "respond",
    "review",
    "security alert",
    "sign",
    "urgent",
    "verify",
)


@dataclass(frozen=True)
class TodayReviewRequest:
    account_ids: list[str] | None = None
    env_file: str | Path = ".env"
    export_dir: Path = DEFAULT_EXPORT_DIR
    review_dir: Path = DEFAULT_REVIEW_DIR
    timezone_name: str = DEFAULT_TIMEZONE
    review_date: date | None = None


def build_today_review(request: TodayReviewRequest) -> Path:
    timezone = ZoneInfo(request.timezone_name)
    review_date = request.review_date or datetime.now(timezone).date()
    account_ids = request.account_ids or configured_account_ids(env_file=request.env_file)
    start = datetime.combine(review_date, time.min, tzinfo=timezone).timestamp()
    end = datetime.combine(review_date, time.max, tzinfo=timezone).timestamp()

    account_results = []
    all_messages = []
    for account_id in account_ids:
        config = NylasConfig.from_environment_file(request.env_file, account_id=account_id)
        fetched_messages = NylasEmailClient(config).list_recent_messages(
            RecentMessagesRequest(
                limit=200,
                received_after=int(start),
                received_before=int(end),
            )
        )
        export_path = write_message_export(fetched_messages, account_id)
        messages = [
            _annotate_message(account_id, message)
            for message in json.loads(export_path.read_text(encoding="utf-8")).get("messages", [])
            if _is_message_on_date(message, start, end)
            and _is_inbox_message(message)
            and not _is_trashed(message)
        ]
        account_results.append(
            {
                "account_id": account_id,
                "export_path": str(export_path),
                "message_count": len(messages),
                "messages": messages,
            }
        )
        all_messages.extend(messages)

    action_candidates = [message for message in all_messages if message["action_candidate"]]
    output_path = _review_output_path(request.review_dir, review_date)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "review_date": review_date.isoformat(),
                "timezone": request.timezone_name,
                "account_count": len(account_ids),
                "message_count": len(all_messages),
                "action_candidate_count": len(action_candidates),
                "accounts": account_results,
                "action_candidates": action_candidates,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return output_path


def _is_message_on_date(message: dict[str, Any], start: float, end: float) -> bool:
    message_date = message.get("date")
    if message_date is None:
        return False
    return start <= int(message_date) <= end


def _is_inbox_message(message: dict[str, Any]) -> bool:
    folders = " ".join(message.get("folders", [])).lower()
    return "inbox" in folders


def _is_trashed(message: dict[str, Any]) -> bool:
    folders = " ".join(message.get("folders", [])).lower()
    return "trash" in folders


def _annotate_message(account_id: str, message: dict[str, Any]) -> dict[str, Any]:
    reasons = _action_reasons(message)
    annotated = dict(message)
    annotated["account_id"] = account_id
    annotated["action_candidate"] = bool(reasons)
    annotated["action_reasons"] = reasons
    return annotated


def _action_reasons(message: dict[str, Any]) -> list[str]:
    text = " ".join(
        str(value or "")
        for value in [
            message.get("subject"),
            message.get("snippet"),
            _address_text(message.get("from", [])),
        ]
    ).lower()
    return [keyword for keyword in ACTION_KEYWORDS if keyword in text]


def _address_text(addresses: list[dict[str, Any]]) -> str:
    return " ".join(
        " ".join(str(value or "") for value in [address.get("name"), address.get("address")])
        for address in addresses
    )


def _review_output_path(review_dir: Path, review_date: date) -> Path:
    timestamp = datetime.now(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")
    return review_dir / review_date.isoformat() / f"today-review-{timestamp}.json"
