# AIHub

AIHub is a personal AI operating system for orchestrating reusable local services and supported external integrations.

The project is organized around capabilities rather than vendors. Orchestrators decide what should happen, services provide stable capability interfaces, providers integrate with external systems, and the local runtime performs deterministic execution whenever practical.

## Architecture

```text
User
  -> Orchestrator
  -> Capability
  -> Service
  -> Provider
  -> External Service
```

AIHub follows these principles:

- GitHub is the source of truth for executable code.
- Local Obsidian is the source of truth for personal operational knowledge.
- GitHub is the source of truth for executable project source.
- Prefer official APIs and supported integrations.
- Prefer deterministic local execution whenever practical.
- Use AI only when reasoning adds meaningful value.
- Design modular, reusable capabilities rather than one-off scripts.
- Never store secrets in documentation or source control.
- Build everything so it can be reproduced from a clean machine.
- Document architectural decisions as ADRs.

## Repository Layout

```text
orchestrators/        Entry points such as ChatGPT, voice, CLI, and future web UI
capabilities/         Stable capability contracts and domain models
providers/            External service integrations behind capability interfaces
services/             Executable service boundaries and adapters
runtime/              Local execution, scheduling, logging, and environment support
shared/               Shared primitives used across services
tests/                Cross-service and repository-level tests
docs/                 Repository documentation and references
config/               Non-secret configuration templates
```

## Current Status

This repository currently contains the initial skeleton plus read-only Nylas configuration scaffolding. No external API calls, authentication flows, schedulers, or message operations have been implemented yet.

The first scaffolded capability is Email, with a placeholder Nylas provider.

## Configuration

Use `config/aihub.yaml` as the local manifest template. Use `.env.example` to see expected environment variables. Do not commit secrets, tokens, credentials, or machine-specific values.

## Local Execution

AIHub should favor local scripts for deterministic work so routine checks and integrations do not require AI tokens.

Check local Nylas configuration with:

```powershell
$env:PYTHONPATH = "services/email-service/src"
python -m aihub_email.cli check-config
```

## Documentation

Architectural decisions are tracked in:

- `docs/adr/`

Operational knowledge belongs in the local Obsidian vault at `C:/Users/trevo/Dropbox/AIHub`.

Project-specific notes live under:

```text
Projects/email-integration/
```

Only intentionally promoted documentation should be committed to GitHub.
