import json

import pytest

from aihub_email.summary import summarize_export_file, summarize_latest_export


def test_summarize_latest_export_counts_messages_unread_and_senders(tmp_path):
    account_dir = tmp_path / "default"
    account_dir.mkdir()
    export = account_dir / "recent-messages-20260101T000000Z.json"
    export.write_text(
        json.dumps(
            {
                "exported_at": "2026-01-01T00:00:00+00:00",
                "messages": [
                    {
                        "id": "1",
                        "from": [{"address": "sender@example.com"}],
                        "unread": True,
                    },
                    {
                        "id": "2",
                        "from": [{"address": "sender@example.com"}],
                        "unread": False,
                    },
                    {
                        "id": "3",
                        "from": [{"address": "other@example.com"}],
                        "unread": True,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_latest_export(account_id="default", export_dir=tmp_path, top=2)

    assert summary.message_count == 3
    assert summary.unread_count == 2
    assert summary.top_senders == [("sender@example.com", 2), ("other@example.com", 1)]


def test_summarize_latest_export_validates_top(tmp_path):
    with pytest.raises(ValueError, match="top must be between 1 and 50"):
        summarize_latest_export(account_id="default", export_dir=tmp_path, top=0)


def test_summarize_export_file_uses_payload_account_id(tmp_path):
    export = tmp_path / "messages.json"
    export.write_text(
        json.dumps({"account_id": "personal", "messages": []}),
        encoding="utf-8",
    )

    summary = summarize_export_file(export)

    assert summary.account_id == "personal"
    assert summary.export_path == str(export)
