# Nylas Setup

This project uses Nylas v3 for the Email capability.

## Current Scope

The current milestone is read-only setup:

- Document the Nylas configuration shape.
- Define local environment variable names.
- Define the provider boundary.
- Avoid live API calls until authentication and secrets handling are approved.

## Nylas Concepts

Nylas v3 uses OAuth 2.0 to create grants. A grant represents an authenticated user connection, and API calls that access user data require a `grant_id`.

Messages are available through the Nylas Messages API under grant-scoped endpoints.

## Local Environment

Copy `.env.example` to `.env` and fill values locally:

```text
NYLAS_API_KEY=
NYLAS_API_URI=https://api.us.nylas.com
NYLAS_GRANT_ID=
AIHUB_ENV=local

NYLAS_GRANT_ID_PERSONAL=
NYLAS_GRANT_ID_WORK=
```

Do not commit `.env`.

## Local Execution

The project should favor local scripts for deterministic work. AI should be used to reason about intent, review results, and decide next actions, while routine execution happens through commands in this repository.

Check local configuration with:

```powershell
python -m aihub_email.cli check-config
```

The CLI loads `.env` by default. To use another local file:

```powershell
python -m aihub_email.cli --env-file path\to\.env check-config
```

Check a named account with:

```powershell
python -m aihub_email.cli check-config --account personal
```

List local account readiness without making Nylas API calls:

```powershell
python -m aihub_email.cli list-accounts
```

## Read-Only Command

List recent messages with:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10
```

List messages for a named account with:

```powershell
python -m aihub_email.cli list-recent-messages --account personal --limit 10
```

For structured output:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10 --json
```

If the Windows console displays unusual characters, use ASCII-safe output:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10 --ascii
```

Export a local JSON snapshot:

```powershell
python -m aihub_email.cli list-recent-messages --limit 10 --export --ascii
```

Exports are written under `exports/` by default and are ignored by Git.

Search the latest local export without making another Nylas API call:

```powershell
python -m aihub_email.cli search-exports --query security --limit 10 --ascii
```

Summarize the latest local export:

```powershell
python -m aihub_email.cli summarize-export --ascii
```

Fetch, export, and summarize in one local workflow:

```powershell
python -m aihub_email.cli refresh-snapshot --limit 10 --ascii
```

PowerShell wrappers are available under `scripts/`:

```powershell
.\scripts\list-accounts.ps1
.\scripts\refresh-snapshot.ps1 -Limit 10
.\scripts\search-exports.ps1 -Query security
.\scripts\refresh-all.ps1 -Limit 10
```

## Add More Mailboxes

For each mailbox:

1. Connect the mailbox in the Nylas dashboard.
2. Copy the new Grant ID.
3. Register it locally with a stable account alias.

```powershell
.\scripts\add-account.ps1 -Account personal
.\scripts\check-config.ps1 -Account personal
.\scripts\refresh-snapshot.ps1 -Account personal -Limit 10
```

Use lowercase account aliases such as:

```text
personal
work
rentals
business
```

The script stores the grant in `.env` as `NYLAS_GRANT_ID_<ACCOUNT>`. The `.env` file remains local and is ignored by Git.

## Read-Only Boundaries

The current command:

- Use `NYLAS_API_KEY`, `NYLAS_API_URI`, and `NYLAS_GRANT_ID`.
- Call only read endpoints.
- Limit response size.
- Map provider response data into Email capability models.
- Avoid send, draft, delete, update, archive, or label operations.

The CLI returns readable local errors for:

- Missing local configuration.
- Invalid message limits.
- Bad API keys.
- Missing or revoked grants.
- Rate limits.
- Network failures.

## References

- Nylas Authentication: https://developer.nylas.com/docs/v3/auth/
- Nylas Email API: https://developer.nylas.com/docs/v3/email/
- Nylas Messages API: https://developer.nylas.com/docs/v3/email/messages/
