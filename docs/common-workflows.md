# Common Workflows

## Add An Account

```powershell
.\scripts\add-account.ps1 -Account gmail_personal
.\scripts\check-config.ps1 -Account gmail_personal
```

## List Ready Accounts

```powershell
.\scripts\list-accounts.ps1 -ReadyOnly
```

## Review Today's Inbox

```powershell
.\scripts\today-review.ps1
```

This performs a fresh live Inbox review across configured accounts.

## Refresh A Single Account Snapshot

```powershell
.\scripts\refresh-snapshot.ps1 -Account gmail_personal -Limit 50
```

## Search Local Exports

```powershell
.\scripts\search-exports.ps1 -Account gmail_personal -Query security
```

## Review Inbox For Non-Bulk Messages

```powershell
python -m aihub_email.cli review-inbox --account gmail_personal --days 7
```

## Maintain Spam Auto-Delete Rules

Approved spam senders and domains live in:

```text
config/spam-auto-delete.yaml
```

Use domains only for clearly disposable or spam-only domains. Use exact senders for shared providers such as Outlook, Gmail, Yahoo, and Hotmail.

## Delete All Spam

When asked to delete all spam, use `config/spam-auto-delete.yaml` to build a delete plan, then move matching messages to Trash.

Do not hard delete unless explicitly requested.

## Python Helper

PowerShell wrappers call:

```powershell
.\scripts\python.ps1
```

This helper chooses the repo `.venv` Python when available, then falls back to system Python. It is intended for normal Python arguments such as `-m aihub_email.cli ...`; do not pipe inline scripts into this helper.
