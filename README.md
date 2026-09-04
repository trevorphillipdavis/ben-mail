# Ben Mail

Ben Mail is a local-first email automation project for reviewing and cleaning up multiple email accounts through Nylas.

It is designed as one modular AIHub capability project: reusable scripts do the deterministic work locally, while an AI assistant can reason over the small review outputs and decide what to run next.

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

This repository contains working local scaffolding for:

- multi-account Nylas configuration
- live Inbox review
- local exports and summaries
- local search over exports
- reviewed delete plans
- spam sender/domain auto-delete rules
- safe move-to-Trash execution

## Configuration

Use `.env.example` to see expected environment variables. Do not commit secrets, tokens, credentials, grants, exports, or review files.

See [Setup From Scratch](</C:/Users/trevo/Dropbox/GitHub/ben-mail/docs/setup-from-scratch.md>) for the full setup flow.

Quick start:

```powershell
.\install.ps1
```

The installer sets up the local Python environment, installs the `ben-mail` Codex skill into the user's local Codex app configuration, and then prompts for Nylas account setup.

## Local Execution

AIHub should favor local scripts for deterministic work so routine checks and integrations do not require AI tokens.

Check local Nylas configuration with:

```powershell
python -m aihub_email.cli check-config
```

List recent messages with:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10
```

By default, commands load local values from `.env`. Use `--env-file path\to\.env` to point at a different local file.

Named accounts are supported through grant-specific environment variables:

```text
NYLAS_GRANT_ID_PERSONAL=
NYLAS_GRANT_ID_WORK=
```

Example:

```powershell
python -m aihub_email.cli list-recent-messages --account personal --limit 10
```

List local account readiness without calling Nylas:

```powershell
python -m aihub_email.cli list-accounts
```

Export recent message summaries to local JSON:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10 --export --ascii
```

Search the latest local export without calling Nylas:

```powershell
python -m aihub_email.cli search-exports --query security --limit 10 --ascii
```

Summarize the latest local export:

```powershell
python -m aihub_email.cli summarize-export --ascii
```

Refresh the local snapshot in one command:

```powershell
python -m aihub_email.cli refresh-snapshot --limit 10 --ascii
```

PowerShell wrappers are available for routine local use:

```powershell
.\scripts\list-accounts.ps1
.\scripts\refresh-snapshot.ps1 -Limit 10
.\scripts\search-exports.ps1 -Query security
.\scripts\refresh-all.ps1 -Limit 10
```

Build a live Inbox review for today's messages across all configured accounts:

```powershell
.\scripts\today-review.ps1
```

Add another connected Nylas account locally:

```powershell
.\scripts\add-account.ps1 -Account personal
.\scripts\check-config.ps1 -Account personal
.\scripts\refresh-snapshot.ps1 -Account personal -Limit 10
```

## Documentation

Architectural decisions are tracked in:

- `docs/adr/`

Delete operation rules are tracked in:

- `docs/delete-operations.md`

Common user workflows are documented in:

- `docs/common-workflows.md`

Assistant/Codex operating rules are documented in:

- `AGENTS.md`

Operational knowledge can live in a local Obsidian vault, but the reusable project source belongs in GitHub.
