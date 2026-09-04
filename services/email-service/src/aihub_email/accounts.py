"""Local account inventory for the Email service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

from .config import (
    DEFAULT_ENV_FILE,
    NylasConfig,
    _grant_id_env_for_account,
    _normalize_account_id,
    _read_env_file,
)


DEFAULT_ACCOUNT_IDS = ("default", "personal", "work")


@dataclass(frozen=True)
class EmailAccountStatus:
    account_id: str
    grant_id_env: str
    configured: bool
    missing: list[str]
    duplicate_grant: bool = False


def list_account_statuses(
    account_ids: tuple[str, ...] = DEFAULT_ACCOUNT_IDS,
    env_file: str | Path = DEFAULT_ENV_FILE,
) -> list[EmailAccountStatus]:
    values = _read_env_file(Path(env_file))
    statuses: list[EmailAccountStatus] = []
    for account_id in account_ids:
        account_id = _normalize_account_id(account_id)
        config = NylasConfig.from_environment_file(env_file, environ={}, account_id=account_id)
        grant_id_env = _grant_id_env_for_account(account_id)
        configured = not config.missing_required_values()
        statuses.append(
            EmailAccountStatus(
                account_id=account_id,
                grant_id_env=grant_id_env,
                configured=configured,
                missing=config.missing_required_values(),
            )
        )

    statuses = _include_discovered_aliases(statuses, values, env_file)
    return _mark_duplicate_grants(statuses, values)


def _include_discovered_aliases(
    statuses: list[EmailAccountStatus],
    values: dict[str, str],
    env_file: str | Path,
) -> list[EmailAccountStatus]:
    known = {status.account_id for status in statuses}
    for key in sorted(values):
        if not key.startswith("NYLAS_GRANT_ID_"):
            continue
        account_id = _normalize_account_id(key.removeprefix("NYLAS_GRANT_ID_"))
        if account_id in known:
            continue
        config = NylasConfig.from_environment_file(env_file, environ={}, account_id=account_id)
        statuses.append(
            EmailAccountStatus(
                account_id=account_id,
                grant_id_env=key,
                configured=not config.missing_required_values(),
                missing=config.missing_required_values(),
            )
        )
    return statuses


def configured_account_ids(env_file: str | Path = DEFAULT_ENV_FILE) -> list[str]:
    return [
        status.account_id
        for status in list_account_statuses(env_file=env_file)
        if status.configured
    ]


def _mark_duplicate_grants(
    statuses: list[EmailAccountStatus],
    values: dict[str, str],
) -> list[EmailAccountStatus]:
    grants_to_envs: dict[str, list[str]] = defaultdict(list)
    for status in statuses:
        grant_id = values.get(status.grant_id_env)
        if grant_id:
            grants_to_envs[grant_id].append(status.grant_id_env)

    duplicate_envs = {
        env_name
        for env_names in grants_to_envs.values()
        if len(env_names) > 1
        for env_name in env_names
    }

    return [
        EmailAccountStatus(
            account_id=status.account_id,
            grant_id_env=status.grant_id_env,
            configured=status.configured,
            missing=status.missing,
            duplicate_grant=status.grant_id_env in duplicate_envs,
        )
        for status in statuses
    ]
