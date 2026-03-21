## 软件测试项目 — 基于 LLM 的白盒测试用例生成工具

---

### 项目简介

使用 **AST 代码分析 + LLM 大语言模型** 自动生成白盒测试用例。
- 支持 Python（AST 精确分析）和其他语言（LLM 通用分析）
- 支持多个 LLM 后端（DeepSeek、OpenAI/ChatAnywhere、Google Gemini、GitHub Models）
- 闭环流程：生成测试 → 运行覆盖率 → 不足则反馈 LLM 补充

---

### 环境配置

#### 1. 创建 Anaconda 环境

```bash
conda create -n ST python=3.11
conda activate ST
```

#### 2. 安装依赖

```bash
cd Assignment1
pip install openai pyyaml coverage pytest google-generativeai esprima
```

#### 3. 配置 API Key

编辑 `Assignment1/config.yaml`，填入你的 API Key：

```yaml
llm:
  deepseek:
    api_key: "你的DeepSeek API Key"
    base_url: "https://api.deepseek.com"
    model: "deepseek-chat"
  openai:
    api_key: "你的ChatAnywhere API Key"
    base_url: "https://api.chatanywhere.tech/v1"
    model: "gpt-3.5-turbo"
```

---

### 使用方法

所有命令在 `Assignment1/` 目录下运行：

```bash
cd Assignment1
```

#### 基本用法（只生成测试用例，不运行覆盖率）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek --no-coverage
```

#### 完整闭环（生成 + 覆盖率反馈补充）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek
```

#### 指定最大闭环轮次

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek --max-rounds 5
```

#### 附带需求文档（提高生成质量）

```bash
python main.py --source targets/convert_number_to_words.py --llm deepseek --requirement targets/requirements_convert_number_to_words.md
```

#### 切换 LLM 后端

```bash
python main.py --source targets/convert_number_to_words.py --llm openai
python main.py --source targets/convert_number_to_words.py --llm google
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
| `--llm` | 否 | LLM 后端名称，默认 `deepseek` |
| `--requirement` | 否 | 需求文档路径 |
| `--compare` | 否 | 用所有 LLM 运行并输出对比表格 |
| `--output` | 否 | 输出目录，默认 `./output` |
| `--no-coverage` | 否 | 只生成测试用例，跳过覆盖率闭环 |
| `--max-rounds` | 否 | 最大闭环轮次，默认 3 |
| `--config` | 否 | 配置文件路径，默认 `config.yaml` |

---

### 输出文件

运行后在 `output/` 目录下生成：

- `test_cases_xxx.json` — 结构化测试用例（含覆盖率信息）
- `test_xxx.py` — 可运行的 pytest 测试文件
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
| **覆盖率** | 语句覆盖率 + 分支覆盖率（coverage.py） |
| **泛化性** | 在两个不同类型项目上的效果对比 |
