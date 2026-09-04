---
name: ben-mail
description: Use the local AIHub email-integration repo to review inboxes, manage Nylas-connected email accounts, build delete plans, and remove spam with safe move-to-Trash workflows.
---

# Ben

Use this skill when the user asks to check, review, search, summarize, clean up, or delete email using the AIHub email integration.

The implementation repo is the clone that installed this skill. By default, the installer writes the clone path into `references/install-location.md`.

## Operating Model

- Prefer deterministic local scripts and Python commands from the repo before reasoning over raw email data.
- Keep token use low by saving provider results locally and summarizing only the needed fields.
- Treat `.env`, `exports/`, and `reviews/` as local/private data. Never print secrets from `.env`.
- Do not commit or push changes unless the user explicitly asks.
- Nylas is the current email provider boundary.

## Finding The Repo

Read `references/install-location.md` when you need the exact local repo path. If that file is missing, ask the user where they cloned `email-integration`.

Run commands from the repo root.

## Common Commands

```powershell
.\scripts\setup.ps1
.\scripts\list-accounts.ps1 -ReadyOnly
.\scripts\today-review.ps1
.\scripts\refresh-snapshot.ps1 -Account gmail_personal -Limit 50
.\scripts\search-exports.ps1 -Account gmail_personal -Query security
python -m aihub_email.cli review-inbox --account gmail_personal --days 7
python -m aihub_email.cli execute-delete-plan --plan <plan.json> --yes-trash
```

Use `python -m pytest` after changing repo code.

## Freshness Rule

For current inbox questions, fetch live data. Do not rely on old `exports/` or `reviews/` unless the user explicitly asks to inspect an earlier saved run.

Today reviews should use live Inbox-only, non-Trash data. If the browser UI and Nylas disagree, verify exact message IDs and folder labels before taking action.

## Delete Safety

Default delete behavior is move to Trash, not permanent deletion.

Before live delete actions:

- Build an exact local delete plan with account, message ID, sender, subject, and reason.
- Preserve the plan under `reviews/`.
- Confirm the scope when the instruction is ambiguous or broad.
- Do not start overlapping delete jobs for the same mailbox.

For every delete batch:

```text
initial_check_delay = number_of_messages * 5 seconds
follow_up_check_delay = 60 seconds
```

After starting a delete batch, wait for the initial budget before checking progress unless the user asks for immediate status. If still running, check every 60 seconds.

## Protected Messages

Keep these by default, even if the sender is automated or the message appears in Gmail Updates:

- Tax, legal, insurance, and document-signature messages.
- Bills, invoices, statements, payment due notices, and transaction alerts.
- Account security, login, authentication, password, and app-password notices.
- Known human/vendor correspondence.

Only include protected messages in a delete plan when the user explicitly identifies the exact message, sender, or domain as unwanted.

## Spam Cleanup

When the user asks to delete or remove all spam:

- Load `config/spam-auto-delete.yaml`.
- Match current emails by `auto_delete_domains` and `auto_delete_senders`.
- Build a delete plan from matching emails.
- Move matching emails to Trash.

Keep building `config/spam-auto-delete.yaml` over time when the user approves additional spam senders or domains. Use exact senders for shared providers such as `outlook.com`, `gmail.com`, `yahoo.com`, and `hotmail.com`.

## Useful Docs

Project docs:

```text
docs\setup-from-scratch.md
docs\common-workflows.md
docs\delete-operations.md
```
