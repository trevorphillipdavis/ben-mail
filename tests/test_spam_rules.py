from aihub_email.spam_rules import load_spam_auto_delete_rules


def test_spam_rules_match_blocked_domain():
    rules = load_spam_auto_delete_rules()

    assert rules.matches_sender("contact@8eobphe88eobphe8.com")


def test_spam_rules_match_blocked_exact_sender_on_shared_domain():
    rules = load_spam_auto_delete_rules()

    assert rules.matches_sender("jess4766881gamez@outlook.com")


def test_spam_rules_do_not_block_entire_outlook_domain():
    rules = load_spam_auto_delete_rules()

    assert not rules.matches_sender("real.person@outlook.com")


def test_spam_rules_exclude_juppiterailabs_domain():
    rules = load_spam_auto_delete_rules()

    assert not rules.matches_sender("sales@juppiterailabs.com")
