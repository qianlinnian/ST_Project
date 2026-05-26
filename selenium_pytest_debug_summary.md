# Selenium + pytest 完整脚本调试过程总结

## 1. 起点：补充完整 optimized suite 自动化脚本

最开始的目标是基于 AutoTestDesign 导出的 `todoitem_optimized_test_suite.csv`，把 Todo Item Management 的 optimized test suite 映射成 Selenium + pytest 自动化脚本。

核心目标包括：

- 使用 pytest 执行测试。
- 使用 Selenium WebDriver 操作 UI。
- 封装 Page Object 基础操作，例如 add、toggle、edit、delete、filter、clear completed。
- 将 optimized suite 中的 57 个测试用例映射到 pytest 参数化测试中。
- 额外增加 1 个 guardrail 测试，用来确认 `CASES` 中确实包含 57 个 optimized test cases。

因此最终 pytest 收集到的测试项数量是：

```text
57 个 optimized test cases + 1 个 completeness guardrail = 58 个 pytest items
```

## 2. 最初的问题：自动化覆盖补全后仍有失败

完整脚本补充后，运行结果一开始不是全部通过，而是出现若干失败。最初的主要失败集中在：

- edit empty title 相关测试。
- whitespace-only input 相关测试。
- toggle all empty / invalid control 相关测试。
- clear completed 按钮不可交互相关问题。

后来逐步确认：

- 手工测试中，删除标题为空后 item 会消失，因此 edit empty title 不是产品缺陷，而是 Selenium 清空输入框动作不稳定。
- whitespace-only 是否属于缺陷需要根据产品当前实现判断；如果当前实现已经修复，则不应继续标记为 xfail。
- toggle all empty / invalid control 的失败主要不是功能错误，而是测试前置状态没有清理干净。

## 3. 关于 edit empty title 的判断

一开始曾经把 `edit title to empty should delete item` 判断为产品缺陷，并建议标记为 `xfail`。

后来你手工验证发现：

```text
把 Todo 标题删空后，item 确实会消失。
```

因此修正判断：

```text
这是 Selenium 脚本没有稳定模拟“清空输入框并保存”的问题，不是产品功能缺陷。
```

后来对 `edit()` 方法做了更稳定的处理，例如：

- 双击 label 进入编辑模式。
- 等待 `.edit` 输入框可点击。
- 使用 Ctrl+A + Backspace 清空旧文本。
- 如果新标题非空则输入新文本。
- 按 Enter 保存。
- 增加 retry，降低 `element not interactable` 或 stale element 的概率。

最终 edit 相关测试通过。

## 4. 关于 pytest 输出日志的保存

由于 pytest 输出太长，直接粘贴聊天容易被截断，因此建议使用重定向保存完整日志：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py -q -rA --tb=short > pytest_full_output.txt 2>&1
```

或者边显示边保存：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py -q -rA --tb=short 2>&1 | Tee-Object -FilePath pytest_full_output.txt
```

后续你多次上传 `pytest_full_output.txt`，我们根据完整日志定位剩余失败。

## 5. toggle-all 相关 helper 的讨论

脚本中原本有：

```python
def toggle_all_once(self):
    self.driver.find_element(By.ID, "toggle-all").click()
    time.sleep(0.3)


def toggle_all_to_completed(self):
    self.toggle_all_once()
    self.wait.until(lambda _: self.visible_count() > 0 and all(self.completed_flags()))
```

后来新增了：

```python
def toggle_all_if_present(self):
    ...
```

这个 helper 的作用是：

```text
如果 toggle-all 控件存在并且可点击，就点击；
如果不存在、隐藏或不可点击，就返回 False，不让测试崩溃。
```

它主要用于空列表 / invalid control 场景，而不是正常 toggle all 功能场景。

正常功能仍使用：

```python
toggle_all_to_completed()
toggle_all_once()
```

## 6. TC-036 和 TC-052 到底想测试什么

后续重点调试的是两个测试：

```text
TC-036_toggle_all_core_invalid_empty
TC-052_toggle_all_control_invalid
```

它们都复用了：

```python
def s_toggle_all_empty_safe(page):
    ...
```

### TC-036

TC-036 属于：

```text
TS-004 Equivalence Partitioning for core behavior
COV-018 Verify core behavior: toggle all
```

它想验证：

```text
当列表为空时，toggle-all 核心行为不应该导致应用崩溃，也不应该凭空创建 item。
```

### TC-052

TC-052 属于：

```text
TS-005 Equivalence Partitioning for inputs
COV-019 Test input field/control with valid and invalid data
```

它想验证：

```text
当 toggle-all control 处于 invalid / unavailable / empty-list 状态时，应用仍然安全。
```

