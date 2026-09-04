"""Provider-neutral Email capability models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EmailAddress:
    address: str
    name: str | None = None


@dataclass(frozen=True)
class EmailMessageSummary:
    id: str
    provider: str
    subject: str | None = None
    from_: list[EmailAddress] = field(default_factory=list)
    to: list[EmailAddress] = field(default_factory=list)
    date: int | None = None
    snippet: str | None = None
    unread: bool | None = None
    folders: list[str] = field(default_factory=list)
