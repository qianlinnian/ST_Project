# Defense Notes
# 答辩备注

## Core positioning
## 核心定位

This project should **not** be presented as:
这个项目**不应该**被表述为：

- "We built an AI tool, gave the code to the model, and testing was done automatically."
- “我们做了一个 AI 工具，把代码丢给模型，测试就自动完成了。”

It should be presented as:
它更合适的表述应该是：

- "This is an **AI-assisted white-box testing tool project**."
- “这是一个**AI 辅助的白盒测试工具项目**。”

- "The tool is designed to support software testing tasks, not to replace testing methodology."
- “这个工具的目标是支持软件测试任务，而不是替代测试方法本身。”

- "Human test analysis provides the baseline and evaluation criteria; the tool improves efficiency, coverage expansion, and iterative refinement."
- “人工测试分析提供基线和评价标准；工具负责提升效率、扩展覆盖范围，并支持迭代补充。”

One safe one-sentence positioning for the defense:
一个比较稳妥的答辩一句话定位是：

> Our project is an AI-assisted white-box testing tool that embeds LLMs into the testing workflow to improve coverage generation efficiency, while test strategy, coverage interpretation, and validity judgment still rely on human analysis.
> 我们的项目是一个 AI 辅助白盒测试工具，它将 LLM 融入测试流程以提升覆盖率生成效率，但测试策略、覆盖项解释和有效性判断仍然依赖人工分析。

## What the teacher is likely to care about
## 老师更可能在意什么

The teacher is likely not only checking whether we built a tool, but whether we still understand:
老师大概率不只是看我们有没有做出工具，更会看我们是否真正理解：

- black-box testing
- 黑盒测试

- white-box testing
- 白盒测试

- experience-based testing
- 经验测试

- coverage items and what they actually mean
- 各类覆盖项，以及这些覆盖项到底意味着什么

- the difference between high coverage and valid testing
- 高覆盖率和有效测试之间的区别

- the role of human review in evaluating AI-generated tests
- 人工复核在评估 AI 生成测试中的作用

So the defense should always keep the focus on:
所以答辩时应该始终把重点放在：

- testing goals
- 测试目标

- testing methodology
- 测试方法

- human baseline
- 人工基线

- what the tool helps with
- 工具具体帮助了什么

- where the tool still has limitations
- 工具目前还有哪些局限

## Recommended defense logic
## 建议的答辩逻辑

Use the following narrative:
可以按下面这条叙述主线来讲：

### 1. Start from the testing problem, not from the tool
### 1. 从测试问题出发，而不是从工具出发

Suggested idea:
建议表达的核心意思：

- Manual white-box testing is systematic but time-consuming.
- 人工白盒测试是系统化的，但非常耗时。

- For complex code, especially JavaScript chain-call libraries, manually enumerating branches and paths becomes expensive and error-prone.
- 对复杂代码，尤其是 JavaScript 链式调用库，人工枚举分支和路径的成本很高，而且容易出错。

- Therefore, we designed a tool to **assist** testing, not to replace testing.
- 因此我们设计了一个工具来**辅助**测试，而不是替代测试。

Suggested line:
建议直接讲的一句话：

> We started from a software testing problem: manual white-box analysis is interpretable and reliable, but expensive and incomplete on complex code. Therefore, we built an AI-assisted tool to support branch discovery, test generation, and coverage refinement.
> 我们是从一个软件测试问题出发的：人工白盒分析具有可解释性和可靠性，但在复杂代码上成本高且不够完整。因此我们构建了一个 AI 辅助工具，用来支持分支发现、测试生成和覆盖率补充。

### 2. Emphasize that manual testing is the baseline
### 2. 强调人工测试是基线

This is very important.
这一点非常重要。

Suggested points:
建议强调的内容：

- We first performed manual white-box test design.
- 我们首先进行了人工白盒测试设计。

- We used CFG, cyclomatic complexity, and independent path derivation.
- 我们使用了控制流图、圈复杂度和独立路径推导。

- These manual test cases serve as the baseline for later comparison.
- 这些人工测试用例构成了后续对比的基线。

- AI-generated tests are evaluated against this baseline, not blindly trusted.
- AI 生成的测试要放在这个基线上评估，而不是直接无条件相信。

