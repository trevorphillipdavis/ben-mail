"""Configuration loading for the AIHub Email service."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re


DEFAULT_NYLAS_API_URI = "https://api.us.nylas.com"
DEFAULT_ENV_FILE = ".env"


@dataclass(frozen=True)
class NylasConfig:
    api_key: str | None
    api_uri: str
    grant_id: str | None
    account_id: str = "default"

    @classmethod
    def from_environment(cls) -> "NylasConfig":
        return cls(
            api_key=os.getenv("NYLAS_API_KEY"),
            api_uri=os.getenv("NYLAS_API_URI", DEFAULT_NYLAS_API_URI),
            grant_id=os.getenv("NYLAS_GRANT_ID"),
        )

    @classmethod
    def from_environment_file(
        cls,
        env_file: str | Path = DEFAULT_ENV_FILE,
        environ: dict[str, str] | None = None,
        account_id: str = "default",
    ) -> "NylasConfig":
        values = dict(environ or os.environ)
        values.update(_read_env_file(Path(env_file)))
        grant_id_env = _grant_id_env_for_account(account_id)
        return cls(
            api_key=values.get("NYLAS_API_KEY"),
            api_uri=values.get("NYLAS_API_URI", DEFAULT_NYLAS_API_URI),
            grant_id=values.get(grant_id_env),
            account_id=account_id,
        )

    def missing_required_values(self) -> list[str]:
        missing: list[str] = []
        if not self.api_key:
            missing.append("NYLAS_API_KEY")
        if not self.grant_id:
            missing.append(_grant_id_env_for_account(self.account_id))
        return missing


def _grant_id_env_for_account(account_id: str) -> str:
    if _normalize_account_id(account_id) == "default":
        return "NYLAS_GRANT_ID"
    normalized = re.sub(r"[^A-Z0-9]+", "_", account_id.strip().upper()).strip("_")
    return f"NYLAS_GRANT_ID_{normalized}"


def _normalize_account_id(account_id: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", account_id.strip().lower()).strip("_")
    return normalized or "default"


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = _clean_env_value(value.strip())
    return values


def _clean_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
