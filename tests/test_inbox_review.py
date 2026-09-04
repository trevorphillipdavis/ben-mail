from aihub_email.inbox_review import _classify_message


def test_keeps_tax_email_from_known_tax_sender():
    message = {
        "subject": "Re: 2025 Taxes",
        "snippet": (
            "All taxes have been filed and accepted except for the $25 filing fee "
            "to NY State."
        ),
        "folders": ["IMPORTANT", "CATEGORY_PERSONAL", "INBOX"],
        "from": [{"address": "hailu@haddisgroup.com", "name": "Hailu Jardines"}],
    }

    assert _classify_message(message) == "keep"


def test_keeps_tax_signature_email_from_secure_document_sender():
    message = {
        "subject": "Federal & NY State Tax Returns",
        "snippet": (
            "Federal and NY State tax return for 1030 Elmwood, LLC & personal. "
            "Your signature or input is requested."
        ),
        "folders": ["IMPORTANT", "CATEGORY_UPDATES", "INBOX"],
        "from": [
            {
                "address": "hailuhaddisgroupcom@no-reply.encyro.com",
                "name": "Hailu Jardines (Haddis Group) via Encyro",
            }
        ],
    }

    assert _classify_message(message) == "keep"


def test_keeps_credit_card_payment_due_notice():
    message = {
        "subject": "Your credit card payment is due",
        "snippet": "Your payment is due soon for your Capital One account.",
        "folders": ["UNREAD", "IMPORTANT", "CATEGORY_UPDATES", "INBOX"],
        "from": [
            {
                "address": "capitalone@notification.capitalone.com",
                "name": "Capital One",
            }
        ],
    }

    assert _classify_message(message) == "keep"


def test_promotions_remain_bulk_after_protection_rules():
    message = {
        "subject": "Flash Sale! 24 hours only!",
        "snippet": "These deals won't last. Free shipping on orders today only.",
        "folders": ["CATEGORY_PROMOTIONS", "UNREAD", "INBOX"],
        "from": [{"address": "woot@marketing.woot.com", "name": "Woot"}],
    }

    assert _classify_message(message) == "bulk_or_ad"
