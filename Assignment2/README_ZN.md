# AutoTestDesign AI 应用

AutoTestDesign 是一个基于 Streamlit 的测试设计工作空间，用于 Assignment 2。

它支持一种以需求为驱动的工作流程，用于生成和改进：

* 结构化需求
* 风险分析
* 覆盖项
* 测试策略
* 高层测试套件
* 详细测试用例
* 可追踪性矩阵
* Markdown 格式的测试计划文档

当前的演示目标是 `../simpletodolist`，但该工具本身被设计为领域无关，并以需求为驱动。

## 1. 工具功能

该应用会引导用户完成以下工作流程：

1. `Requirement Input` 需求输入
2. `Risk Analysis` 风险分析
3. `Coverage, Strategy & Model` 覆盖、策略与模型
4. `Suites & Cases` 测试套件与测试用例
5. `Test Plan Document` 测试计划文档
6. `Export` 导出

该工作流程是有意分阶段设计的。前面阶段生成的工件会成为后续阶段的输入，这使得生成结果具有可追踪性，并且更容易审查。

## 2. 环境配置

### 2.1 Python 依赖

安装所需软件包：

```powershell
pip install -r requirements.txt
```

当前 Python 包依赖包括：

* `streamlit`
* `pandas`
* `openpyxl`
* `scikit-learn`
* `pytest`
* `python-dotenv`
* `requests`
* `spacy`

### 2.2 spaCy 模型

需求处理流程使用 spaCy。需要单独安装英文模型：

```powershell
python -m spacy download en_core_web_sm
```

需要该模型的原因：

* `spacy` 安装的是 NLP 框架
* `en_core_web_sm` 提供本地需求解析所使用的英文语言模型

## 3. LLM 配置

该工具被设计为支持两种模式：

1. `local-first mode` 本地优先模式
2. `local + LLM enhancement mode` 本地 + LLM 增强模式

即使没有任何外部 LLM API，该工具也可以运行。在这种情况下，系统仍然会执行基于本地规则或轻量级机器学习的生成流程。

### 3.1 配置 `.env`

复制模板文件：

```powershell
Copy-Item .env.example .env
```

然后填写你的 API key 和 endpoint。

当前 `.env.example` 假设使用兼容 OpenAI 的 Chat Completion 接口：

```text
AUTOTESTDESIGN_LLM_PROVIDERS=deepseek,aliyun 
AUTOTESTDESIGN_LLM_TIMEOUT=120 # LLM 请求超时时间，单位为秒
AUTOTESTDESIGN_LLM_LOG=1 # 是否记录 LLM 请求和响应 1=是 0=否

AUTOTESTDESIGN_LLM_DEEPSEEK_API_KEY=
AUTOTESTDESIGN_LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
AUTOTESTDESIGN_LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro,deepseek-chat

AUTOTESTDESIGN_LLM_ALIYUN_API_KEY=
AUTOTESTDESIGN_LLM_ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AUTOTESTDESIGN_LLM_ALIYUN_MODELS=qwen-plus,qwen-max,qwen3.5-plus
```

### 3.2 运行时 LLM 设置

在 Streamlit 侧边栏中，用户可以调整：

* provider
* model
* LLM batch size
* LLM concurrency

这些设置会影响可选的 LLM 增强阶段，例如：

* 覆盖项改进
* 策略改进
* 测试套件描述改进
* 测试用例修订与补充
* 预期结果的 oracle 澄清
* 优化测试套件最小化审查
* 测试计划文档改进

## 4. 如何启动应用

在当前项目目录下运行 Streamlit 应用：

```powershell
streamlit run app.py
```

启动后：

1. 打开终端中显示的 Streamlit 本地 URL
2. 提供或编辑需求输入
3. 按页面顺序完成工作流程
4. 在准备好后导出生成的工件

## 5. 如何使用工作流程

### 5.1 Requirement Input 需求输入

该页面用于：

* 手动输入需求
* 加载结构化需求行
* 规范化缺失或重复的需求 ID
* 将需求结构化为输入、条件、动作和预期结果等字段

### 5.2 Risk Analysis 风险分析

该页面生成需求级别的风险输出，包括：

* 风险类别
* 影响
* 发生可能性
* 风险分数
* 风险等级
* 测试建议

### 5.3 Coverage, Strategy & Model 覆盖、策略与模型

该页面生成：

* 覆盖项
* 每个覆盖项所选择的测试技术
* 从需求行为模型推导出的状态转换序列

### 5.4 Suites & Cases 测试套件与测试用例

该页面生成：

* 高层测试套件
* 候选测试用例
* 优化后的测试套件
* 可追踪性矩阵

### 5.5 Test Plan Document 测试计划文档

该页面基于以下内容生成英文 Markdown 测试计划文档：

* 需求
* 风险
* 覆盖项
* 测试策略
* 测试套件
* 测试用例
* 状态转换信息

该文档可以：

* 预览
* 编辑
* 使用 LLM 改进
* 直接导出为 Markdown

### 5.6 Export 导出

导出页面支持：

* `Markdown document` Markdown 文档
* `XLSX workbook` XLSX 工作簿
* `CSV package` CSV 包
* `JSON artifact` JSON 工件
* `Full package` 完整包

## 6. 代码结构

主项目结构如下：

