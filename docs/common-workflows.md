# Common Workflows

Run commands from the repo root.

```powershell
cd C:\Users\trevo\Dropbox\GitHub\ben-mail
```

For a different user, replace that path with their local clone path.

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

Review one account only:

```powershell
.\scripts\today-review.ps1 -Account yahoo_personal -Json
```

The review uses live provider data and writes a local JSON review under `reviews\YYYY-MM-DD\`.

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

Delete jobs should use the timing budget:

```text
initial_check_delay = number_of_messages * 5 seconds
follow_up_check_delay = 60 seconds
```

## Share Or Install Ben Mail For Another User

Give the user the GitHub repo and have them run:

```powershell
git clone https://github.com/trevorphillipdavis/ben-mail.git
cd ben-mail
.\install.ps1
```

They must provide their own Nylas API key and Grant IDs.

Do not share local `.env`, `exports`, `reviews`, or Obsidian vault files.

## Python Helper

PowerShell wrappers call:

```powershell
.\scripts\python.ps1
```

This helper chooses the repo `.venv` Python when available, then falls back to system Python. It is intended for normal Python arguments such as `-m aihub_email.cli ...`; do not pipe inline scripts into this helper.
