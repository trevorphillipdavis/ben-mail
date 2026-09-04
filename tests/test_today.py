import json
from datetime import date

from aihub_email.today import TodayReviewRequest, build_today_review


def test_build_today_review_filters_messages_and_flags_action_candidates(tmp_path):
    export_dir = tmp_path / "exports"
    account_dir = export_dir / "default"
    account_dir.mkdir(parents=True)
    export = account_dir / "recent-messages-20260904T120000Z.json"
    export.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "id": "1",
                        "subject": "Invoice due today",
                        "snippet": "Please review",
                        "from": [{"address": "billing@example.com"}],
                        "date": 1788523200,
                    },
                    {
                        "id": "2",
                        "subject": "Old message",
                        "snippet": "Yesterday",
                        "from": [{"address": "old@example.com"}],
                        "date": 1788436800,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    review_path = build_today_review(
        TodayReviewRequest(
            account_ids=["default"],
            export_dir=export_dir,
            review_dir=tmp_path / "reviews",
            review_date=date(2026, 9, 4),
        )
    )

    payload = json.loads(review_path.read_text(encoding="utf-8"))
    assert payload["message_count"] == 1
    assert payload["action_candidate_count"] == 1
    assert payload["action_candidates"][0]["id"] == "1"
