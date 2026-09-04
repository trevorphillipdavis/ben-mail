"""Command-line entry point for local Email service checks."""

from __future__ import annotations

import argparse
import json

from .config import NylasConfig
from .nylas_client import NylasEmailClient, RecentMessagesRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AIHub Email service")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-config", help="Check local Nylas configuration.")
    recent = subparsers.add_parser("list-recent-messages", help="List recent messages.")
    recent.add_argument("--limit", type=int, default=10)
    recent.add_argument("--json", action="store_true", help="Print JSON output.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "check-config":
        config = NylasConfig.from_environment()
        client = NylasEmailClient(config)
        if client.is_configured:
            print("Nylas configuration is present.")
            return 0

        missing = ", ".join(config.missing_required_values())
        print(f"Nylas configuration is incomplete. Missing: {missing}")
        return 1

    if args.command == "list-recent-messages":
        config = NylasConfig.from_environment()
        client = NylasEmailClient(config)
        messages = client.list_recent_messages(RecentMessagesRequest(limit=args.limit))
        if args.json:
            print(json.dumps([_message_to_dict(message) for message in messages], indent=2))
        else:
            for message in messages:
                subject = message.subject or "(no subject)"
                sender = message.from_[0].address if message.from_ else "(unknown sender)"
                print(f"{message.id}\t{sender}\t{subject}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _message_to_dict(message):
    return {
        "id": message.id,
        "provider": message.provider,
        "subject": message.subject,
        "from": [address.__dict__ for address in message.from_],
        "to": [address.__dict__ for address in message.to],
        "date": message.date,
        "snippet": message.snippet,
        "unread": message.unread,
    }


if __name__ == "__main__":
    raise SystemExit(main())
