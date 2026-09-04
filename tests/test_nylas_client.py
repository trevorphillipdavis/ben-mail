from aihub_email.config import NylasConfig
from aihub_email.nylas_client import NylasEmailClient, RecentMessagesRequest


class FakeTransport:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get_json(self, url, headers):
        self.calls.append((url, headers))
        return self.payload


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