这两个测试的关注点不同，但 UI 可观察行为相似，所以可以共用一个 scenario。

## 7. 为什么空列表下没有 Mark all as complete

你截图确认了：当 Todo list 为空时，页面上没有：

```text
Mark all as complete
All / Active / Completed
Clear completed
items left
```

因此空列表下的合理预期是：

```text
toggle-all 控件不存在或不可点击；
尝试安全点击 toggle-all 应返回 False；
列表仍然为空；
应用仍然可用。
```

因此 `s_toggle_all_empty_safe()` 的语义应是：

```python
def s_toggle_all_empty_safe(page):
    page.assert_count(0)
    clicked = page.toggle_all_if_present()
    assert clicked is False
    page.assert_count(0)
    page.assert_app_still_usable()
```

不过在全套运行时，必须先保证每个测试开始前确实是空列表。

## 8. 真正的核心问题：测试之间状态没有隔离

单独跑 TC-036 / TC-052 时可以通过，但跑完整套时出现很多失败。这说明核心问题不是单个 case 的逻辑，而是：

```text
测试之间存在状态污染。
```

进一步调试发现：

```text
reset_todos() 执行后，页面中的 item 没有消失。
```

调试输出中出现过：

```text
count before: 4
texts before: ['completed item', 'active item', 'completed item', 'Buy milk']
count after reset: 4
texts after reset: ['completed item', 'active item', 'completed item', 'Buy milk']
toggle-all count: 1
```

这说明：

```text
reset_todos() 没有清掉当前页面 test-list 中实际显示的 todos。
```

结合 Codex 对代码的分析，当前应用功能上主要使用 `ApiStorage` 和后端 API，但 `Todo` 构造函数中仍残留一次 `new Storage()` 和 `createStore()` 的 localStorage 初始化行为。

不过从调试结果看，主要问题更可能是：

```text
reset_todos() 清理的 API 范围，与页面当前 test-list 的数据范围不完全一致。
```

也就是说：

```text
页面显示的是 test-list 下的 todos，
但 reset_todos() 可能只清理了 /api/todos，
没有准确清理当前 list scope。
```

## 9. 为什么改用 UI 清理是合理的

后来为了保证测试隔离，采用了 UI 层清理：

```python
def clear_all_items_via_ui(self):
    """
    Clear all currently visible Todo items using delete buttons only.
    Used only by empty-list boundary tests or test isolation setup.
    """
    try:
        self.filter_all()
    except Exception:
        pass

    for _ in range(50):
        items = self.visible_items()
        if not items:
            return

        before = len(items)
        item = items[0]

        ActionChains(self.driver).move_to_element(item).perform()
        time.sleep(0.1)

        destroy = item.find_element(By.CSS_SELECTOR, ".destroy")
        self.driver.execute_script("arguments[0].click();", destroy)

        self.wait.until(lambda _: self.visible_count() < before)

    self.wait.until(lambda _: self.visible_count() == 0)
```

这个方法的作用是：

```text
不依赖后端 reset_todos() 是否清对了 list scope；
直接删除当前 UI 上实际可见的 items；
保证下一个测试从空列表开始。
```

这不是“耍小聪明”，而是测试自动化中的 test isolation / setup cleanup。只要它不替代被测动作的断言，就合理。

报告中可以这样解释：

```text
Due to list-scoped API cleanup limitations during automation setup, UI-level cleanup was used before each test to guarantee test isolation. This cleanup is not part of the test oracle; it is only a setup step to ensure that each automated case starts from a known empty Todo list.
```

中文：

```text
由于当前后端清理接口与页面中的 test-list 数据范围不完全一致，单纯调用 reset_todos() 不能稳定清空当前列表。为保证自动化测试之间互不污染，脚本在每个测试开始前通过 UI 删除当前可见 Todo items，从而建立稳定的空列表前置状态。该操作仅作为测试环境准备步骤，不作为被测功能通过与否的判定依据。
```

## 10. UI 清理为什么一开始也失败过

最初尝试 UI 清理时，使用的是：

```text
Mark all as complete -> Clear completed
```

这个流程在功能测试中可以工作，但作为全局清理 helper 不够稳定，因为：

- 页面可能有残留 item。
- 当前 filter 状态可能不是 All。
- 有的 item 可能 active，有的 completed。
- Clear completed 按钮可能还没出现。
- `clear_completed_if_present()` 如果没点到按钮，只返回 False，不会让清理立即失败。
- 后续仍然等待 `visible_count() == 0`，导致 Timeout。

因此后来改成逐个点击 `.destroy` 删除当前可见 item。逐个删除更慢，但更适合做测试前置清理，因为它不依赖 completed 状态，也不依赖 Clear completed 按钮。

