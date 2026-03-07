#!/usr/bin/env python
"""
统一采集脚本：从 config/信息源列表.md 读取「每行一个」的 URL，写入待蒸馏。
URL 为 feed（RSS/Atom）则解析条目；为网页则抓主站子页。运行环境通过环境变量提供配置，不在脚本中写死路径。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("DISTILL_PROJECT_ROOT", "")).expanduser() if os.environ.get("DISTILL_PROJECT_ROOT") else SCRIPT_DIR.parent
SOURCES_FILE = PROJECT_ROOT / "config" / "信息源列表.md"
PENDING_DIR = PROJECT_ROOT / "待蒸馏"
HISTORY_PATH = PROJECT_ROOT / "distill_input_history.json"

FEED_TIMEOUT = int(os.environ.get("DISTILL_OPML_FEED_TIMEOUT", "25"))
DAYS_RECENT = int(os.environ.get("DISTILL_OPML_DAYS_RECENT", "90"))
PER_FEED = int(os.environ.get("DISTILL_OPML_PER_FEED", "10"))
MAX_FEEDS = int(os.environ.get("DISTILL_OPML_MAX_FEEDS", "50"))
TOTAL_CAP = int(os.environ.get("DISTILL_OPML_TOTAL_CAP", "100"))
MAX_PER_SITE = int(os.environ.get("DISTILL_ADDITIONAL_MAX_PER_SITE", "8"))
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
CONTENT_PATH_KEYWORDS = (
    "report", "case", "study", "resource", "article", "blog", "paper", "course",
    "knowledge", "hub", "database", "toolkit", "microgrid", "semiconductor", "energy",
)


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[dict]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def slug(s: str, max_len: int = 40) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len] if s else "untitled"


def read_sources(path: Path) -> list[str]:
    """每行一个 URL，跳过空行和 # 注释。"""
    if not path.exists():
        return []
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not (line.startswith("http://") or line.startswith("https://")):
            continue
        lines.append(line)
    return lines


def is_feed_content(data: bytes, content_type: str) -> bool:
    ct = (content_type or "").lower()
    if "xml" in ct or "rss" in ct or "atom" in ct:
        return True
    head = (data[:500] or b"").decode("utf-8", errors="ignore")
    return "<rss" in head or "<feed" in head or '<?xml' in head


