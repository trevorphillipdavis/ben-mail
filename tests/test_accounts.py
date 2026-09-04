from aihub_email.accounts import configured_account_ids, list_account_statuses


def test_list_account_statuses_reports_defaults(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("NYLAS_API_KEY=test-key\nNYLAS_GRANT_ID=default-grant\n", encoding="utf-8")

    statuses = list_account_statuses(env_file=env_file)

    by_id = {status.account_id: status for status in statuses}
    assert by_id["default"].configured is True
    assert by_id["personal"].configured is False
    assert by_id["personal"].missing == ["NYLAS_GRANT_ID_PERSONAL"]


def test_list_account_statuses_discovers_extra_aliases(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "NYLAS_API_KEY=test-key",
                "NYLAS_GRANT_ID=default-grant",
                "NYLAS_GRANT_ID_RENTALS=rentals-grant",
            ]
        ),
        encoding="utf-8",
    )

    statuses = list_account_statuses(env_file=env_file)

    by_id = {status.account_id: status for status in statuses}
    assert by_id["rentals"].configured is True
    assert by_id["rentals"].grant_id_env == "NYLAS_GRANT_ID_RENTALS"


def test_configured_account_ids_returns_only_ready_accounts(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "NYLAS_API_KEY=test-key\nNYLAS_GRANT_ID_GMAIL=test-grant\n",
        encoding="utf-8",
    )

    assert configured_account_ids(env_file=env_file) == ["gmail"]


def test_list_account_statuses_flags_duplicate_grants(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "NYLAS_API_KEY=test-key",
                "NYLAS_GRANT_ID_FIRST=same-grant",
                "NYLAS_GRANT_ID_SECOND=same-grant",
            ]
        ),
        encoding="utf-8",
    )

    statuses = list_account_statuses(env_file=env_file)
    by_id = {status.account_id: status for status in statuses}

    assert by_id["first"].duplicate_grant is True
    assert by_id["second"].duplicate_grant is True
