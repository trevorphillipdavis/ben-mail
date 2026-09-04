import json

from aihub_email.export import message_to_dict, write_message_export
from aihub_email.models import EmailAddress, EmailMessageSummary


def test_message_to_dict_uses_provider_neutral_from_key():
    message = EmailMessageSummary(
        id="message-1",
        provider="nylas",
        from_=[EmailAddress(address="sender@example.com")],
    )

    data = message_to_dict(message)

    assert "from_" not in data
    assert data["from"] == [{"address": "sender@example.com", "name": None}]


def test_write_message_export_writes_json_payload(tmp_path):
    output = tmp_path / "messages.json"
    message = EmailMessageSummary(id="message-1", provider="nylas", subject="Hello")

    destination = write_message_export([message], account_id="default", output_path=output)

    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["account_id"] == "default"
    assert payload["message_count"] == 1
    assert payload["messages"][0]["id"] == "message-1"
