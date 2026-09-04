from aihub_email.config import DEFAULT_NYLAS_API_URI, NylasConfig


def test_nylas_config_uses_default_api_uri(monkeypatch):
    monkeypatch.delenv("NYLAS_API_KEY", raising=False)
    monkeypatch.delenv("NYLAS_API_URI", raising=False)
    monkeypatch.delenv("NYLAS_GRANT_ID", raising=False)

    config = NylasConfig.from_environment()

    assert config.api_uri == DEFAULT_NYLAS_API_URI


def test_nylas_config_reports_missing_required_values(monkeypatch):
    monkeypatch.delenv("NYLAS_API_KEY", raising=False)
    monkeypatch.delenv("NYLAS_GRANT_ID", raising=False)

    config = NylasConfig.from_environment()

    assert config.missing_required_values() == ["NYLAS_API_KEY", "NYLAS_GRANT_ID"]


def test_nylas_config_loads_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "NYLAS_API_KEY=test-key",
                "NYLAS_API_URI=https://api.eu.nylas.com",
                "NYLAS_GRANT_ID='grant-1'",
            ]
        ),
        encoding="utf-8",
    )

    config = NylasConfig.from_environment_file(env_file, environ={})

    assert config.api_key == "test-key"
    assert config.api_uri == "https://api.eu.nylas.com"
    assert config.grant_id == "grant-1"


def test_nylas_config_env_file_overrides_process_environment(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("NYLAS_API_KEY=file-key\nNYLAS_GRANT_ID=file-grant\n", encoding="utf-8")

    config = NylasConfig.from_environment_file(
        env_file,
        environ={"NYLAS_API_KEY": "process-key", "NYLAS_GRANT_ID": "process-grant"},
    )

    assert config.api_key == "file-key"
    assert config.grant_id == "file-grant"
