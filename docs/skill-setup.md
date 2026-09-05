# Ben Mail Skill Setup

Ben Mail is intended to be used as a Codex skill by default.

The repo contains the implementation. The installed skill tells Codex how to operate that implementation.

## What Gets Installed

Source skill folder in the repo:

```text
skill\ben-mail
```

Installed skill folder:

```text
%USERPROFILE%\.codex\skills\ben-mail
```

If `CODEX_HOME` is set:

```text
%CODEX_HOME%\skills\ben-mail
```

The installed skill contains:

```text
SKILL.md
references\install-location.md
```

`install-location.md` points back to the local repo clone. This is how Codex knows where to run Ben Mail scripts.

## Install

From the repo root:

```powershell
.\install.ps1
```

To refresh only the skill:

```powershell
.\scripts\install-skill.ps1 -Force
```

## Verify

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\ben-mail\SKILL.md"
Get-Content "$env:USERPROFILE\.codex\skills\ben-mail\references\install-location.md"
```

The install location should match the user's local repo clone.

## Use

In Codex:

```text
$ben-mail check my emails from today
$ben-mail check the yahoo account for mail from today
$ben-mail delete all spam
```

## Important Behavior

Ben Mail should:

- run local scripts from the repo
- fetch fresh live data for current inbox questions
- avoid old exports unless explicitly asked
- build delete plans before deleting
- move messages to Trash by default
- keep `.env`, `exports`, and `reviews` private

## Do Not Share

Never share or commit:

- `.env`
- Nylas API keys
- Nylas Grant IDs
- `exports/`
- `reviews/`
- local Obsidian vault notes
