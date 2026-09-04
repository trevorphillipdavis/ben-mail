# Delete Operations

Email delete operations affect live mailboxes and must be handled carefully.

## Delete Mode

Move messages to Trash by default.

Do not hard delete messages unless that behavior is explicitly requested and separately confirmed.

## Confirmation

Before executing a delete plan:

- Build an exact local delete plan.
- Include account ID, message ID, sender, subject, and reason.
- Get explicit user confirmation for the exact plan.

## Protected Messages

Keep these messages by default, even if the sender is automated or the message appears in Gmail Updates:

- Tax, legal, insurance, and document-signature messages.
- Bills, invoices, statements, payment due notices, and transaction alerts.
- Account security, login, authentication, and password/app-password notices.
- Known human/vendor correspondence.

Only include a protected message in a delete plan when the user explicitly identifies that exact message or sender as unwanted.

## Spam Auto-Delete Rules

When the user asks to delete or remove all spam, use `config/spam-auto-delete.yaml` as the local source of truth for accumulated spam senders/domains and include matching emails in the delete plan.

Keep building this list over time when the user approves additional spam senders or domains.

- `auto_delete_domains` is for clearly disposable or spam-only domains.
- `auto_delete_senders` is for exact addresses, especially when the domain is shared or public.
- Do not block entire shared providers such as `outlook.com`, `gmail.com`, `yahoo.com`, or `hotmail.com`.
- Do not include `juppiterailabs.com` unless the user explicitly changes that decision.

## Runtime Check Budget

For all email delete batches, use this progress-check rule:

```text
initial_check_delay = number_of_messages * 5 seconds
follow_up_check_delay = 60 seconds
```

After starting a delete batch:

1. Calculate the initial check delay using 5 seconds per email.
2. Do not check the process before that delay unless the user asks for an immediate status update.
3. If the process is still running at the initial check, check again every 60 seconds.
4. Do not start overlapping delete jobs for the same mailbox.

This keeps progress monitoring predictable and avoids unnecessary token use during long provider-side delete batches.
