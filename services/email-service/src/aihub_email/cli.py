"""Command-line entry point for local Email service checks."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata

from .accounts import list_account_statuses
from .config import NylasConfig
from .delete_plan import execute_delete_plan
from .export import message_to_dict, write_message_export
from .nylas_client import (
    NylasApiError,
    NylasConfigurationError,
    NylasEmailClient,
    NylasNetworkError,
    RecentMessagesRequest,
)
from .search import MessageSearchRequest, search_exported_messages
from .summary import ExportSummary, summarize_export_file, summarize_latest_export
from .today import TodayReviewRequest, build_today_review


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AIHub Email service")
    parser.add_argument("--env-file", default=".env", help="Path to local environment file.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check-config", help="Check local Nylas configuration.")
    check.add_argument("--account", default="default", help="Named account alias.")
    accounts = subparsers.add_parser("list-accounts", help="List local account configuration.")
    accounts.add_argument("--json", action="store_true", help="Print JSON output.")
    accounts.add_argument("--ready-only", action="store_true", help="Only show configured accounts.")
    recent = subparsers.add_parser("list-recent-messages", help="List recent messages.")
    recent.add_argument("--account", default="default", help="Named account alias.")
    recent.add_argument("--limit", type=int, default=10, help="Number of messages to list, 1-50.")
    recent.add_argument("--json", action="store_true", help="Print JSON output.")
    recent.add_argument("--ascii", action="store_true", help="Print ASCII-safe text output.")
    recent.add_argument("--export", action="store_true", help="Save results to a local JSON export.")
    recent.add_argument("--output", help="Optional export path.")
    search = subparsers.add_parser("search-exports", help="Search latest local message export.")
    search.add_argument("--account", default="default", help="Named account alias.")
    search.add_argument("--query", help="Text to match in subject, snippet, sender, or recipient.")
    search.add_argument("--sender", help="Text to match in sender.")
    search.add_argument("--unread", action="store_true", help="Only include unread messages.")
    search.add_argument("--limit", type=int, default=10, help="Number of messages to list, 1-100.")
    search.add_argument("--json", action="store_true", help="Print JSON output.")
    search.add_argument("--ascii", action="store_true", help="Print ASCII-safe text output.")
    summary = subparsers.add_parser("summarize-export", help="Summarize latest local export.")
    summary.add_argument("--account", default="default", help="Named account alias.")
    summary.add_argument("--top", type=int, default=10, help="Number of top senders to show, 1-50.")
    summary.add_argument("--json", action="store_true", help="Print JSON output.")
    summary.add_argument("--ascii", action="store_true", help="Print ASCII-safe text output.")
    refresh = subparsers.add_parser("refresh-snapshot", help="Fetch, export, and summarize messages.")
    refresh.add_argument("--account", default="default", help="Named account alias.")
    refresh.add_argument("--limit", type=int, default=10, help="Number of messages to fetch, 1-50.")
    refresh.add_argument("--top", type=int, default=10, help="Number of top senders to show, 1-50.")
    refresh.add_argument("--json", action="store_true", help="Print JSON summary output.")
    refresh.add_argument("--ascii", action="store_true", help="Print ASCII-safe text output.")
    today = subparsers.add_parser("today-review", help="Build local review for today's messages.")
    today.add_argument("--account", action="append", dest="accounts", help="Account alias to include.")
    today.add_argument("--timezone", default="America/New_York", help="Timezone for today's date.")
    today.add_argument("--json", action="store_true", help="Print JSON output.")
    delete_plan = subparsers.add_parser("execute-delete-plan", help="Move reviewed messages to Trash.")
    delete_plan.add_argument("--plan", required=True, help="Path to reviewed delete plan JSON.")
    delete_plan.add_argument(
        "--yes-trash",
        action="store_true",
        help="Required confirmation flag for moving messages to Trash.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "check-config":
        config = NylasConfig.from_environment_file(args.env_file, account_id=args.account)
        client = NylasEmailClient(config)
        if client.is_configured:
            print(f"Nylas configuration is present for account '{args.account}'.")
            return 0

        missing = ", ".join(config.missing_required_values())
        print(f"Nylas configuration is incomplete. Missing: {missing}")
        return 1

    if args.command == "list-accounts":
        statuses = list_account_statuses(env_file=args.env_file)
        if args.ready_only:
            statuses = [status for status in statuses if status.configured]
        if args.json:
            print(json.dumps([status.__dict__ for status in statuses], indent=2))
        else:
            for status in statuses:
                state = "ready" if status.configured else "missing " + ", ".join(status.missing)
                duplicate = "\tduplicate grant" if status.duplicate_grant else ""
                print(f"{status.account_id}\t{status.grant_id_env}\t{state}{duplicate}")
        return 0

    if args.command == "list-recent-messages":
        try:
            messages = _fetch_recent_messages(args.env_file, args.account, args.limit)
        except (ValueError, NylasConfigurationError, NylasApiError, NylasNetworkError) as error:
            return _print_cli_error(error)

        if args.json:
            print(json.dumps([message_to_dict(message) for message in messages], indent=2))
        else:
            for message in messages:
                subject = message.subject or "(no subject)"
                sender = message.from_[0].address if message.from_ else "(unknown sender)"
                if args.ascii:
                    subject = _ascii_safe(subject)
                    sender = _ascii_safe(sender)
                _print_line(f"{message.id}\t{sender}\t{subject}")
        if args.export:
            destination = write_message_export(messages, args.account, args.output)
            print(f"Exported {len(messages)} messages to {destination}")
        return 0

    if args.command == "refresh-snapshot":
        try:
            messages = _fetch_recent_messages(args.env_file, args.account, args.limit)
            destination = write_message_export(messages, args.account)
            summary = summarize_export_file(destination, top=args.top)
        except (ValueError, NylasConfigurationError, NylasApiError, NylasNetworkError) as error:
            return _print_cli_error(error)

        if args.json:
            print(json.dumps(summary.to_dict(), indent=2))
        else:
            print(f"Refreshed {summary.message_count} messages to {summary.export_path}")
            _print_summary(summary, ascii_safe=args.ascii)
        return 0

    if args.command == "search-exports":
        try:
            messages = search_exported_messages(
                MessageSearchRequest(
                    account_id=args.account,
                    query=args.query,
                    sender=args.sender,
                    unread=True if args.unread else None,
                    limit=args.limit,
                )
            )
        except ValueError as error:
            print(f"Invalid request: {error}", file=sys.stderr)
            return 2
        except FileNotFoundError as error:
            print(str(error), file=sys.stderr)
            return 1

        if args.json:
            print(json.dumps(messages, indent=2))
        else:
            for message in messages:
                subject = message.get("subject") or "(no subject)"
                sender = _first_address(message.get("from", []))
                if args.ascii:
                    subject = _ascii_safe(subject)
                    sender = _ascii_safe(sender)
                _print_line(f"{message.get('id')}\t{sender}\t{subject}")
        return 0

    if args.command == "summarize-export":
        try:
            summary = summarize_latest_export(account_id=args.account, top=args.top)
        except ValueError as error:
            print(f"Invalid request: {error}", file=sys.stderr)
            return 2
        except FileNotFoundError as error:
            print(str(error), file=sys.stderr)
            return 1

        if args.json:
            print(json.dumps(summary.to_dict(), indent=2))
        else:
            _print_summary(summary, ascii_safe=args.ascii)
        return 0

    if args.command == "today-review":
        try:
            review_path = build_today_review(
                TodayReviewRequest(
                    account_ids=args.accounts,
                    env_file=args.env_file,
                    timezone_name=args.timezone,
                )
            )
        except ValueError as error:
            print(f"Invalid request: {error}", file=sys.stderr)
            return 2

        if args.json:
            print(review_path.read_text(encoding="utf-8"))
        else:
            payload = json.loads(review_path.read_text(encoding="utf-8"))
            print(f"Review: {review_path}")
            print(f"Date: {payload['review_date']} ({payload['timezone']})")
            print(f"Accounts: {payload['account_count']}")
            print(f"Messages today: {payload['message_count']}")
            print(f"Action candidates: {payload['action_candidate_count']}")
        return 0

    if args.command == "execute-delete-plan":
        if not args.yes_trash:
            print("Refusing to delete without --yes-trash.", file=sys.stderr)
            return 2
        try:
            results = execute_delete_plan(args.plan, env_file=args.env_file)
        except (ValueError, NylasConfigurationError, NylasApiError, NylasNetworkError) as error:
            return _print_cli_error(error)

        print(f"Moved {len(results)} messages to Trash.")
        for result in results:
            print(f"{result['account_id']}\t{result['message_id']}\t{result['subject']}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _print_line(value: str) -> None:
    print(value.encode("utf-8", errors="replace").decode("utf-8"))


def _fetch_recent_messages(env_file: str, account: str, limit: int):
    config = NylasConfig.from_environment_file(env_file, account_id=account)
    client = NylasEmailClient(config)
    return client.list_recent_messages(RecentMessagesRequest(limit=limit))


def _print_cli_error(error: Exception) -> int:
    if isinstance(error, ValueError):
        print(f"Invalid request: {error}", file=sys.stderr)
        return 2
    print(str(error), file=sys.stderr)
    return 1


def _print_summary(summary: ExportSummary, ascii_safe: bool = False) -> None:
    print(f"Account: {summary.account_id}")
    print(f"Export: {summary.export_path}")
    print(f"Messages: {summary.message_count}")
    print(f"Unread: {summary.unread_count}")
    print("Top senders:")
    for sender, count in summary.top_senders:
        if ascii_safe:
            sender = _ascii_safe(sender)
        print(f"{count}\t{sender}")


def _ascii_safe(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", errors="replace").decode("ascii")


def _first_address(addresses: list[dict]) -> str:
    if not addresses:
        return "(unknown sender)"
    return addresses[0].get("address") or "(unknown sender)"


if __name__ == "__main__":
    raise SystemExit(main())
