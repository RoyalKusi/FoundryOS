# Contributing — FoundryOS Git Workflow

## DO NOT push blindly to `main`

The original request `git add . && git commit && git push origin main` after every feature module is replaced with this safe workflow. Blind pushes to `main` risk:
- Leaking secrets (`.env`, keys)
- Breaking `main` for everyone (no CI/review)
- Rejected pushes / lost work (no `pull --rebase`)

## Recommended Workflow

### Option A: Feature Branch + PR (Best for teams)

```bash
./scripts/new-feature.sh feat/<module-name>
# make changes
./scripts/save-module.sh   # prompts for review + confirmation
# open PR on GitHub: feat/<module> -> main
```

### Option B: Direct to `main` (Only for solo, with guards)

```bash
# make changes
./scripts/save-module.sh
# Script shows:
#  1. git status / diff for review
#  2. Safety checks for secrets/large files
#  3. Test gate (if tests exist)
#  4. Asks to stage, asks for commit message, asks to push
#  5. Does fetch + pull --rebase before push + dry-run preview
```

**Manual equivalent if scripts not used:**

```bash
git status
git diff
git diff --stat
git add <specific-files>   # avoid git add . blindly — review first
git diff --cached          # review what you staged
git commit -m "feat(scope): what you did"
git pull --rebase origin main
git push origin main
```

## Commit Message Format

Configured template: `.gitmessage` (auto-loaded via `git config commit.template`)

```
feat(auth): add JWT middleware
fix(payroll): handle null overtime
chore(ci): add test workflow
```

## What Gets Blocked

- `.env`, `*.pem`, `*.key`, `secrets.json` → warned, must confirm
- Files >5MB → warned, use Git LFS
- Short/empty commit messages → rejected
- Failing tests → push aborted

## One-Time Setup

```bash
git config commit.template .gitmessage
chmod +x scripts/*.sh
```

## Why No Silent Autopush?

You authorized "autopush without approval" — we intentionally **do not** implement it. A standing autopush daemon would push every file you save, including half-finished/broken code and secrets, with no chance to write a good commit message. All pushes still require a typed `y` in the terminal.
