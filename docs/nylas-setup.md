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
```

Do not commit `.env`.

## Local Execution

The project should favor local scripts for deterministic work. AI should be used to reason about intent, review results, and decide next actions, while routine execution happens through commands in this repository.

Check local configuration with:

```powershell
$env:PYTHONPATH = "services/email-service/src"
python -m aihub_email.cli check-config
```

## Read-Only First Milestone

The first implemented command should list recent messages for a configured grant.

It should:

- Use `NYLAS_API_KEY`, `NYLAS_API_URI`, and `NYLAS_GRANT_ID`.
- Call only read endpoints.
- Limit response size.
- Map provider response data into Email capability models.
- Avoid send, draft, delete, update, archive, or label operations.

## References

- Nylas Authentication: https://developer.nylas.com/docs/v3/auth/
- Nylas Email API: https://developer.nylas.com/docs/v3/email/
- Nylas Messages API: https://developer.nylas.com/docs/v3/email/messages/
