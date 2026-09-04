"""Execute reviewed local delete plans."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import NylasConfig
from .nylas_client import NylasEmailClient


def execute_delete_plan(plan_path: str | Path, env_file: str | Path = ".env") -> list[dict[str, Any]]:
    path = Path(plan_path)
    plan = json.loads(path.read_text(encoding="utf-8"))
    if plan.get("delete_mode") != "trash":
        raise ValueError("Only trash delete plans are supported.")

    results = []
    for message in plan.get("messages", []):
        account_id = message["account_id"]
        message_id = message["message_id"]
        config = NylasConfig.from_environment_file(env_file, account_id=account_id)
        client = NylasEmailClient(config)
        client.move_message_to_trash(message_id)
        results.append(
            {
                "account_id": account_id,
                "message_id": message_id,
                "subject": message.get("subject"),
                "status": "trashed",
            }
        )
    return results
