# Setup From Scratch

This guide is for setting up the Ben Mail repo on a clean machine.

## 1. Clone The Repo

```powershell
git clone https://github.com/YOUR_USERNAME/ben-mail.git
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

The setup script prompts for:

- Nylas API key.
- Nylas API URI, defaulting to `https://api.us.nylas.com`.
- One or more account aliases.
- One Nylas Grant ID per account.

Never commit `.env`.

## 3. Connect Nylas Accounts

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

## 4. Verify Configuration

```powershell
.\scripts\list-accounts.ps1 -ReadyOnly
.\scripts\check-config.ps1 -Account gmail_personal
```

## 5. Run A Read-Only Review

```powershell
.\scripts\today-review.ps1
```

Review files are written under `reviews/`, which is ignored by Git.

## 6. Run Tests

```powershell
python -m pytest
```

## Sharing Notes

Share the GitHub repo, not your `.env`, `exports/`, `reviews/`, or Obsidian vault.

Each user should create their own Nylas app credentials and Grant IDs.

## Optional Codex Skill

This repo can be operated directly with scripts, or wrapped by a local Codex skill. The normal install path installs the skill automatically.

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
