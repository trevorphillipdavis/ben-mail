"""Local review helpers for non-bulk Inbox messages."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
from typing import Any
from zoneinfo import ZoneInfo

from .config import NylasConfig
from .nylas_client import NylasEmailClient, RecentMessagesRequest


DEFAULT_REVIEW_DIR = Path("reviews")
PROMO_KEYWORDS = (
    "advertising email",
    "best sellers",
    "black friday",
    "clearance",
    "coupon",
    "deal",
    "discount",
    "free shipping",
    "labor day sale",
    "limited time",
    "marketing",
    "newsletter",
    "offers waiting",
    "offer",
    "promo",
    "promotion",
    "sale",
    "shop",
    "survey",
    "unsubscribe",
    "view in browser",
    "view the online version",
)
SPAM_SIGNALS = (
    "gift card",
    "claim your",
    "congratulations",
    "expiring in",
    "final notice",
    "immediate confirmation required",
    "randomly selected",
    "survey required",
    "transfer ready",
)
PROTECTED_KEYWORDS = (
    "accepted",
    "account",
    "authorized",
    "bank",
    "bill",
    "card payment is due",
    "completed:",
    "credit card payment",
    "debit block",
    "debt",
    "docusign",
    "document has been completed",
    "federal",
    "fee",
    "filed",
    "finance",
    "insurance",
    "invoice",
    "large transaction",
    "login from a new device",
    "ny state",
    "overdue balance",
    "payment is due",
    "paypal",
    "return",
    "shareholder reports",
    "sign or fill",
    "signature",
    "statement is now available",
    "tax",
    "transaction",
    "your signature or input is requested",
)
PROTECTED_SENDERS = (
    "capitalone@notification.capitalone.com",
    "citicards@info6.citi.com",
    "dse@docusign.net",
    "fidelity.investments@mail.fidelity.com",
    "hailu@haddisgroup.com",
    "noreply@quicken.com",
    "service@paypal.com",
)
PROTECTED_SENDER_DOMAINS = (
    "haddisgroup.com",
)


def review_inbox_non_bulk(
    account_id: str,
    env_file: str | Path = ".env",
    days: int = 30,
    limit: int = 200,
    timezone_name: str = "America/New_York",
    output_dir: Path = DEFAULT_REVIEW_DIR,
) -> Path:
    timezone = ZoneInfo(timezone_name)
    now = datetime.now(timezone)
    start = now - timedelta(days=days)
    config = NylasConfig.from_environment_file(env_file, account_id=account_id)
    messages = NylasEmailClient(config).list_recent_messages(
        RecentMessagesRequest(
            limit=limit,
            folder_id="INBOX",
            received_after=int(start.timestamp()),
            received_before=int(now.timestamp()),
        )
    )
    kept = []
    rejected = []
    for message in messages:
        data = _message_to_dict(message)
        category = _classify_message(data)
        data["local_classification"] = category
        if category == "keep":
            kept.append(data)
        else:
            rejected.append(data)

    output_path = output_dir / account_id / f"inbox-non-bulk-{now.strftime('%Y%m%dT%H%M%S')}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "account_id": account_id,
                "days": days,
                "timezone": timezone_name,
                "generated_at": now.isoformat(),
                "reviewed_count": len(messages),
                "kept_count": len(kept),
                "rejected_count": len(rejected),
                "kept_messages": kept,
                "rejected_messages": rejected,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return output_path


def _classify_message(message: dict[str, Any]) -> str:
    folders = " ".join(message.get("folders", [])).lower()
    if "trash" in folders or "spam" in folders or "junk" in folders:
        return "spam_or_trash"
    text = _message_text(message)
    sender = _first_sender(message)
    if _is_protected_message(sender, text):
        return "keep"
    if any(
        category in folders
        for category in ("category_promotions", "category_social", "category_forums")
    ):
        return "bulk_or_ad"
    if any(signal in text for signal in SPAM_SIGNALS):
        return "spam_like"
    if any(keyword in text for keyword in PROMO_KEYWORDS):
        return "bulk_or_ad"
    if _looks_random_sender(sender):
        return "spam_like"
    return "keep"


def _message_to_dict(message) -> dict[str, Any]:
    data = asdict(message)
    data["from"] = data.pop("from_")
    return data


def _message_text(message: dict[str, Any]) -> str:
    return " ".join(
        str(value or "")
        for value in [
            message.get("subject"),
            message.get("snippet"),
            _first_sender(message),
        ]
    ).lower()


def _first_sender(message: dict[str, Any]) -> str:
    senders = message.get("from", [])
    if not senders:
        return ""
    return senders[0].get("address") or ""


def _looks_random_sender(sender: str) -> bool:
    local = sender.split("@", 1)[0]
    domain = sender.split("@", 1)[1] if "@" in sender else ""
    return bool(
        re.fullmatch(r"[a-z0-9]{12,}", local.lower())
        or re.fullmatch(r"[a-z0-9]{10,}\.[a-z0-9.-]+", domain.lower())
    )


def _is_protected_message(sender: str, text: str) -> bool:
    sender = sender.lower()
    domain = sender.split("@", 1)[1] if "@" in sender else ""
    return (
        sender in PROTECTED_SENDERS
        or domain in PROTECTED_SENDER_DOMAINS
        or any(keyword in text for keyword in PROTECTED_KEYWORDS)
    )
