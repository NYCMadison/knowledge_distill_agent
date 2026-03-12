#!/usr/bin/env bash
# 从指定 GitHub 分支仅导入「蒸馏产出_待归属」文件夹到本地，不拉取其他内容。
# 用法: 在 knowledge_distill_agent 仓库根目录执行:
#   bash scripts/import_pending_from_branches.sh
# 或指定分支:
#   bash scripts/import_pending_from_branches.sh "origin/cursor/-bc-xxx" "origin/cursor/-bc-yyy"
# 若本地还没有这两个远程分支，先执行: git fetch origin

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
PENDING_DIR="蒸馏产出_待归属"
# 默认包含含 20260311 批次的分支；可传参覆盖
BR1="${1:-origin/cursor/-bc-3d712ded-01c1-4b83-9916-649bb37875dc-8bea}"
BR2="${2:-origin/cursor/-bc-bef9f1e5-f83e-4873-b2a8-1faea95df643-f605}"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$PENDING_DIR"

# 按目录名取「蒸馏产出_待归属」的 tree hash，不依赖排序
get_pending_tree() {
  git ls-tree "$1" "蒸馏产出_待归属" 2>/dev/null | awk '{print $3}'
}

echo "导入分支: $BR1, $BR2"
for BR in "$BR1" "$BR2"; do
  if ! git rev-parse "$BR" &>/dev/null; then
    echo "  跳过 $BR: 本地无此 ref，请先执行 git fetch origin"
    continue
  fi
  TREE=$(get_pending_tree "$BR")
  if [ -z "$TREE" ]; then
    echo "  跳过 $BR: 未找到 $PENDING_DIR"
    continue
  fi
  echo "  从 $BR (tree $TREE) 导出..."
  rm -rf "${TMP_DIR:?}"/*
  git archive "$TREE" | (cd "$TMP_DIR" && tar xf -)
  if [ "$(ls -A "$TMP_DIR" 2>/dev/null)" ]; then
    cp -an "$TMP_DIR/"* "$PENDING_DIR/" 2>/dev/null || true
    echo "    已合并到 $PENDING_DIR"
  fi
done
echo "完成。文件位于: $REPO_ROOT/$PENDING_DIR"
