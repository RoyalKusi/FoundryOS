#!/usr/bin/env bash
set -euo pipefail

# save-module.sh — Safe alternative to blind "git add . && commit && push origin main"
# Requires explicit confirmation before staging/committing/pushing.
# Usage: ./scripts/save-module.sh

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
REMOTE="origin"
TARGET="main"

echo "=== FoundryOS Safe Save ==="
echo "Branch: $BRANCH"
echo "Remote: $REMOTE/$TARGET"
echo ""

# 1. Show current state - you MUST review this
echo "--- git status ---"
git status --short
echo ""
echo "--- git status (verbose) ---"
git status
echo ""

# Early exit if clean
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "Working tree clean — nothing to save."
  exit 0
fi

echo "--- Unstaged diff stat ---"
git diff --stat || true
echo ""
echo "--- Staged diff stat ---"
git diff --cached --stat || true
echo ""
echo "--- Untracked files ---"
git ls-files --others --exclude-standard || true
echo ""

# 2. Secret / large file guard
echo "--- Safety checks ---"
BLOCKED=0
# Check for .env or key files staged/unstaged
if git ls-files --others --exclude-standard | grep -qE "^\.env(\.|$)"; then
  echo "⚠️  WARNING: Untracked .env file detected. Ensure .gitignore covers it."
  BLOCKED=1
fi
if git status --porcelain | grep -qE "\.pem|\.key|secrets\.json"; then
  echo "⚠️  WARNING: Potential secret file (.pem/.key/secrets.json) in changes. Review carefully!"
  BLOCKED=1
fi
# Large files >5MB
LARGE_FILES=$(find . -type f -size +5M -not -path "./.git/*" 2>/dev/null | head -n 10 || true)
if [ -n "$LARGE_FILES" ]; then
  echo "⚠️  WARNING: Large files >5MB detected:"
  echo "$LARGE_FILES"
  echo "Consider Git LFS or adding to .gitignore"
  BLOCKED=1
fi
if [ "$BLOCKED" -eq 1 ]; then
  echo "Resolve warnings before continuing or confirm you intend to commit them."
fi
echo ""

# 3. Optional test gate - runs if test command exists
if [ -f "package.json" ] && grep -q '"test"' package.json 2>/dev/null; then
  echo "--- Test gate: npm test detected ---"
  read -p "Run tests before commit? (Y/n): " RUN_TEST
  RUN_TEST=${RUN_TEST:-Y}
  if [[ "$RUN_TEST" =~ ^[Yy]$ ]]; then
    npm test || { echo "❌ Tests failed — aborting. Fix before pushing to main."; exit 1; }
  fi
  echo ""
fi
if [ -f "Makefile" ] && grep -q "^test:" Makefile 2>/dev/null; then
  echo "--- Test gate: make test detected ---"
  read -p "Run 'make test' before commit? (Y/n): " RUN_TEST2
  RUN_TEST2=${RUN_TEST2:-Y}
  if [[ "$RUN_TEST2" =~ ^[Yy]$ ]]; then
    make test || { echo "❌ Tests failed — aborting."; exit 1; }
  fi
  echo ""
fi

# 4. Stage step - requires explicit approval
echo "--- Staging ---"
if ! git diff --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "Changes not yet staged:"
  git diff --name-only
  git ls-files --others --exclude-standard | sed 's/^/  (untracked) /'
  echo ""
  read -p "Stage ALL changes (git add -A)? Review first! (y/N): " DO_ADD
  if [[ "$DO_ADD" =~ ^[Yy]$ ]]; then
    echo "Running: git add -A"
    git add -A
  else
    echo "Skipped staging. Use 'git add <file>' manually, then re-run this script."
    echo "Preview staged diff:"
    git diff --cached --stat || echo "(nothing staged)"
    exit 0
  fi
fi

echo ""
echo "--- Staged for commit ---"
git diff --cached --stat
echo ""
echo "--- Staged diff preview ---"
git diff --cached | head -n 200
echo ""
if git diff --cached --quiet; then
  echo "Nothing staged — aborting."
  exit 0
fi

# 5. Commit message - requires human input
echo "--- Commit message ---"
echo "Use Conventional Commits: feat|fix|chore|docs|refactor|test(scope): description"
read -p "Commit message: " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
  echo "Commit message cannot be empty — aborting."
  exit 1
fi
# Basic validation
if [ ${#COMMIT_MSG} -lt 10 ]; then
  echo "Message too short (<10 chars). Please write a meaningful message."
  exit 1
fi

echo ""
echo "Ready to commit as:"
echo "  $COMMIT_MSG"
read -p "Create commit? (y/N): " DO_COMMIT
if [[ ! "$DO_COMMIT" =~ ^[Yy]$ ]]; then
  echo "Aborted commit."
  exit 0
fi

git commit -m "$COMMIT_MSG"

echo ""
echo "✅ Committed: $(git log -1 --oneline)"

# 6. Sync with remote before push - prevents rejected pushes
echo ""
echo "--- Syncing with $REMOTE/$TARGET ---"
git fetch "$REMOTE"
if ! git merge-base --is-ancestor "$REMOTE/$TARGET" HEAD 2>/dev/null; then
  echo "Local main has diverged or is behind. Attempting rebase..."
  git pull --rebase "$REMOTE" "$TARGET" || {
    echo "❌ Rebase failed — resolve conflicts then run: git push"
    exit 1
  }
fi

# 7. Final push confirmation - NEVER silent
echo ""
echo "--- Push preview (dry-run) ---"
git push --dry-run "$REMOTE" "$BRANCH" 2>&1 || true
echo ""
echo "You are about to push to $REMOTE/$BRANCH"
read -p "Push to $REMOTE $BRANCH now? (y/N): " DO_PUSH
if [[ "$DO_PUSH" =~ ^[Yy]$ ]]; then
  git push "$REMOTE" "$BRANCH"
  echo "🚀 Pushed to $REMOTE/$BRANCH"
else
  echo "Commit created locally but NOT pushed. Run 'git push' when ready."
fi
