# Setup From Scratch

This guide is for setting up the Ben Mail repo on a clean machine.

The supported default setup is:

```text
GitHub repo clone -> local install script -> local Codex skill -> local Nylas-connected email actions
```

The `backend/` folder is not required for this setup.

## 1. Clone The Repo

```powershell
git clone https://github.com/YOUR_USERNAME/ben-mail.git
cd ben-mail
```

For Trevor's canonical repo:

```powershell
git clone https://github.com/trevorphillipdavis/ben-mail.git
cd ben-mail
```

## 2. Create Local Environment

```powershell
.\install.ps1
```

The installer:

- Creates the local Python environment.
- Installs the `ben-mail` Codex skill into the user's local Codex skills folder.
- Runs the setup script.
- Copies `skill\ben-mail` to the local Codex skills directory.
- Records this repo path in the installed skill so Codex knows where to run commands.

The setup script prompts for:

- Nylas API key.
- Nylas API URI, defaulting to `https://api.us.nylas.com`.
- One or more account aliases.
- One Nylas Grant ID per account.

Never commit `.env`.

## 3. Confirm Skill Installation

The installed skill should exist at:

```text
%USERPROFILE%\.codex\skills\ben-mail\SKILL.md
```

If `CODEX_HOME` is set, use:

```text
%CODEX_HOME%\skills\ben-mail\SKILL.md
```

The installed file:

```text
references\install-location.md
```

should point back to the repo clone.

Refresh the local skill after repo changes:

```powershell
.\scripts\install-skill.ps1 -Force
```

## 4. Connect Nylas Accounts

Create a Nylas application, connect each email account, and copy each Grant ID into `.env`.

For the first/default account:

```text
NYLAS_GRANT_ID=
```

For named accounts:

```text
NYLAS_GRANT_ID_GMAIL_PERSONAL=
NYLAS_GRANT_ID_WORK=
NYLAS_GRANT_ID_YAHOO_PERSONAL=
```

Named account IDs are normalized. For example, this setup prompt value:

```text
gmail_personal
```

creates or updates:

```text
NYLAS_GRANT_ID_GMAIL_PERSONAL=
```

You can also add accounts later with:

```powershell
.\scripts\add-account.ps1 -Account gmail_personal
```

## 5. Verify Configuration

```powershell
.\scripts\list-accounts.ps1 -ReadyOnly
.\scripts\check-config.ps1 -Account gmail_personal
```

## 6. Run A Read-Only Review

```powershell
.\scripts\today-review.ps1
```

Review files are written under `reviews/`, which is ignored by Git.

Review a single account:

```powershell
.\scripts\today-review.ps1 -Account yahoo_personal -Json
```

## 7. Run Tests

```powershell
python -m pytest
```

## Operating Rules

Ben Mail should prefer local scripts for deterministic work:

- account setup
- live message fetches
- export creation
- searching local exports
- delete plan execution
- spam rule matching

AI should be used for judgment calls:

- whether an email appears action-worthy
- whether a sender/domain should be added to spam rules
- whether a message is protected and should be kept

## Delete Safety

Deletes mean "move to Trash" by default.

Before deleting, Ben Mail should create a JSON delete plan under `reviews/` containing:

- account ID
- message ID
- sender
- subject
- reason

For delete jobs, use this timing rule:

```text
initial_check_delay = number_of_messages * 5 seconds
follow_up_check_delay = 60 seconds
```

## Protected Messages

Keep these by default:

- tax, legal, insurance, document-signature messages
- bills, invoices, statements, payment due notices, transaction alerts
- login, password, authentication, app-password, and security notices
- known human/vendor correspondence

Only delete protected messages when the user explicitly identifies the exact message, sender, or domain as unwanted.

## Spam Rules

Approved spam senders and domains live in:

```text
config\spam-auto-delete.yaml
```

Use full domains for spam-only domains. For shared providers like Gmail, Outlook, Yahoo, and Hotmail, use exact senders instead of whole domains.

## Sharing Notes

Share the GitHub repo, not your `.env`, `exports/`, `reviews/`, or Obsidian vault.

Each user should create their own Nylas app credentials and Grant IDs.

## Codex Skill

The default way to use Ben Mail from Codex is through the local `ben-mail` skill.

By default, the installer copies the skill source from:

```text
skill\ben-mail
```

to:

```text
$env:CODEX_HOME\skills\ben-mail
```

If `CODEX_HOME` is not set, it uses:

```text
~\.codex\skills\ben-mail
```

The skill is only an operating guide for Codex. The repo remains the reusable implementation.

To install or refresh only the skill:

```powershell
.\scripts\install-skill.ps1 -Force
```

Then invoke it in Codex with:

```text
$ben-mail check my emails from today
```

or:

```text
$ben-mail delete all spam
```
