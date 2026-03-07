#!/usr/bin/env python
"""
蒸馏脚本：单条（文件/stdin）或批量（待蒸馏/ → 蒸馏产出_待归属）。
单条：python distill_run.py <文件路径>  或  echo "..." | python distill_run.py
批量：python distill_run.py --target 100 [--dry-run]
环境变量从 .env.distill 加载。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KB_DISTILL_DIR = Path(os.environ.get("DISTILL_PROJECT_ROOT", "")).expanduser() if os.environ.get("DISTILL_PROJECT_ROOT") else SCRIPT_DIR.parent
HISTORY_PATH = KB_DISTILL_DIR / "distill_input_history.json"
PENDING_DIR = KB_DISTILL_DIR / "待蒸馏"
OUT_DIR = KB_DISTILL_DIR / "蒸馏产出_待归属"


def load_dotenv():
    try:
        from dotenv import load_dotenv as _load
        env_file = SCRIPT_DIR / ".env.distill"
        if env_file.exists():
            _load(env_file)
    except ImportError:
        pass


def get_llm_client():
    load_dotenv()
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    model = os.environ.get("DISTILL_LLM_MODEL", "deepseek-chat")
    if not api_key:
        print("请在 .env.distill 中配置 DEEPSEEK_API_KEY", file=sys.stderr)
        sys.exit(1)
    try:
        from openai import OpenAI
        return OpenAI(base_url=base_url, api_key=api_key), model
    except ImportError:
        print("请安装: pip install openai python-dotenv", file=sys.stderr)
        sys.exit(1)


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[dict]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def already_processed(entry_id: str, history: list[dict]) -> bool:
    return any(h.get("id") == entry_id for h in history)


def content_hash(text: str, max_chars: int = 8000) -> str:
    normalized = re.sub(r"\s+", " ", text.strip())
    normalized = normalized[:max_chars]
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def already_distilled_by_content(content_hash_val: str, history: list[dict]) -> bool:
    return any(h.get("content_hash") == content_hash_val for h in history)


def distill_one(client, model: str, title: str, text: str, source_url: str = "", date_str: str = "") -> str:
    """调用 LLM 提炼一条知识单元（Markdown）。"""
    prompt = f"""从下面这段内容中提炼可沉淀的结构化知识，采用「知识单元(KU) + 关系图谱 + 本质观点与关键因素」的流程，输出为**一条**结构化 Markdown 知识单元（一个文档内包含下列所有小节）。

## 一、提炼要求（按顺序）

### 1) 知识单元（KU）
- 将内容拆解为原子化知识单元，每个 KU 一句话定义，并标注**类型**之一：概念、命题/观点、机制/因果、指标/变量、方法/策略、约束/前提、证据/事实。
- 对每个 KU 给出**边界**（包含/不包含什么）与**原文证据**（1 句关键短语短引）。
- KU 类型与最终「类型」字段的对应：概念/术语→术语，方法/框架→框架，命题/原则→原则，机制/指标/数据→指标，案例/事实→案例。

### 2) 关系图谱
- 写出 KU 之间的**关系**，至少覆盖：causes（因果）、depends_on（依赖）、drives（驱动）、correlates（相关）、constrains（约束）、supports（支撑/证据）。
- 每条关系注明：From KU、To KU、关系类型、**强度(1-5)**（5=明确必要且充分/强因果，4=明确因果或关键依赖，3=合理推断，2=可能影响，1=仅同现）、**证据**（原文短引或触发词如「导致/因此/取决于」）。
- 以表格呈现：| From | To | Type | Strength(1-5) | Evidence |

### 3) 本质观点与最重要因素
- **本质观点（1–3 条）**：从关系图谱中选出出度/入度高、强度高、贯穿全文的 KU 或子图，改写成可独立陈述的观点。
- **最重要因素（Top 3–5）**：优先选连接多簇的枢纽 KU、多条高强度边指向的 KU、或约束/因果的源头 KU。

### 4) 正文（可泛化、支持任务决策）
- **核心洞察**：原文背后的意义、机制或隐含逻辑。
- **可泛化**：适用边界、条件、可复用模式，避免只绑定单一事件。
- **可引用与可操作**：原则补边界与反例，框架补层级/步骤，案例补关键要素，指标补口径与解读要点。

## 二、输出格式（必须完整）

整份输出为**一条** Markdown 知识单元，包含以下结构（缺一不可）：

```
标题：（与输入标题一致或提炼）
类型：（原则/框架/案例/指标/术语 之一）
主题标签：#xxx
来源 URL：{source_url or "无"}
日期：{date_str or "无"}

## 知识单元（KU）
- KU-01（类型）：定义｜边界｜证据
- KU-02（类型）：…
（根据需要列出，不必拘泥数量）

## 关系图谱
| From | To | Type | Strength(1-5) | Evidence |
|------|-----|------|---------------|----------|
| KU-xx | KU-yy | causes | 4 | "…" |
…

## 本质观点（1–3）
1. …
## 最重要因素（Top 3–5）
1. …

## 正文
（核心洞察、可泛化要点、可引用与可操作说明；可含列表或表格）
```

只输出上述一条知识单元的 Markdown，不要多余解释或前缀说明。