## 11. Clear completed 功能有没有被真正测试

有。Clear completed 不是靠 UI 清理偶然通过，脚本中有独立测试。

### 混合 active + completed 场景

```python
def s_clear_completed_keeps_active(page):
    page.add_many("active item", "done item")
    page.toggle("done item")
    page.clear_completed()
    page.assert_visible(["active item"], [False])
    assert page.active_count_text() == "1 item left"
```

这个测试验证：

```text
Clear completed 删除 completed item，同时保留 active item。
```

### 全部 completed 场景

```python
def s_clear_completed_all_completed_empty(page):
    page.add_many("done 1", "done 2")
    page.toggle("done 1")
    page.toggle("done 2")
    page.clear_completed()
    page.assert_count(0)
```

这个测试验证：

```text
当所有 item 都 completed 时，Clear completed 后列表变为空。
```

### 没有 completed item 的负向场景

```python
def s_clear_completed_none_safe(page):
    page.add_many("active 1", "active 2")
    page.clear_completed_if_present()
    page.assert_visible(["active 1", "active 2"], [False, False])
    assert page.active_count_text() == "2 items left"
```

这个测试验证：

```text
没有 completed item 时，Clear completed 不应误删 active item。
```

因此 Clear completed 功能是被专门测试过的，不是靠 setup cleanup 混过去。

## 12. 为什么 Clear completed 可以删 item，但之前清理时会报错

原因是：

```text
作为测试主体时，测试自己创建数据、自己标记 completed、自己点击 Clear completed，状态明确，所以稳定。

作为全局清理 helper 时，页面状态可能是前一个测试残留的，不确定当前 filter、completed 状态和按钮可用性，所以直接靠 Clear completed 清理不稳定。
```

所以：

```text
Clear completed 功能本身没问题；
之前报错是因为把它拿来做全局清理时，前置状态和按钮可用性不稳定。
```

## 13. 最终修复策略

最终思路是：

```text
1. 每个测试开始前，先尝试 reset_todos()。
2. 打开当前 test-list 页面。
3. 如果页面上仍然有残留 item，就通过 UI 逐个点击 destroy 删除。
4. 确认页面为空。
5. 每个 scenario 再自己创建测试数据并执行被测动作。
```

关键点是：

```text
UI 清理只作为测试隔离，不作为测试断言的一部分。
每个功能测试仍然自己创建数据、执行动作、验证结果。
```

## 14. 最终执行结果

最终运行完整脚本：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

结果为：

```text
collected 58 items
Assignment2\tests\test_todoitem_ui_selenium_full.py ................. [ 29%]
.........................................                             [100%]

====================== 58 passed in 117.05s (0:01:57) ======================
```

这说明：

```text
57 个 optimized test cases 全部执行通过；
1 个 coverage-completeness guardrail 测试通过；
没有 failed；
没有 skipped；
没有 xfailed；
没有 xpassed。
```

## 15. 可以放进报告的总结

```text
The Selenium + pytest script maps all 57 optimized AutoTestDesign test cases for the Todo Item Management feature, plus one guardrail test that verifies mapping completeness. During debugging, the main issue was not the functional behavior itself, but test isolation: the backend reset helper did not reliably clear the current list-scoped Todo data shown in the UI. To ensure each case starts from a deterministic empty list, the final script performs UI-level cleanup before each test by deleting any visible Todo items. This cleanup is treated only as test setup and is not used as a test oracle.

After improving test isolation and stabilizing UI actions such as edit, toggle-all, and clear-completed flows, the final execution collected 58 pytest items and all 58 passed successfully. This demonstrates that the automated implementation fully executes the optimized test suite mapping for the selected Todo Item Management feature.
```

中文版本：

```text
最终 Selenium + pytest 脚本映射了 Todo Item Management 的 57 个 AutoTestDesign 优化测试用例，并额外包含 1 个用于检查映射完整性的 guardrail 测试。调试过程中发现，主要问题不是功能行为本身，而是测试隔离不稳定：后端 reset_todos() 没有可靠清空当前页面 test-list 中实际显示的 Todo 数据。因此最终脚本在每个测试开始前通过 UI 删除当前可见 Todo items，确保每个测试从确定的空列表状态开始。该 UI 清理仅作为测试环境准备步骤，不作为测试通过与否的判定依据。

在修复测试隔离并稳定 edit、toggle-all、clear-completed 等 UI 操作后，最终 pytest 共收集 58 个测试项，并全部通过。这表明自动化脚本已经完整执行了针对 Todo Item Management 的 optimized test suite 映射。
```
