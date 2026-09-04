from aihub_email.config import NylasConfig
import pytest

from aihub_email.nylas_client import (
    NylasConfigurationError,
    NylasEmailClient,
    RecentMessagesRequest,
)


class FakeTransport:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get_json(self, url, headers):
        self.calls.append((url, headers))
        return self.payload

    def delete_json(self, url, headers):
        self.calls.append((url, headers))
        return {"request_id": "request-1"}


def test_list_recent_messages_uses_grant_scoped_read_endpoint():
    transport = FakeTransport(
        {
            "data": [
                {
                    "id": "message-1",
                    "subject": "Hello",
                    "from": [{"email": "sender@example.com", "name": "Sender"}],
                    "to": [{"email": "recipient@example.com"}],
                    "date": 123,
                    "snippet": "Short preview",
                    "unread": True,
                }
            ]
        }
    )
    config = NylasConfig(
        api_key="test-key",
        api_uri="https://api.us.nylas.com",
        grant_id="grant-1",
    )

    client = NylasEmailClient(config, transport=transport)
    messages = client.list_recent_messages(RecentMessagesRequest(limit=5))

    assert transport.calls[0][0] == "https://api.us.nylas.com/v3/grants/grant-1/messages?limit=5"
    assert transport.calls[0][1]["Authorization"] == "Bearer test-key"
    assert messages[0].id == "message-1"
    assert messages[0].from_[0].address == "sender@example.com"


def test_list_recent_messages_requires_config():
    client = NylasEmailClient(NylasConfig(api_key=None, api_uri="https://api.us.nylas.com", grant_id=None))

    with pytest.raises(NylasConfigurationError):
        client.list_recent_messages(RecentMessagesRequest(limit=5))


def test_recent_messages_limit_must_be_in_safe_range():
    with pytest.raises(ValueError, match="limit must be between 1 and 50"):
        RecentMessagesRequest(limit=0)

    with pytest.raises(ValueError, match="limit must be between 1 and 50"):
        RecentMessagesRequest(limit=51)


def test_move_message_to_trash_uses_delete_endpoint():
    transport = FakeTransport({})
    config = NylasConfig(
        api_key="test-key",
        api_uri="https://api.us.nylas.com",
        grant_id="grant-1",
    )

    client = NylasEmailClient(config, transport=transport)
    client.move_message_to_trash("message-1")

    assert transport.calls[0][0] == "https://api.us.nylas.com/v3/grants/grant-1/messages/message-1"
    assert transport.calls[0][1]["Authorization"] == "Bearer test-key"
