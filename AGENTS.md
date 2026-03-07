# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a **Knowledge Distillation Agent** — a pure-Python CLI pipeline that collects content from RSS/Atom feeds and web pages, distills it into structured knowledge using an LLM (DeepSeek), and assigns/migrates the output to topic-specific knowledge bases (`about_*` directories).

Pipeline: `collect_sources.py` → `待蒸馏/` → `distill_run.py` → `蒸馏产出_待归属/` → `assign_and_migrate.py` → `about_*`

### Running the scripts

All scripts are in `scripts/` and run with `python3` from that directory. See `scripts/README.md` and the root `README.md` for full command reference.

- **Collection** (no API key needed): `python3 collect_sources.py` — fetches from 20 sources in `config/信息源列表.md`
- **Distillation** (requires `DEEPSEEK_API_KEY`): `python3 distill_run.py --target N` — calls DeepSeek LLM API
- **Assignment/Migration** (requires `KB_VENTURE`): `KB_VENTURE=/path/to/kb python3 assign_and_migrate.py --migrate`

### Environment variables

| Variable | Required for | Notes |
|---|---|---|
| `DEEPSEEK_API_KEY` | `distill_run.py` | Set in `scripts/.env.distill` (copy from `config/.env.distill.example`) |
| `DEEPSEEK_BASE_URL` | `distill_run.py` | Defaults to DeepSeek endpoint |
| `DISTILL_LLM_MODEL` | `distill_run.py` | Defaults to deepseek model |
| `KB_VENTURE` | `assign_and_migrate.py`, `migrate_by_csv.py` | Knowledge base root path for migration target |
| `DISTILL_PROJECT_ROOT` | optional | Defaults to `scripts/` parent directory |

### Key caveats

- **No test framework or linting** is configured in this repository. Validation is done by running scripts with `--dry-run` flags.
- `assign_and_migrate.py` exits immediately with error if `KB_VENTURE` is not set — always provide it via env var when testing that script. For quick local testing, use a temp path: `KB_VENTURE=/tmp/test_kb`.
- The `distill_run.py` script exits with error if `DEEPSEEK_API_KEY` is empty — the collection step (`collect_sources.py`) works without any API keys.
- When `DEEPSEEK_API_KEY` is available as an environment variable, create `scripts/.env.distill` from the example template and populate it before running distillation.
- Collection fetches from live URLs; some may time out or return 403 depending on network conditions. Expect 4-5 sources to fail on each run — this is normal.
- History deduplication is stored in `distill_input_history.json` at the project root. Re-running collection won't duplicate already-fetched URLs. Re-running distillation also skips already-distilled files.
- Distillation is slow (~30-40s per item) since each item requires a full LLM API call. Use `--target N` to control batch size.
- `distill_run.py` emits a `DeprecationWarning` about `datetime.utcnow()` — this is cosmetic and does not affect functionality.
