"""Local spam rule loading for planned cleanup operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_SPAM_AUTO_DELETE_FILE = Path("config/spam-auto-delete.yaml")


@dataclass(frozen=True)
class SpamAutoDeleteRules:
    domains: set[str] = field(default_factory=set)
    senders: set[str] = field(default_factory=set)

    def matches_sender(self, sender: str) -> bool:
        normalized = sender.strip().lower()
        domain = normalized.split("@", 1)[1] if "@" in normalized else ""
        return normalized in self.senders or domain in self.domains


def load_spam_auto_delete_rules(
    path: str | Path = DEFAULT_SPAM_AUTO_DELETE_FILE,
) -> SpamAutoDeleteRules:
    values = _read_simple_yaml_lists(Path(path))
    return SpamAutoDeleteRules(
        domains={value.lower() for value in values.get("auto_delete_domains", [])},
        senders={value.lower() for value in values.get("auto_delete_senders", [])},
    )


def _read_simple_yaml_lists(path: Path) -> dict[str, list[str]]:
    lists: dict[str, list[str]] = {}
    current_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":") and not line.startswith("-"):
            current_key = line[:-1].strip()
            lists.setdefault(current_key, [])
            continue
        if current_key and line.startswith("- "):
            lists[current_key].append(line[2:].strip())
    return lists
