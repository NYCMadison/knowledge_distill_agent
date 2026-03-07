#!/usr/bin/env python
"""
从 蒸馏产出_待归属 识别每个知识文件，按 归属匹配规则.json 分配到知识库，生成迁移映射并可选执行迁移。
约定见 蒸馏归属目标.md。匹配逻辑在 config/归属匹配规则.json，可单独编辑。

步骤：
  1. 扫描 待归属 下 .md，解析 标题、类型、主题标签
  2. 按规则文件顺序做关键词匹配，得到 target_key
  3. 生成 迁移映射_YYYYMMDD.csv（目标文件名：YYYYMMDD_主题简述_类型.md）
  4. 若加 --migrate则执行迁移（复制到 about_* 并删除待归属内源文件）

用法：
  python assign_and_migrate.py                    # 仅生成映射 CSV，不迁移
  python assign_and_migrate.py --migrate          # 生成映射并执行迁移
  python assign_and_migrate.py --dry-run          # 仅打印映射，不写 CSV 不迁移
  python assign_and_migrate.py --batch 20260210   # 只处理 20260210_distill_*.md
"""
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# 项目根（可由 DISTILL_PROJECT_ROOT 指定，适用于线上/云环境）
KB_DISTILL = Path(os.environ.get("DISTILL_PROJECT_ROOT", "")).expanduser() if os.environ.get("DISTILL_PROJECT_ROOT") else SCRIPT_DIR.parent
# 迁移目标知识库根：必须由环境变量 KB_VENTURE 提供，不依赖本地路径
_kb = os.environ.get("KB_VENTURE")
if not _kb:
    print("错误：请设置环境变量 KB_VENTURE（知识库根路径）。", file=sys.stderr)
    sys.exit(1)
KB = Path(_kb).expanduser()
PENDING = KB_DISTILL / "蒸馏产出_待归属"
RULES_PATH = KB_DISTILL / "config" / "归属匹配规则.json"

# 与 蒸馏归属目标.md 一致，须与 migrate_by_csv.py TARGET_DIRS 对齐
TARGET_DIRS = {
    "INDUSTRY": KB / "about_industry_analysis" / "所有产业链框架汇总",
    "STARTUP": KB / "about_startup",
    "FINANCIALS": KB / "about_financials",
    "ENERGY_STORAGE": KB / "about_energy_storage",
    "CRISIS_MANAGEMENT": KB / "about_crisis_management",
    "MARKETING": KB / "about_marketing",
    "PRODUCT_DEVELOPMENT": KB / "about_product_development",
    "KNOWLEDGE_LOGIC": KB / "about_knowledge_logic",
    "QUANT_ANALYSIS": KB / "about_quant_analysis",
}


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(KB))
    except ValueError:
        return str(p)


def parse_frontmatter(content: str) -> tuple[str, str, str]:
    """从正文前若干行解析 标题、类型、主题标签。返回 (标题, 类型, 主题标签拼接)。"""
    title, typ, tags = "", "", ""
    for line in content.splitlines()[:35]:
        if line.startswith("标题："):
            title = line.replace("标题：", "").strip()
        elif line.startswith("类型："):
            typ = line.replace("类型：", "").strip()
        elif line.startswith("主题标签："):
            tags = line.replace("主题标签：", "").strip()
    return title, typ or "框架", tags


def sanitize_basename(s: str, max_len: int = 55) -> str:
    """生成可作文件名的短串：去掉非法字符、截断长度。"""
    s = re.sub(r'[\\/:*?"<>|]', "_", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s or "未命名"


def assign_target(search_text: str, rules: list[dict]) -> str:
    """按规则顺序匹配，返回 target_key。空关键词的规则作为默认，仅当无其他规则命中时使用。"""
    search_lower = search_text.lower()
    default = "INDUSTRY"
    for rule in rules:
        kws = rule.get("keywords") or []
        if not kws:
            default = rule["target"]
            continue
        if any(kw in search_text or kw in search_lower for kw in kws):
            return rule["target"]
    return default


def main():
    dry_run = "--dry-run" in sys.argv
    do_migrate = "--migrate" in sys.argv
    batch_arg = None
    for i, a in enumerate(sys.argv):
        if a == "--batch" and i + 1 < len(sys.argv):
            batch_arg = sys.argv[i + 1]
            break

    if not RULES_PATH.exists():
        print("归属匹配规则不存在:", RULES_PATH, file=sys.stderr)
        sys.exit(1)
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    rules = data.get("rules") or []
    if not rules:
        print("归属匹配规则 rules 为空", file=sys.stderr)
        sys.exit(1)

    # 待归属下 .md，可选按批次前缀过滤
    all_md = sorted(PENDING.glob("*.md"))
    if batch_arg:
        prefix = f"{batch_arg}_distill_"
        all_md = [p for p in all_md if p.name.startswith(prefix)]
    all_md.sort(key=lambda p: (len(p.name), p.name))

    if not all_md:
        print("待归属下无匹配的 .md 文件", file=sys.stderr)
        sys.exit(0)

    # 推断批次日期
    first_name = all_md[0].name
    m = re.match(r"(\d{8})_distill_", first_name)
    batch_date = m.group(1) if m else ""

    rows = []
    for path in all_md:
        src_name = path.name
        raw = path.read_text(encoding="utf-8", errors="replace")
        title, typ, tags = parse_frontmatter(raw)
        search_text = f"{title} {typ} {tags}"
        target_key = assign_target(search_text, rules)
        safe_title = sanitize_basename(title)
        target_basename = f"{batch_date}_{safe_title}_{typ}.md"
        rows.append((src_name, target_key, target_basename))
        if dry_run:
            print(src_name, "->", target_key, target_basename)

    if dry_run:
        return

    csv_name = f"迁移映射_{batch_date}.csv"
    csv_path = KB_DISTILL / csv_name
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_basename", "target_key", "target_basename"])
        w.writerows(rows)
    print("已生成", rel(csv_path), "共", len(rows), "条", file=sys.stderr)

    if not do_migrate:
        print("未加 --migrate，未执行迁移。可编辑 CSV 后运行: python migrate_by_csv.py ../" + csv_name, file=sys.stderr)
        return

    for src_name, target_key, tname in rows:
        if target_key not in TARGET_DIRS:
            print("SKIP (未知 target_key):", src_name, "->", target_key, file=sys.stderr)
            continue
        src = PENDING / src_name
        if not src.exists():
            print("SKIP (missing):", src_name, file=sys.stderr)
            continue
        tdir = TARGET_DIRS[target_key]
        tdir.mkdir(parents=True, exist_ok=True)
        dst = tdir / tname
        shutil.copy2(src, dst)
        src.unlink()
        print("OK", rel(dst))


if __name__ == "__main__":
    main()