Suggested line:
建议直接讲的一句话：

> Manual white-box analysis is our baseline. We first constructed CFGs, computed cyclomatic complexity, and derived independent paths before using the tool. The AI part is evaluated relative to that baseline.
> 人工白盒分析是我们的基线。在使用工具之前，我们先构建了控制流图、计算了圈复杂度，并推导了独立路径。AI 部分的效果是相对于这个基线来评估的。

### 3. Then explain what the tool actually does
### 3. 然后再解释工具到底做了什么

Do not skip the tool. But describe it as part of the testing workflow.
不要回避工具，但要把它描述成测试流程中的一部分。

Suggested tool description:
建议这样描述工具：

- The tool reads source code
- 工具读取源代码

- optionally performs AST-based structure extraction for Python
- 对 Python 可选地执行基于 AST 的结构提取

- builds prompts
- 构造提示词

- calls different LLMs
- 调用不同的 LLM

- generates candidate test cases or test scripts
- 生成候选测试用例或测试脚本

- runs coverage measurement
- 执行覆盖率测量

- performs closed-loop supplementation when coverage is insufficient
- 当覆盖率不足时执行闭环补充

- records results for comparison
- 记录实验结果并进行对比

Suggested line:
建议直接讲的一句话：

> The tool automates repetitive parts of the white-box workflow: code reading, structure extraction, candidate test generation, coverage execution, and iterative supplementation.
> 这个工具自动化了白盒测试流程中重复性的部分，包括代码读取、结构提取、候选测试生成、覆盖率执行和迭代补充。

### 4. Clearly explain what remains human work
### 4. 明确说明哪些部分仍然是人工工作

This is the part that makes the project align with the teacher's requirement.
这一部分最能体现项目与老师要求的一致性。

Human responsibilities include:
人工仍需负责的内容包括：

- selecting key target functions
- 选择关键测试目标函数

- deciding what counts as meaningful coverage
- 判断什么样的覆盖才算真正有意义

- checking whether generated test inputs are valid
- 检查生成的测试输入是否合法

- identifying false assertions and hallucinated expectations
- 识别错误断言和幻觉式预期结果

- interpreting whether high coverage is actually useful
- 判断高覆盖率是否真的有价值

- comparing manual and AI-generated results
- 对人工结果和 AI 结果进行对比分析

Suggested line:
建议直接讲的一句话：

> The tool can generate candidate tests, but humans still decide test strategy, inspect whether assertions are reasonable, and interpret whether the resulting coverage is truly meaningful.
> 工具可以生成候选测试，但测试策略、断言是否合理，以及最终覆盖率是否真正有意义，仍然需要人工来判断。

## How to connect black-box / white-box / experience-based testing
## 如何把黑盒 / 白盒 / 经验测试串起来

Even if the project mainly focuses on white-box testing, mention all three.
即使项目主要聚焦白盒测试，也要把这三类测试都提到。

### White-box testing
### 白盒测试

This is the main focus of the project.
这是项目的主要重心。

Mention:
可以提到：

- CFG construction
- 控制流图构建

- cyclomatic complexity
- 圈复杂度

- independent path design
- 独立路径设计

- statement coverage
- 语句覆盖率

- branch coverage
- 分支覆盖率

- AST-assisted structural analysis
- AST 辅助结构分析

Suggested line:
建议直接讲的一句话：

> The core of the project is white-box testing: we analyze control flow, branches, and paths, and evaluate results using statement and branch coverage.
> 本项目的核心是白盒测试：我们分析控制流、分支和路径，并通过语句覆盖率和分支覆盖率来评价结果。

### Black-box testing
### 黑盒测试

Even if black-box testing is not the primary method, it still appears in:
即使黑盒测试不是主要方法，它仍然体现在：

- input categories
- 输入类别划分

- boundary values
- 边界值

- invalid input constraints
- 非法输入约束

- requirement documents
- 需求文档

Suggested line:
建议直接讲的一句话：

> Black-box thinking still appears in our work through input partitioning, invalid input handling, and requirement-based constraints. The tool benefits from such information when prompts include requirement documents.
> 黑盒测试思维仍然体现在我们的工作中，比如输入划分、非法输入处理和需求约束。当提示词中加入需求文档时，工具也会从这些信息中受益。

