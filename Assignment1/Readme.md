## 软件测试项目 — 基于 LLM 的白盒测试用例生成工具

---

### 项目简介

使用 **AST 代码分析 + LLM 大语言模型** 自动生成白盒测试用例。
- 支持 Python（AST 精确分析）和其他语言（LLM 通用分析）
- 支持多个 LLM 后端（DeepSeek Chat、DeepSeek Reasoner、Google Gemini、GitHub Models）
- `--script` 模式：LLM 直接生成可运行的测试脚本（pytest/Jest），支持链式调用等复杂场景
- 闭环流程：生成测试 → 运行覆盖率 → 不足则补充测试方法片段 → 语法校验 → 回退保护
- Python 闭环使用 pytest + coverage.py，JavaScript 闭环使用 Jest + --coverage

---

### 环境配置

#### 1. 创建 Anaconda 环境

```bash
conda create -n ST python=3.11
conda activate ST
```

#### 2. 安装 Python 依赖

```bash
cd Assignment1
pip install openai pyyaml coverage pytest google-generativeai esprima
```

#### 3. 安装 Node.js 依赖（JavaScript 闭环需要）

```bash
npm install
```

#### 4. 配置 API Key

编辑 `Assignment1/config.yaml`，填入你的 API Key：

```yaml
llm:
  deepseek-chat:
    api_key: "你的DeepSeek API Key"
    base_url: "https://api.deepseek.com"
    model: "deepseek-chat"
  deepseek-reasoner:
    api_key: "你的DeepSeek API Key"
    base_url: "https://api.deepseek.com"
    model: "deepseek-reasoner"
  google:
    api_key: "你的Google Gemini API Key"
    model: "gemini-2.5-flash"
  github:
    api_key: "你的GitHub Token"
    base_url: "https://models.inference.ai.azure.com"
    model: "gpt-4o-mini"
```

---

### 使用方法

所有命令在 `Assignment1/` 目录下运行：

```bash
cd Assignment1
```

#### 交互模式（不带参数直接运行）

```bash
python main.py
```

会依次提示输入源文件路径、LLM 后端等参数，按回车使用默认值。

#### 基本用法（只生成 JSON 测试用例，不运行覆盖率）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek-chat
```

#### 生成测试脚本 + 覆盖率闭环（`--script` 模式）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek-chat --script
```

#### JavaScript 项目（推荐使用 `--script` 模式）

```bash
python main.py --source targets/index.js --llm deepseek-chat --script
```

#### 使用 AST 分析辅助（仅 Python）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek-chat --ast
```

#### 附带需求文档（提高生成质量）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek-chat --requirement targets/requirements_convert_number_to_words.md
```

#### 指定最大闭环轮次

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek-chat --script --max-rounds 5
```

#### 切换 LLM 后端

```bash
python main.py --source targets/convert_number_to_words.py --llm google
python main.py --source targets/convert_number_to_words.py --llm github
python main.py --source targets/convert_number_to_words.py --llm deepseek-reasoner
```

#### 对比所有 LLM 的效果

```bash
python main.py --source targets/convert_number_to_words.py --compare
```

---

### 命令行参数说明

| 参数 | 必选 | 说明 |
|------|------|------|
| `--source` | 是 | 被测源代码文件路径 |
| `--llm` | 否 | LLM 后端名称（deepseek-chat / deepseek-reasoner / google / github），默认 `deepseek` |
| `--script` | 否 | LLM 直接生成测试脚本 + 覆盖率闭环（推荐 JS 项目使用） |
| `--ast` | 否 | 使用 AST 分析辅助生成（仅 Python 有效） |
| `--requirement` | 否 | 需求文档路径，为 LLM 提供额外上下文 |
| `--compare` | 否 | 用所有已配置的 LLM 运行并输出对比表格 |
| `--output` | 否 | 输出目录，默认 `./output` |
| `--max-rounds` | 否 | 最大闭环轮次，默认 3（仅 `--script` 模式有效） |
| `--config` | 否 | 配置文件路径，默认 `config.yaml` |

---

### 输出文件

运行后在 `output/` 目录下生成：

- `test_cases_xxx_时间戳.json` — 结构化测试用例（含覆盖率信息）
- `test_xxx_时间戳.py` — 可运行的 pytest 测试文件（Python）
- `test_xxx_时间戳.js` — 可运行的 Jest 测试文件（JavaScript）
- `experiment_data.json` — 实验记录数据
- `comparison_report.md` — 多 LLM 对比报告（`--compare` 模式）

---

### 被测项目

| 文件 | 语言 | 说明 |
|------|------|------|
| `targets/convert_number_to_words.py` | Python | 数字转英文单词，多分支逻辑 |
| `targets/index.js` | JavaScript | Day.js 日期处理库核心模块 |

---

### 评估指标

| 指标 | 评估方式 |
|------|---------|
| **准确性** | 生成的测试用例通过率（passed / total） |
| **覆盖率** | 语句覆盖率 + 分支覆盖率（Python: coverage.py, JS: Jest） |
| **泛化性** | 在两个不同类型项目上的效果对比 |

---

### 项目文档（docs/）

| 文件 | 说明 |
|------|------|
| `docs/工作总结.md` | 完整的工作总结：开发时间线、遇到的问题与解决方案、实验结果汇总、关键结论 |
| `docs/prompt记录.md` | 所有 Prompt 模板的完整内容和设计说明，以及不同配置下的实验对比数据 |
| `docs/log-days.md` | 开发过程中遇到的关键问题分析（脚本截断、覆盖率回退、准确率下降等）及解决策略 |
| `docs/log-all.md` | 大部分实验运行的原始终端输出日志，可用于复现和分析闭环过程 |
| `docs/llm_problem.md` | LLM 生成相关的已知问题记录 |
