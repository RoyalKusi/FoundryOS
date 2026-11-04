#!/usr/bin/env bash
set -euo pipefail

# new-feature.sh — Recommended workflow: push to feature branch + PR, NOT directly to main
# Usage: ./scripts/new-feature.sh feat/my-module

if [ $# -lt 1 ]; then
  echo "Usage: $0 <branch-name>"
  echo "Example: $0 feat/hr-module"
  exit 1
fi

BRANCH_NAME="$1"
if [[ ! "$BRANCH_NAME" =~ ^(feat|fix|chore|docs)/ ]]; then
  echo "Branch name should start with feat/, fix/, chore/, or docs/"
  echo "You gave: $BRANCH_NAME"
  read -p "Continue anyway? (y/N): " CONF
  if [[ ! "$CONF" =~ ^[Yy]$ ]]; then exit 1; fi
fi

echo "=== Creating feature branch: $BRANCH_NAME ==="
git fetch origin
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  echo "Branch $BRANCH_NAME already exists locally. Checking out."
  git checkout "$BRANCH_NAME"
else
  git checkout -b "$BRANCH_NAME" origin/main
fi

echo ""
git status --short
echo ""
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "No changes to commit on new branch. Make changes then use ./scripts/save-module.sh"
  exit 0
fi

echo "Changes detected. Run ./scripts/save-module.sh to commit safely."
echo "When ready, this branch will push to origin/$BRANCH_NAME for PR review."
read -p "Run save-module.sh now? (y/N): " RUN_SAVE
if [[ "$RUN_SAVE" =~ ^[Yy]$ ]]; then
  ./scripts/save-module.sh
else
  echo "Next steps:"
  echo "  1. git add -A (after reviewing)"
  echo "  2. git commit -m 'feat: ...'"
  echo "  3. git push -u origin $BRANCH_NAME"
  echo "  4. Open PR from $BRANCH_NAME -> main on GitHub"
fi
