#!/usr/bin/env python
"""
按 CSV 映射将 蒸馏产出_待归属 中的文件迁移到 about_* 知识库。
约定见 蒸馏归属目标.md；运行后请在 蒸馏归属目标.md 增加「本次迁移记录」节。

CSV 格式（表头可选）：source_basename, target_key, target_basename
- source_basename: 待归属目录下的文件名，如 20260210_distill_001.md
- target_key: INDUSTRY | STARTUP | FINANCIALS | ENERGY_STORAGE | CRISIS_MANAGEMENT | MARKETING | PRODUCT_DEVELOPMENT | KNOWLEDGE_LOGIC | QUANT_ANALYSIS
- target_basename: 目标目录下的文件名，如 20260210_某主题_案例.md

用法：
  python migrate_by_csv.py 迁移映射_20260210.csv
  python migrate_by_csv.py ../迁移映射.csv
  python migrate_by_csv.py --template > ../迁移映射_20260210.csv   # 生成模板（全部默认 INDUSTRY），编辑后再跑上一条
"""
from __future__ import annotations

import csv
import os
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KB_DISTILL = Path(os.environ.get("DISTILL_PROJECT_ROOT", "")).expanduser() if os.environ.get("DISTILL_PROJECT_ROOT") else SCRIPT_DIR.parent
# 迁移目标知识库根：必须由环境变量 KB_VENTURE 提供
_kb = os.environ.get("KB_VENTURE")
if not _kb:
    print("错误：请设置环境变量 KB_VENTURE（知识库根路径）。", file=sys.stderr)
    sys.exit(1)
KB = Path(_kb).expanduser()
PENDING = KB_DISTILL / "蒸馏产出_待归属"

# 与 蒸馏归属目标.md 一致；assign_and_migrate.py 生成的 CSV 会使用这些键
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


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--template":
        # 生成模板：扫描 蒸馏产出_待归属 下 20260210_distill_*.md，输出 CSV（默认 INDUSTRY，目标名=源名）
        out = PENDING.glob("20260210_distill_*.md")
        files = sorted(out, key=lambda p: (len(p.name), p.name))
        writer = csv.writer(sys.stdout)
        writer.writerow(["source_basename", "target_key", "target_basename"])
        for p in files:
            writer.writerow([p.name, "INDUSTRY", p.name])
        print("# 已输出模板到 stdout，可重定向到 迁移映射_20260210.csv 后编辑 target_key/target_basename 再运行迁移", file=sys.stderr)
        return

    if len(sys.argv) < 2:
        print("用法: python migrate_by_csv.py <映射.csv>  或  python migrate_by_csv.py --template", file=sys.stderr)
        sys.exit(1)
    csv_path = Path(sys.argv[1])
    if not csv_path.is_absolute():
        csv_path = (Path.cwd() / csv_path).resolve()
    if not csv_path.exists():
        print("文件不存在:", csv_path, file=sys.stderr)
        sys.exit(1)

    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            if row[0].strip().lower() == "source_basename":
                continue
            if len(row) < 3:
                continue
            src_name = row[0].strip()
            target_key = row[1].strip().upper()
            tname = row[2].strip()
            if target_key not in TARGET_DIRS:
                print("SKIP (未知 target_key):", src_name, "->", target_key, file=sys.stderr)
                continue
            rows.append((src_name, TARGET_DIRS[target_key], tname))

    for src_name, tdir, tname in rows:
        src = PENDING / src_name
        if not src.exists():
            print("SKIP (missing):", src_name)
            continue
        tdir.mkdir(parents=True, exist_ok=True)
        dst = tdir / tname
        shutil.copy2(src, dst)
        src.unlink()
        print("OK", rel(dst))


if __name__ == "__main__":
    main()
