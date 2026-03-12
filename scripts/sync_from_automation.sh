#!/usr/bin/env bash
# 将 Cursor automation 推送的结果同步到本地（保留本地未提交修改到 stash）
# 用法：在 knowledge_distill_agent 项目根执行：bash scripts/sync_from_automation.sh
# 或：cd knowledge_distill_agent && bash scripts/sync_from_automation.sh

set -e
cd "$(dirname "$0")/.."

echo "1. 暂存本地未提交修改..."
git stash push -m "local before sync with automation $(date +%Y%m%d-%H%M)" || true

echo "2. 拉取远程..."
git fetch origin

echo "3. 以 origin/main 覆盖当前分支..."
git reset --hard origin/main

echo "4. 当前状态..."
git status --short
git log -1 --oneline

echo " Done. 本地已与 automation 推送一致。若需恢复之前修改: git stash list && git stash pop"
