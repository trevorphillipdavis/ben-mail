# Ben Mail

Ben Mail is a local-first email automation project for reviewing and cleaning up multiple email accounts through Nylas.

It is designed as one modular AIHub capability project: reusable scripts do the deterministic work locally, while an AI assistant can reason over small review outputs and decide what to run next.

This repo installs Ben Mail as a local Codex skill named `ben-mail`, with display name `Ben`.

The `backend/` folder is experimental development work and is not required for the local Ben Mail skill setup.

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

## Clean Machine Setup

From PowerShell:

```powershell
git clone https://github.com/trevorphillipdavis/ben-mail.git
cd ben-mail
.\install.ps1
```

The installer:

- creates a local Python virtual environment
- installs Python dependencies
- creates `.env` from `.env.example` if needed
- installs the Codex skill from `skill\ben-mail`
- writes the repo path into the installed skill's `references\install-location.md`
- prompts for Nylas configuration and email account Grant IDs

After install, verify:

```powershell
.\scripts\list-accounts.ps1 -ReadyOnly
.\scripts\today-review.ps1
```

Expected installed skill location:

```text
%USERPROFILE%\.codex\skills\ben-mail
```

If `CODEX_HOME` is set, the skill is installed under:

```text
%CODEX_HOME%\skills\ben-mail
```

To refresh the skill after changing the repo:

```powershell
.\scripts\install-skill.ps1 -Force
```

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

Named accounts are supported through grant-specific environment variables. The setup scripts normalize account names into environment variable names.

```text
NYLAS_GRANT_ID_PERSONAL=
NYLAS_GRANT_ID_WORK=
NYLAS_GRANT_ID_GMAIL_PERSONAL=
NYLAS_GRANT_ID_YAHOO_PERSONAL=
```

Example:

```powershell
python -m aihub_email.cli list-recent-messages --account personal --limit 10
```

List local account readiness without calling Nylas:

```powershell
python -m aihub_email.cli list-accounts
```

Review only one account for today's Inbox mail:

```powershell
.\scripts\today-review.ps1 -Account yahoo_personal -Json
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

## Sharing This Repo

Share the GitHub repo only. Do not share:

- `.env`
- local exports under `exports/`
- local reviews under `reviews/`
- Obsidian vault contents
- Nylas API keys or Grant IDs

Each user needs their own:

- Codex app installed locally
- local clone of this repo
- Nylas account
- Nylas application credentials
- one Nylas Grant ID per connected email account

The normal user flow is:

```text
clone repo -> run .\install.ps1 -> connect Nylas accounts -> use $ben-mail in Codex
```