---
标题：{title}
来源：{source_url or "无"}
日期：{date_str or "无"}
---
内容：
{text[:8000]}
---
请直接输出该知识单元的完整 Markdown。"""

    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return (r.choices[0].message.content or "").strip()


def run_single(path_or_stdin: Path | None, history: list[dict]) -> str | None:
    """处理单条输入，返回蒸馏后的 Markdown，或 None（跳过）。会修改并写回 history。"""
    if path_or_stdin is not None:
        path = Path(path_or_stdin)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        if not path.exists():
            print(f"文件不存在: {path}", file=sys.stderr)
            return None
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        title = path.stem
        entry_id = str(path.resolve())
        source_type = "document"
    else:
        text = sys.stdin.read()
        if not text.strip():
            return None
        title = "stdin"
        entry_id = f"stdin:{hash(text[:500])}"
        source_type = "stdin"

    source_url = ""
    date_str = ""
    if already_processed(entry_id, history):
        return None
    content_hash_val = content_hash(text)
    if already_distilled_by_content(content_hash_val, history):
        return None

    client, model = get_llm_client()
    out = distill_one(client, model, title, text, source_url, date_str)
    now = datetime.utcnow().isoformat() + "Z"
    history.append({
        "id": entry_id,
        "source_type": source_type,
        "content_hash": content_hash_val,
        "first_seen_at": now,
        "distilled_at": now,
    })
    save_history(history)
    return out


def run_batch(target: int, dry_run: bool) -> None:
    history = load_history()
    already_ids = {h["id"] for h in history if h.get("id")}
    if not PENDING_DIR.exists():
        print(f"待蒸馏目录不存在: {PENDING_DIR}", file=sys.stderr)
        sys.exit(1)
    pending_files = sorted(PENDING_DIR.glob("*.md"))
    to_process = []
    for f in pending_files:
        try:
            resolved = str(f.resolve())
        except Exception:
            resolved = str(f)
        if resolved not in already_ids:
            to_process.append(f)

    print(f"待蒸馏共 {len(pending_files)} 个 .md，未蒸馏 {len(to_process)} 个", file=sys.stderr)
    if dry_run:
        for f in to_process[:target]:
            print(f.name)
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date_prefix = datetime.now().strftime("%Y%m%d")
    existing_nums = []
    for p in OUT_DIR.glob(f"{date_prefix}_distill_*.md"):
        try:
            n = int(p.stem.split("_")[-1])
            existing_nums.append(n)
        except (ValueError, IndexError):
            pass
    start_index = max(existing_nums, default=0)
    if start_index > 0:
        print(f"# 当日已有至 {start_index:03d}，新产出自 {start_index + 1:03d} 起", file=sys.stderr)

    client, model = get_llm_client()
    done = 0
    for f in to_process:
        if done >= target:
            break
        with open(f, "r", encoding="utf-8", errors="replace") as fp:
            text = fp.read()
        title = f.stem
        entry_id = str(f.resolve())
        if already_processed(entry_id, history):
            continue
        content_hash_val = content_hash(text)
        if already_distilled_by_content(content_hash_val, history):
            continue
        print(f"[{done + 1}/{target}] {f.name} -> ", end="", file=sys.stderr)
        try:
            out = distill_one(client, model, title, text, "", "")
        except Exception as e:
            print(f" 错误: {e}", file=sys.stderr)
            continue
        if not out.strip():
            print(" 无产出", file=sys.stderr)
            continue
        out_name = f"{date_prefix}_distill_{start_index + done + 1:03d}.md"
        (OUT_DIR / out_name).write_text(out, encoding="utf-8")
        now = datetime.utcnow().isoformat() + "Z"
        history.append({
            "id": entry_id,
            "source_type": "document",
            "content_hash": content_hash_val,
            "first_seen_at": now,
            "distilled_at": now,
        })
        save_history(history)
        done += 1
        print(out_name, file=sys.stderr)
    print(f"本次完成 {done} 条蒸馏，产出在 {OUT_DIR}", file=sys.stderr)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="蒸馏：单条（文件/stdin）或批量（--target）")
    parser.add_argument("path", nargs="?", help="待蒸馏的 .md 文件路径（不传则从 stdin 读入）")
    parser.add_argument("--target", type=int, default=0, help="批量模式：从待蒸馏/ 蒸馏至目标条数")
    parser.add_argument("--dry-run", action="store_true", help="批量模式：仅列待处理文件")
    args = parser.parse_args()

    if args.target > 0:
        run_batch(args.target, args.dry_run)
        return

    # 单条模式
    if args.path:
        path = Path(args.path)
        if path.is_absolute() or path.exists():
            pass
        else:
            path = (Path.cwd() / path).resolve()
        out = run_single(path, load_history())
    else:
        if sys.stdin.isatty():
            print("用法: python distill_run.py <文件路径>  或  echo \"...\" | python distill_run.py", file=sys.stderr)
            print("      python distill_run.py --target 100   # 批量", file=sys.stderr)
            sys.exit(1)
        out = run_single(None, load_history())

    if out is None:
        print("(已跳过：在历史中或内容重复)", file=sys.stderr)
        sys.exit(0)
    print(out)


if __name__ == "__main__":
    main()