def collect_from_feed_url(url: str, history: list[dict], history_ids: set[str], date_prefix: str, cutoff: datetime) -> int:
    """RSS/Atom URL：拉取 feed，写入近期条目到待蒸馏。"""
    try:
        import feedparser
        import urllib.request
    except ImportError:
        print("# 跳过 feed（未安装 feedparser）", file=sys.stderr)
        return 0
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, */*"})
        with urllib.request.urlopen(req, timeout=FEED_TIMEOUT) as resp:
            data = resp.read()
    except Exception as e:
        print(f"# 拉取失败 {url[:50]}... {e}", file=sys.stderr)
        return 0
    fp = feedparser.parse(data)
    entries = getattr(fp, "entries", [])[:PER_FEED]
    feed_title = getattr(fp.feed, "title", "") or urlparse(url).netloc
    written = 0
    for entry in entries:
        link = getattr(entry, "link", "") or ""
        if not link or link in history_ids:
            continue
        pub = None
        if getattr(entry, "published_parsed", None):
            t = entry.published_parsed
            pub = datetime(*t[:6], tzinfo=timezone.utc)
        if pub is None or pub < cutoff:
            continue
        title = getattr(entry, "title", "") or "untitled"
        summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
        if hasattr(summary, "replace"):
            summary = summary[:2000]
        else:
            summary = ""
        base = f"feed_{date_prefix}_{slug(title)}_{slug(feed_title, 20)}.md"
        base = base[:120]
        dest = PENDING_DIR / f"{base}.md"
        if dest.exists():
            dest = PENDING_DIR / f"{base}_{int(time.time())}.md"
        body = f"# {title}\n\n**来源**：{link}\n**日期**：{pub.strftime('%Y-%m-%d')}\n**feed**：{feed_title}\n\n---\n\n{summary}"
        dest.write_text(body, encoding="utf-8")
        history.append({"id": link, "source_type": "feed_entry", "first_seen_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "distilled_at": ""})
        history_ids.add(link)
        written += 1
        print(dest.name)
    return written


def collect_from_page_url(url: str, history: list[dict], history_ids: set[str], date_prefix: str, session) -> int:
    """主页面 URL：抓主站，发现子页，抓子页正文写入待蒸馏。"""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("# 跳过页面（未安装 requests 或 beautifulsoup4）", file=sys.stderr)
        return 0
    try:
        r = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        r.raise_for_status()
        html = r.text
    except Exception as e:
        print(f"# 抓取失败 {url[:50]}... {e}", file=sys.stderr)
        return 0
    base_parsed = urlparse(url)
    base_netloc = base_parsed.netloc
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for a in soup.find_all("a", href=True):
        href = (a.get("href") or "").strip()
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        full = urljoin(url, href)
        try:
            p = urlparse(full)
        except Exception:
            continue
        if p.netloc != base_netloc:
            continue
        path_lower = (p.path or "").lower()
        if any(k in path_lower for k in CONTENT_PATH_KEYWORDS):
            candidates.append(full)
    candidates = list(dict.fromkeys(candidates))[:MAX_PER_SITE]
    written = 0
    label = base_parsed.netloc.replace(".", "_")
    for sub_url in candidates:
        if sub_url in history_ids:
            continue
        time.sleep(0.3)
        try:
            r2 = session.get(sub_url, headers={"User-Agent": USER_AGENT}, timeout=15)
            r2.raise_for_status()
            sub_html = r2.text
        except Exception:
            continue
        soup2 = BeautifulSoup(sub_html, "html.parser")
        for tag in soup2(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        body = (soup2.find("body") or soup2).get_text(separator="\n", strip=True)
        if len(body) < 200:
            continue
        path_slug = slug(urlparse(sub_url).path.strip("/") or "page", 30)
        fname = f"page_{date_prefix}_{label}_{path_slug}.md"
        dest = PENDING_DIR / fname
        if dest.exists():
            dest = PENDING_DIR / f"{fname.removesuffix('.md')}_{int(time.time())}.md"
        content = f"# {label} - {path_slug}\n\n**来源**：{sub_url}\n**日期**：{date_prefix}\n\n---\n\n{body[:80000]}"
        dest.write_text(content, encoding="utf-8")
        history.append({"id": sub_url, "source_type": "url", "first_seen_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "distilled_at": ""})
        history_ids.add(sub_url)
        written += 1
        print(dest.name)
    return written


def main():
    parser = argparse.ArgumentParser(description="从信息源列表（每行一个 URL）采集到待蒸馏")
    parser.add_argument("--sources", type=Path, default=SOURCES_FILE, help="信息源列表文件路径")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将处理的条目，不采集")
    args = parser.parse_args()

    sources_path = args.sources.resolve() if args.sources else SOURCES_FILE
    lines = read_sources(sources_path)
    if not lines:
        print("未找到有效信息源行，或文件为空。", file=sys.stderr)
        return
    if args.dry_run:
        for i, line in enumerate(lines, 1):
            print(f"{i}\t{line[:80]}")
        return

    history = load_history()
    history_ids = {h.get("id", "") for h in history if h.get("id")}
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    date_prefix = datetime.now().strftime("%Y%m%d")
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS_RECENT)
    total_written = 0

    try:
        import requests
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
    except ImportError:
        session = None

    for line in lines:
        if total_written >= TOTAL_CAP:
            break
        if line.startswith("http://") or line.startswith("https://"):
            # 先按 feed 拉取；若返回 HTML 再按主页面处理
            try:
                import urllib.request
                req = urllib.request.Request(line, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=FEED_TIMEOUT) as resp:
                    data = resp.read()
                    ct = resp.headers.get("Content-Type", "")
            except Exception as e:
                print(f"# 跳过 {line[:50]}... {e}", file=sys.stderr)
                continue
            if is_feed_content(data, ct):
                n = collect_from_feed_url(line, history, history_ids, date_prefix, cutoff)
                total_written += n
            else:
                if session:
                    n = collect_from_page_url(line, history, history_ids, date_prefix, session)
                    total_written += n

    if total_written > 0:
        save_history(history)
    print(f"# 本次共写入待蒸馏 {total_written} 条", file=sys.stderr)


if __name__ == "__main__":
    main()
