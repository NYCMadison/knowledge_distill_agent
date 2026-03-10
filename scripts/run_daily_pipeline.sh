#!/usr/bin/env bash
set -euo pipefail

# Daily automation entrypoint:
# - always use one long-lived branch
# - collect sources
# - distill batch
# - commit distilled outputs
# - push to remote

LONG_BRANCH="${LONG_BRANCH:-bot/daily-distill}"
DISTILL_TARGET="${DISTILL_TARGET:-100}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python interpreter not found: $PYTHON_BIN" >&2
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "[1/6] Ensure long-lived branch: $LONG_BRANCH"
git fetch origin
if git show-ref --verify --quiet "refs/heads/$LONG_BRANCH"; then
  git checkout "$LONG_BRANCH"
elif git ls-remote --exit-code --heads origin "$LONG_BRANCH" >/dev/null 2>&1; then
  git checkout -b "$LONG_BRANCH" --track "origin/$LONG_BRANCH"
else
  git checkout -b "$LONG_BRANCH"
fi

if git ls-remote --exit-code --heads origin "$LONG_BRANCH" >/dev/null 2>&1; then
  git pull --ff-only origin "$LONG_BRANCH"
fi

echo "[2/6] Collect sources"
"$PYTHON_BIN" scripts/collect_sources.py

echo "[3/6] Distill batch target=$DISTILL_TARGET"
"$PYTHON_BIN" scripts/distill_run.py --target "$DISTILL_TARGET"

echo "[4/6] Stage distilled outputs"
git add distill_input_history.json "蒸馏产出_待归属"

echo "[5/6] Commit if there are staged changes"
if git diff --cached --quiet; then
  echo "No staged changes; skip commit."
else
  commit_date="$(date +%F)"
  git commit -m "chore: daily distill outputs $commit_date"
fi

echo "[6/6] Push branch $LONG_BRANCH"
git push -u origin "$LONG_BRANCH"

echo "Done."