### Experience-based testing
### 经验测试

This is useful when discussing discovered errors and practical limitations.
在讨论发现的问题和实际局限时，这部分很有用。

Mention examples such as:
可以举例如下：

- Dayjs float assertion issues
- Dayjs 浮点断言问题

- rounding vs flooring misunderstandings
- 四舍五入与向下取整的误解

- invalid generated inputs
- 无效生成输入

- syntax instability
- 语法不稳定

Suggested line:
建议直接讲的一句话：

> Experience-based testing is reflected in how we manually identified likely failure patterns, such as floating-point assertion errors, invalid inputs, and framework misuse in generated tests.
> 经验测试体现在我们如何人工识别可能的失败模式，例如浮点断言错误、无效输入，以及生成测试中的框架误用。

## How to answer the "coverage is high, is testing enough?" question
## 如何回答“覆盖率高是不是就说明测试足够”这个问题

Very important defense point:
这是一个非常重要的答辩点：

> High coverage does not automatically mean sufficient testing.
> 高覆盖率并不自动意味着测试已经充分。

Explain:
可以这样解释：

- coverage shows structural reach
- 覆盖率反映的是结构上触达了多少代码

- but not all executed tests are correct
- 但并不是所有执行到的测试都是正确的

- we must also check pass rate, assertion quality, and input validity
- 我们还必须看通过率、断言质量和输入有效性

- some tests can raise coverage but still be unreasonable
- 有些测试虽然提高了覆盖率，但本身仍然可能不合理

Suggested line:
建议直接讲的一句话：

> Coverage tells us how much code was reached, but not whether the tests are correct or meaningful. So we evaluate coverage together with pass rate, assertion validity, and manual review.
> 覆盖率告诉我们代码被触达了多少，但不能说明这些测试是否正确、是否有意义。因此我们会结合通过率、断言有效性和人工复核一起评价。

## How to explain manual vs AI
## 如何解释人工测试与 AI 测试的关系

Use a balanced comparison.
要用一种平衡的比较方式来讲。

### Manual testing strengths
### 人工测试的优势

- more interpretable
- 可解释性更强

- better for precise reasoning on selected paths
- 更适合对选定路径进行精确推理

- easier to explain in a teaching context
- 在教学场景中更容易说明白

### Manual testing weaknesses
### 人工测试的弱点

- time-consuming
- 耗时

- incomplete on large or complex modules
- 面对大模块或复杂模块时容易不完整

- easy to miss hidden branches
- 容易漏掉隐藏分支

- vulnerable to intuitive misunderstandings
- 容易受到直觉性误解的影响

### AI-generated testing strengths
### AI 生成测试的优势

- faster expansion of coverage
- 扩展覆盖率更快

- better at generating many candidate cases
- 更擅长批量生成候选用例

- useful for iterative supplementation
- 适合做迭代补充

- stronger on large structural search space
- 在大规模结构搜索空间中更有优势

### AI-generated testing weaknesses
### AI 生成测试的弱点

- may hallucinate expected outputs
- 可能会幻觉出错误的预期输出

- may generate invalid inputs
- 可能生成无效输入

- may misuse framework syntax
- 可能误用测试框架语法

- high coverage does not guarantee high validity
- 高覆盖率并不保证高有效性

Suggested line:
建议直接讲的一句话：

> Manual testing provides interpretability and methodological rigor, while AI testing provides scalability and coverage expansion. Our project explores how to combine them rather than replace one with the other.
> 人工测试提供可解释性和方法上的严谨性，而 AI 测试提供可扩展性和覆盖范围扩张能力。我们的项目探索的是如何把两者结合起来，而不是用一方替代另一方。

## Suggested slide-by-slide speaking strategy
## 建议的逐页讲解策略

### Slide 1: Project Background & Tool Design
### 第 1 页：项目背景与工具设计

What to say:
这一页建议讲：

- This is a testing project first, tool project second.
- 这是一个以测试为主、工具为辅的项目。

- We began from manual white-box testing methodology.
- 我们从人工白盒测试方法出发。

- The tool is designed to support that workflow.
- 工具是为了支持这条测试流程而设计的。