```text
./
  app.py
  requirements.txt
  README.md
  .env.example
  app_ui/
  src/
  data/
  docs/
  exports/
  scripts/
  tests/
```

### 6.1 UI 层

`app.py`

* Streamlit 入口文件
* 侧边栏工作流导航
* provider/model 选择
* 顶层页面路由

`app_ui/`

* `actions.py`：由 UI 触发的工作流动作
* `state.py`：会话状态初始化和下游状态重置
* `components.py`：共享 UI 组件和指标
* `styles.py`：自定义 Streamlit 样式
* `pages/`：各个工作流页面

重要页面文件：

* `requirement_input.py`
* `risk_analysis.py`
* `coverage_strategy.py`
* `test_cases.py`
* `test_plan_document.py`
* `export.py`

### 6.2 核心逻辑层

`src/`

* `requirement_parser.py`：需求结构化
* `nlp_processor.py`：本地 NLP 支持
* `risk_analyzer.py`：风险生成和回退逻辑
* `ml_risk_model.py`：轻量级机器学习风险框架
* `coverage_identifier.py`：覆盖项生成
* `test_strategy_selector.py`：策略/技术选择
* `state_modeler.py`：状态模型和转换序列生成
* `test_suite_designer.py`：测试套件设计和套件元数据改进
* `test_case_generator.py`：详细测试用例生成
* `oracle_generator.py`：预期结果澄清
* `suite_optimizer.py`：优化测试套件缩减
* `test_plan_document_generator.py`：Markdown 测试计划生成
* `exporter.py`：导出流程和可追踪性输出
* `improvement_engine.py`：LLM 增强审查和改进的编排
* `ai_client.py`：provider/model 抽象
* `llm_execution.py`：批处理执行、回退、超时和并发处理

### 6.3 测试与示例资产

* `data/`：示例需求输入
* `docs/`：参考资料和模板材料
* `exports/`：生成的工件
* `scripts/`：工具脚本，包括 pytest 导出清理
* `tests/`：核心逻辑的回归测试

## 7. LLM 处理策略

该工具并不依赖 LLM 完成整个流水线。

它的设计有意采用 `local-first` 本地优先方式，并在其上叠加可选的 LLM 增强。

### 7.1 本地优先基线

大多数流水线阶段都有本地或基于规则的基线能力：

* 需求规范化
* 需求结构化回退
* 风险分析回退
* 覆盖项生成
* 策略选择
* 状态模型生成
* 测试套件生成
* 测试用例生成
* 导出和可追踪性生成

这意味着即使在以下情况下，该工具仍然可用：

* 未配置 API key
* provider 不可用
* LLM 响应失败
* JSON 解析失败

### 7.2 LLM 增强

LLM 主要用于改进已有工件，而不是完全替代它们。

示例包括：

* 改进较弱的覆盖项描述
* 优化策略描述
* 修订模糊或质量较弱的测试用例
* 澄清预期结果
* 改进测试套件元数据
* 审查优化测试套件，确保最小化安全合理
* 润色最终测试计划文档

### 7.3 批处理

为了使请求保持可控，系统会分批处理 LLM 任务。

这对于以下任务尤其重要：

* 需求结构化
* 风险分析
* 覆盖项改进
* 测试用例改进
* oracle 审查
* 测试套件最小化

实现中使用可配置的：

* batch size
* concurrency
* timeout

这有助于控制：

* 延迟
* token 使用量
* provider 速率限制压力
* 错误恢复行为

### 7.4 回退与稳健性

当某个 LLM 阶段失败时，该工具通常不会停止整个工作流程。

相反，它会：

* 回退到本地逻辑，或
* 保留当前工件并记录 LLM 错误

这种行为会通过 UI 中的警告信息和保留的本地输出体现出来。

### 7.5 选择该设计的原因

这种混合设计用于平衡：

* 可复现性
* 可追踪性
* 无云依赖情况下的可用性
* 在 LLM 可用时获得更好的措辞和改进效果

换句话说：

* 本地逻辑提供稳定基线
* LLM 审查提供可选的质量提升

## 8. 测试计划文档设计

当前工具将测试计划视为一个文档工件，而不是仅用于内部处理的表格对象。

Markdown 测试计划由已有工件生成，并包含以下章节：

* 项目范围
* 测试项
* 高层测试套件设计
* 进度/检查清单
* 组织结构
* 选定框架及其理由
* 成本估算
* 当前工件总结

该文档旨在支持作业提交和项目报告，而详细的结构化表格仍然可以在工具和导出包的其他位置获取。

## 9. 测试

使用以下命令运行主要回归测试文件：

```powershell
python -m pytest tests/test_case_generator.py -q
```

其他测试文件也可在 `tests/` 目录下找到。

## 10. 工具脚本

`scripts/cleanup_pytest_exports.ps1`

用途：

* 从 `exports/` 中删除生成的 `pytest_*` 导出文件

示例：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\cleanup_pytest_exports.ps1
```

## 11. 说明

* 生成的工件是设计工件，本身不是可执行的端到端测试程序。
* Selenium、PyTest 和 JUnit 等框架会在生成的测试计划中被描述，但该工具本身并不直接执行浏览器自动化。
* Todo 示例只是一个演示目标。只要需求以合适的形式提供，该流水线就可以推广到其他应用。
