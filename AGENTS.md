# AIHub Email Integration Agent Instructions

This repository is a local-first email automation project.

## Core Rules

- Prefer local scripts and deterministic execution before asking an AI model to inspect raw email data.
- Never print, commit, summarize, or store secrets from `.env`.
- Treat exports and reviews as local working data. They are ignored by Git and should not be shared.
- Use Nylas as the provider boundary unless the project explicitly adds another provider.
- Move messages to Trash by default. Do not permanently delete messages unless the user explicitly requests that exact behavior.
- Build exact delete plans before live delete actions.
- Confirm account, sender, subject, and count before deleting unless the user has already given an exact instruction using an existing generated plan.

## Delete Timing

For every delete action:

```text
initial_check_delay = number_of_messages * 5 seconds
follow_up_check_delay = 60 seconds
```

After starting a delete batch, wait for the initial budget before checking progress. If the batch is still running, check every 60 seconds. Do not start overlapping delete jobs for the same mailbox.

## Spam Cleanup

When the user asks to delete or remove all spam:

- Load `config/spam-auto-delete.yaml`.
- Match emails by `auto_delete_domains` and `auto_delete_senders`.
- Build a local delete plan from matching emails.
- Execute the plan by moving messages to Trash.

Keep building this spam list over time when the user approves additional spam senders or domains.

## Protected Messages

Keep these messages by default:

- Tax, legal, insurance, and document-signature messages.
- Bills, invoices, statements, payment due notices, and transaction alerts.
- Account security, login, authentication, password, and app-password notices.
- Known human/vendor correspondence.

Only include protected messages in a delete plan when the user explicitly identifies the exact message, sender, or domain as unwanted.
