# 需求文档：convert_number_to_words.py

## 功能概述
将整数转换为对应的英文单词表示，支持三种数字命名系统（短制、长制、印度制）。

## 模块组成

### 1. NumberingSystem（枚举类）
定义三种数字命名系统的单位和量级：

| 系统 | 说明 | 最大值 |
|------|------|--------|
| SHORT（短制） | 英美常用：thousand, million, billion, trillion, quadrillion | 10^18 - 1 |
| LONG（长制） | 欧洲部分国家：thousand, million, milliard, billiard | 10^21 - 1 |
| INDIAN（印度制） | 印度：thousand, lakh, crore, lakh crore, crore crore | 10^19 - 1 |

**方法**：
- `max_value(system: str) -> int`：返回指定命名系统支持的最大数值

### 2. NumberWords（枚举类）
存储英文数字单词的映射表：
- `ONES`：0-9 的英文单词（0 映射为空字符串）
- `TEENS`：10-19 的英文单词
- `TENS`：20, 30, ..., 90 的英文单词

### 3. convert_small_number(num: int) -> str
将 0-99 的非负整数转换为英文单词。

**输入要求**：
- 必须是非负整数（num >= 0）
- 必须小于 100（num < 100）

**转换规则**：
- 0 → "zero"
- 1-9 → 直接查 ONES 表（"one", "two", ...）
- 10-19 → 查 TEENS 表（"ten", "eleven", ...）
- 20-99 → 组合 TENS 和 ONES，中间用连字符 "-" 连接（如 "twenty-five"）
- 整十数无连字符（如 "twenty"，不是 "twenty-"）

**异常**：
- num < 0 → 抛出 `ValueError("This function only accepts non-negative integers")`
- num >= 100 → 抛出 `ValueError("This function only converts numbers less than 100")`

### 4. convert_number(num: int, system: str = "short") -> str
将任意整数转换为英文单词，支持指定命名系统。

**输入要求**：
- num 为整数
- system 为 "short"（默认）、"long" 或 "indian"

**转换规则**：
- 负数 → 前缀 "negative"，然后转换绝对值（如 -100 → "negative one hundred"）
- 0 → "zero"
- 超过该系统最大值 → 抛出 `ValueError("Input number is too large")`
- 按照命名系统中定义的量级从高到低拆分数字，递归转换各部分
  - 数字组 >= 100 时递归调用 `convert_number`
  - 数字组 < 100 时调用 `convert_small_number`
- 各部分用空格连接

**输出示例**：
- `convert_number(0)` → `"zero"`
- `convert_number(100)` → `"one hundred"`
- `convert_number(-100)` → `"negative one hundred"`
- `convert_number(123456789)` → `"one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine"`

## 边界条件和特殊情况

1. **零值处理**：输入 0 时，word_groups 为空，走 `num > 0 or not word_groups` 的第二个条件
2. **负数处理**：先添加 "negative"，再将 num 取绝对值
3. **最大值边界**：恰好等于 max_value 时应正常转换，max_value + 1 应抛出异常
4. **递归调用**：digit_group >= 100 时会递归调用 convert_number
5. **命名系统校验**：传入无效的 system 字符串时，`NumberingSystem[system.upper()]` 会抛出 KeyError
6. **连字符规则**：21 → "twenty-one"（有连字符），20 → "twenty"（无连字符）
7. **teens 特殊处理**：10-19 有专用单词，不是 "ten-one" 这种组合形式
