import json

import pytest

from aihub_email.search import MessageSearchRequest, latest_export_path, search_exported_messages


def test_latest_export_path_uses_newest_named_export(tmp_path):
    account_dir = tmp_path / "default"
    account_dir.mkdir()
    older = account_dir / "recent-messages-20260101T000000Z.json"
    newer = account_dir / "recent-messages-20260102T000000Z.json"
    older.write_text("{}", encoding="utf-8")
    newer.write_text("{}", encoding="utf-8")

    assert latest_export_path("default", tmp_path) == newer


def test_search_exported_messages_filters_by_query_sender_and_unread(tmp_path):
    account_dir = tmp_path / "default"
    account_dir.mkdir()
    export = account_dir / "recent-messages-20260101T000000Z.json"
    export.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "id": "1",
                        "subject": "Security alert",
                        "snippet": "New sign-in",
                        "from": [{"address": "no-reply@accounts.google.com", "name": "Google"}],
                        "to": [],
                        "unread": True,
                    },
                    {
                        "id": "2",
                        "subject": "Weekend sale",
                        "snippet": "Discounts",
                        "from": [{"address": "sales@example.com"}],
                        "to": [],
                        "unread": False,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    matches = search_exported_messages(
        MessageSearchRequest(
            account_id="default",
            query="security",
            sender="google",
            unread=True,
            export_dir=tmp_path,
        )
    )

    assert [message["id"] for message in matches] == ["1"]


def test_search_exported_messages_requires_existing_export(tmp_path):
    with pytest.raises(FileNotFoundError):
        search_exported_messages(MessageSearchRequest(account_id="default", export_dir=tmp_path))
