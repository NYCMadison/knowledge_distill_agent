# 脚本说明

- **采集**：仅用 **`collect_sources.py`**。从 `config/信息源列表.md` 读取「每行一个」的 URL，写入 `待蒸馏/`。URL 为 feed（RSS/Atom）则解析条目，为网页则抓主站子页。
- **蒸馏**：`distill_run.py`（单条：文件/stdin；批量：`--target N`）。
- **迁移**：`assign_and_migrate.py`、`migrate_by_csv.py`（须设 KB_VENTURE）。
- **路径**：由环境变量提供（KB_VENTURE 迁移时必设，DISTILL_PROJECT_ROOT 可选），项目中不引用本地路径。

## 常用命令

```bash
conda activate ikb_env
export KB_VENTURE=<知识库根路径>   # 迁移时必设

python collect_sources.py                    # 从信息源列表采集
python collect_sources.py --dry-run          # 仅打印将处理的条目
python distill_run.py --target 50          # 批量蒸馏
python assign_and_migrate.py --migrate       # 归属并迁移
```

## 信息源列表格式

`config/信息源列表.md`：每行一个 URL，空行与 `#` 开头行忽略。RSS/Atom 订阅 URL 可从 OPML 中导出 xmlUrl 后每行一个粘贴到列表中。
