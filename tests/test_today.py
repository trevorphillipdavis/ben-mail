import json
from datetime import date

import aihub_email.today as today
from aihub_email.models import EmailAddress, EmailMessageSummary
from aihub_email.today import TodayReviewRequest, build_today_review


class FakeNylasEmailClient:
    def __init__(self, config):
        self.config = config

    def list_recent_messages(self, request):
        return [
            EmailMessageSummary(
                id="1",
                provider="nylas",
                subject="Invoice due today",
                snippet="Please review",
                from_=[EmailAddress(address="billing@example.com")],
                date=1788523200,
                folders=["INBOX"],
            )
        ]


def test_build_today_review_fetches_live_messages_and_flags_action_candidates(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(today, "NylasEmailClient", FakeNylasEmailClient)

    review_path = build_today_review(
        TodayReviewRequest(
            account_ids=["default"],
            export_dir=tmp_path / "exports",
            review_dir=tmp_path / "reviews",
            review_date=date(2026, 9, 4),
        )
    )

    payload = json.loads(review_path.read_text(encoding="utf-8"))
    assert payload["message_count"] == 1
    assert payload["action_candidate_count"] == 1
    assert payload["action_candidates"][0]["id"] == "1"
