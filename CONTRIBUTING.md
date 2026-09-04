# Contributing to AIHub

AIHub is designed to stay modular, reproducible, and maintainable.

## Ground Rules

- Keep executable code in GitHub.
- Keep architecture, operational knowledge, ADRs, and SOPs in Obsidian-oriented documentation.
- Prefer capability interfaces over vendor-specific coupling.
- Prefer official APIs and supported integrations.
- Prefer deterministic local execution whenever practical.
- Do not commit secrets, API keys, passwords, tokens, or generated credential files.
- Propose architectural changes before implementing them.

## Repository Conventions

- `capabilities/` defines stable contracts and domain models.
- `services/` contains executable service boundaries.
- `providers/` contains integrations with external systems.
- `runtime/` contains local execution infrastructure.
- `shared/` contains reusable primitives that are not owned by one capability.
- `tests/` contains repository-level and cross-module tests.

## Implementation Conventions

- Keep new functionality behind a capability interface.
- Keep providers replaceable.
- Add tests when behavior is implemented.
- Add or update ADRs for meaningful architectural decisions.
- Add SOPs for repeatable operational workflows.

## Documentation Conventions

- Use ADRs for decisions that affect architecture, service boundaries, provider strategy, data flow, or long-term maintenance.
- Use SOPs for repeatable operations.
- Use capability docs to describe domain behavior and interfaces.
- Use provider docs to describe external system assumptions, API boundaries, and setup requirements.
