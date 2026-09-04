"""Configuration loading for the AIHub Email service."""

from __future__ import annotations

from dataclasses import dataclass
import os


DEFAULT_NYLAS_API_URI = "https://api.us.nylas.com"


@dataclass(frozen=True)
class NylasConfig:
    api_key: str | None
    api_uri: str
    grant_id: str | None

    @classmethod
    def from_environment(cls) -> "NylasConfig":
        return cls(
            api_key=os.getenv("NYLAS_API_KEY"),
            api_uri=os.getenv("NYLAS_API_URI", DEFAULT_NYLAS_API_URI),
            grant_id=os.getenv("NYLAS_GRANT_ID"),
        )

    def missing_required_values(self) -> list[str]:
        missing: list[str] = []
        if not self.api_key:
            missing.append("NYLAS_API_KEY")
        if not self.grant_id:
            missing.append("NYLAS_GRANT_ID")
        return missing
