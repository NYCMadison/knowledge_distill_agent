#!/usr/bin/env bash
# 从 GitHub 分支 cursor/-bc-08d79450-8ed3-4b8e-9c79-d4773bad7c10-8191
# 将「蒸馏产出_待归属」文件夹同步到本地 knowledge_distill_agent
# 用法: bash scripts/sync_distill_pending_from_github.sh
# 若报 index.lock 错误，先执行: rm -f .git/index.lock

set -e
BRANCH="origin/cursor/-bc-08d79450-8ed3-4b8e-9c79-d4773bad7c10-8191"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$REPO_ROOT"
rm -f .git/index.lock
echo "==> Fetching from origin..."
git fetch origin
echo "==> Checking out 蒸馏产出_待归属 from $BRANCH ..."
git checkout "$BRANCH" -- "蒸馏产出_待归属"
echo "==> Done. Files in 蒸馏产出_待归属: $(ls 蒸馏产出_待归属 2>/dev/null | wc -l)"