Suggested sentence:
建议直接讲的一句话：

> We treat the tool as an extension of the white-box testing workflow, not as a substitute for testing methodology.
> 我们把这个工具视为白盒测试流程的延伸，而不是测试方法本身的替代品。

### Slide 2: Experimental Results & Analysis
### 第 2 页：实验结果与分析

What to say:
这一页建议讲：

- We compare manual baseline and AI-generated results.
- 我们比较了人工基线和 AI 生成结果。

- We evaluate by coverage, accuracy, and test quality.
- 我们从覆盖率、准确率和测试质量三个方面进行评价。

- The goal is not only higher coverage, but better testing support.
- 我们的目标不只是更高覆盖率，而是更有效的测试支持能力。

Suggested sentence:
建议直接讲的一句话：

> Our evaluation focuses not only on structural coverage, but also on whether the generated tests are executable, logically correct, and useful.
> 我们的评估重点不仅是结构覆盖率，还包括生成的测试是否可执行、逻辑是否正确、以及是否真正有用。

### Slide 3: Challenges & Engineering Solutions
### 第 3 页：挑战与工程解决方案

What to say:
这一页建议讲：

- These are engineering issues encountered when embedding LLMs into testing.
- 这些是把 LLM 融入测试流程时遇到的工程问题。

- Some are already implemented, and some are identified as improvement directions.
- 其中有些已经实现，有些仍然属于后续改进方向。

- Be careful not to over-claim implemented features.
- 不要把尚未完全落地的内容讲成已经全部实现。

Suggested sentence:
建议直接讲的一句话：

> These challenges show that LLMs alone are not enough; robust engineering and human validation are essential in practice.
> 这些挑战说明，仅靠 LLM 本身是不够的；稳健的工程机制和人工验证在实践中是必不可少的。

### Slide 4: Conclusion & Future Work
### 第 4 页：结论与未来工作

What to say:
这一页建议讲：

- The contribution is not "AI replaces testing"
- 贡献点不是“AI 替代了测试”

- The contribution is "AI can be integrated into testing workflow"
- 真正的贡献是“AI 可以被整合进测试流程”

- Human judgment remains essential
- 人工判断仍然是必不可少的

Suggested sentence:
建议直接讲的一句话：

> Our main conclusion is that AI can effectively assist white-box testing, but testing strategy and result validation must remain human-guided.
> 我们的主要结论是，AI 可以有效辅助白盒测试，但测试策略和结果验证仍然必须由人工主导。

## A short final defense summary
## 一段简短的最终答辩总结

If time is limited, use this:
如果时间紧张，可以直接用下面这段：

> Our project is a software testing project centered on white-box methodology, with an AI-assisted tool as the implementation vehicle. We first established a manual testing baseline using CFGs, cyclomatic complexity, and independent paths, then used the tool to automate candidate test generation, coverage execution, and iterative refinement. The tool improves efficiency and coverage expansion, but humans still determine test strategy, inspect validity, and interpret whether the resulting tests are truly meaningful.
> 我们的项目本质上是一个以白盒测试方法为核心的软件测试项目，而 AI 辅助工具是它的实现载体。我们先通过控制流图、圈复杂度和独立路径建立了人工测试基线，然后再使用工具自动化候选测试生成、覆盖率执行和迭代补充。这个工具提升了效率并扩展了覆盖范围，但测试策略、有效性检查以及结果是否真正有意义，仍然由人工来决定。

## Practical advice
## 实用建议

- Do not hide the tool; it is a legitimate core contribution.
- 不要回避工具，它本身就是一个正当且重要的贡献点。

- Do not present the tool as replacing testing knowledge.
- 但不要把工具讲成在替代测试知识和测试方法。

- Use phrases like:
- 可以多使用这些表达：

  - "assist"
  - “辅助”

  - "support"
  - “支持”

  - "baseline"
  - “基线”

  - "human review"
  - “人工复核”

  - "coverage interpretation"
  - “覆盖项解释”

  - "validity judgment"
  - “有效性判断”

- If challenged, always return to:
- 如果被追问，就把回答拉回到这三点：

  - manual baseline
  - 人工基线

  - testing methodology
  - 测试方法

  - human validation
  - 人工验证
