"""Command-line entry point for local Email service checks."""

from __future__ import annotations

import argparse

from .config import NylasConfig
from .nylas_client import NylasEmailClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AIHub Email service")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-config", help="Check local Nylas configuration.")
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

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
