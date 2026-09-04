"""Read-only Nylas client boundary."""

from __future__ import annotations

from dataclasses import dataclass

from .config import NylasConfig


@dataclass(frozen=True)
class RecentMessagesRequest:
    limit: int = 10


class NylasEmailClient:
    def __init__(self, config: NylasConfig) -> None:
        self._config = config

    @property
    def is_configured(self) -> bool:
        return not self._config.missing_required_values()

    def list_recent_messages(self, request: RecentMessagesRequest) -> None:
        raise NotImplementedError(
            "Live Nylas message retrieval is not implemented yet. "
            "This scaffold currently defines the read-only provider boundary only."
        )
