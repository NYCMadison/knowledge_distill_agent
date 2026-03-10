# 知识蒸馏项目 (Knowledge Distill Agent)

**来源**：由「知识抽取和蒸馏」整理而成的独立项目，用于从多源信息（RSS/Atom 订阅、主页面 URL）采集内容并蒸馏为结构化知识，按主题迁移到 about_* 知识库。

**运行环境**：适用于**线上/云环境**（如 Cursor Cloud、CI、远程服务器）。**不依赖本地知识库路径**：所有输入/输出路径由**环境变量**配置，便于在任意部署环境中运行。

---

## 一、流程总览

```
多源采集 → 待蒸馏/ → 批量蒸馏 → 蒸馏产出_待归属/ → 按规则归属并迁移 → about_*
```

| 阶段     | 输入           | 输出                         | 关键脚本/配置                    |
|----------|----------------|------------------------------|----------------------------------|
| 采集     | 信息源列表（每行一个 URL） | `待蒸馏/*.md` + history 去重 | `collect_sources.py` |
| 蒸馏     | `待蒸馏/` 中未在 history 的 .md | `蒸馏产出_待归属/*.md` + history | `distill_run.py`（单条或 `--target` 批量） |
| 归属迁移 | `蒸馏产出_待归属/*.md` | about_* 下按主题落盘         | `归属匹配规则.json`、`assign_and_migrate.py` |

---

## 二、环境变量（必读）

| 变量 | 必填 | 说明 |
|------|------|------|
| **KB_VENTURE** | 是（迁移时） | 知识库根路径，迁移目标 about_* |
| **DISTILL_PROJECT_ROOT** | 可选 | 项目根路径（待蒸馏、蒸馏产出_待归属、history 所在目录）；未设置时默认为脚本所在目录的父目录 |

**说明**：项目中不引用任何本地路径；部署时在运行环境中设置上述变量即可。

---

## 三、目录结构

```
knowledge_distill_agent/
├── README.md
├── docs/                     # 流程、架构、归属目标、经验总结、口径说明
├── config/
│   ├── 信息源列表.md          # 每行一个 URL，便于管理与更新
│   ├── 归属匹配规则.json      # 脚本直接读取
│   └── .env.distill.example   # API 与环境变量示例
├── scripts/
├── 待蒸馏/
├── 蒸馏产出_待归属/
└── distill_input_history.json
```

---

## 四、快速开始

**环境**：conda 环境 **ikb_env**，使用 **python**。

```bash
cd <项目根>/scripts
conda activate ikb_env
pip install -r requirements.txt
cp ../config/.env.distill.example .env.distill   # 填入 DEEPSEEK_API_KEY 等
export KB_VENTURE=<知识库根路径>   # 迁移时必设
# 可选：export DISTILL_PROJECT_ROOT=<项目根>
```

### 采集 → 蒸馏 → 迁移

```bash
python collect_sources.py                    # 从信息源列表采集到待蒸馏
python distill_run.py --target 50          # 批量蒸馏（条数自定）
python assign_and_migrate.py --migrate       # 按规则归属并迁移（需已设 KB_VENTURE）
```

### 只做归属/迁移

```bash
python assign_and_migrate.py --dry-run
python assign_and_migrate.py --migrate
```

### 每日自动化（固定长期分支）

使用同一个长期分支运行每日任务，避免每次触发都生成新分支：

```bash
LONG_BRANCH=bot/daily-distill DISTILL_TARGET=100 bash scripts/run_daily_pipeline.sh
```

可选变量：
- `LONG_BRANCH`：长期分支名（默认 `bot/daily-distill`）
- `DISTILL_TARGET`：批量蒸馏目标条数（默认 `100`）
- `PYTHON_BIN`：Python 可执行文件（默认 `python3`）

---

## 五、信息源管理

**单一文件**：`config/信息源列表.md`。**每行一个**信息源，不区分类型：

- **RSS/Atom 订阅 URL**：直接拉取 feed，解析近期条目写入待蒸馏（可从 OPML 中导出 feed 的 xmlUrl 粘贴到此处）
- **主页面 URL**：抓取主站及子页正文写入待蒸馏

空行与 `#` 开头行忽略。增删改信息源只改此文件；采集由统一脚本 `collect_sources.py` 读取并处理。

---

## 六、文档索引

| 文档 | 内容 |
|------|------|
| **docs/流程说明.md** | 采集→待蒸馏→蒸馏→待归属→迁移 |
| **docs/架构.md** | 信息源蒸馏与知识/任务体系更新架构 |
| **docs/蒸馏归属目标.md** | 可归属的 about_* 列表与归属决策说明 |
| **docs/任务体系设计_经验总结.md** | 蒸馏→归属→任务体系的可复用经验 |
| **docs/采集蒸馏归属_口径与日报.md** | 采集/蒸馏/归属统计口径 |
| **config/信息源列表.md** | 信息源一行一条，统一管理 |

---

*项目版本：1.1 | 适用于线上/云环境，路径由环境变量配置；信息源合并为 config/信息源列表.md*
