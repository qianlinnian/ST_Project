# 需求文档：index.js（Day.js 核心模块）

## 功能概述
Day.js 是一个轻量级的日期时间处理库，提供类似 Moment.js 的 API。
本文件是 Day.js 的核心模块，包含日期解析、格式化、比较、计算等核心功能。

## 模块组成

### 1. 全局状态管理

- `L`：全局默认语言（初始值 `"en"`）
- `Ls`：已加载的语言包对象（键为语言名，值为语言配置）

### 2. 辅助函数

#### isDayjs(d) -> boolean
判断一个对象是否是 Dayjs 实例。
- 通过 `instanceof Dayjs` 或 `d.$isDayjsObject` 标记判断

#### parseLocale(preset, object, isLocal) -> string
解析并设置语言。
- `preset` 为字符串时：尝试查找已加载的语言包，支持 "zh-cn" 自动回退到 "zh"
- `preset` 为对象时：直接注册为语言包
- `isLocal` 为 false 时会更新全局默认语言

#### parseDate(cfg) -> Date
将各种类型的日期输入解析为 JavaScript Date 对象。
- `null` → `new Date(NaN)`（无效日期）
- `undefined` → `new Date()`（当前时间）
- `Date` 对象 → 克隆一份
- 字符串 → 用正则 `REGEX_PARSE` 匹配 "YYYY-MM-DD HH:mm:ss.SSS" 格式
  - 支持 UTC 模式和本地模式
  - 不以 "Z" 结尾的字符串才尝试正则匹配
- 其他 → 交给 `new Date()` 处理（如时间戳数字）

### 3. dayjs(date, c) 工厂函数
创建 Dayjs 实例的入口函数。
- 如果 date 已经是 Dayjs 实例，返回其克隆
- 否则创建新的 Dayjs 实例

### 4. Dayjs 类

#### 构造与初始化
- `constructor(cfg)`：解析语言设置，调用 parse 初始化
- `parse(cfg)`：调用 parseDate 解析日期，然后 init
- `init()`：从 Date 对象提取年、月、日、星期、时、分、秒、毫秒

#### 查询方法
- `isValid()`：判断日期是否有效（通过 toString 是否为 "Invalid Date"）
- `isSame(that, units)`：判断是否与另一个日期相同（精确到指定单位）
- `isAfter(that, units)`：判断是否在另一个日期之后
- `isBefore(that, units)`：判断是否在另一个日期之前

#### 获取/设置方法
- `$g(input, get, set)`：通用 getter/setter 代理
- `get(unit)`：获取指定单位的值（年/月/日/时/分/秒/毫秒）
- `set(string, int)`：设置指定单位的值（返回新实例）
- `$set(units, int)`：内部设置方法（直接修改当前实例）
  - 月份/年份设置时需特殊处理（防止日期溢出，如 1月31日 设置月份为2月时取 min(31, 28)）

#### 计算方法
- `add(number, units)`：日期加法
  - 月/年：通过 set 设置
  - 日/周：通过天数计算
  - 时/分/秒：通过毫秒时间戳计算
- `subtract(number, string)`：日期减法（内部调用 add 取反）
- `diff(input, units, float)`：计算两个日期的差值
  - 支持年/月/季度/周/日/时/分/秒/毫秒单位
  - `float` 参数控制是否返回浮点数
  - 考虑时区差异（zoneDelta）

#### 范围方法
- `startOf(units)`：获取指定单位的起始时间（如月初、年初、周一）
  - 周的起始日由语言包的 `weekStart` 配置决定
- `endOf(arg)`：获取指定单位的结束时间（如月末 23:59:59.999）
- `daysInMonth()`：获取当月天数

#### 格式化方法
- `format(formatStr)`：按格式字符串输出日期
  - 支持的格式符：YY, YYYY, M, MM, MMM, MMMM, D, DD, d, dd, ddd, dddd, H, HH, h, hh, a, A, m, mm, s, ss, SSS, Z, ZZ
  - 无效日期返回 `locale.invalidDate` 或 "Invalid Date"
  - 方括号内的字符原样输出（转义）

#### 输出方法
- `valueOf()`：返回毫秒时间戳
- `unix()`：返回秒级时间戳
- `toDate()`：返回原生 Date 对象
- `toJSON()`：有效日期返回 ISO 字符串，无效返回 null
- `toISOString()`：返回 ISO 8601 格式字符串
- `toString()`：返回 UTC 字符串

#### 语言相关
- `$locale()`：获取当前实例的语言配置对象
- `locale(preset, object)`：切换语言（返回新实例）
- `clone()`：克隆当前实例

### 5. 原型方法注册
通过循环为 Dayjs 原型注册快捷方法：
- `millisecond()`, `second()`, `minute()`, `hour()`, `day()`, `month()`, `year()`, `date()`
- 这些方法既是 getter（无参数时）也是 setter（有参数时）

### 6. 静态方法
- `dayjs.extend(plugin, option)`：注册插件（每个插件只安装一次）
- `dayjs.locale(preset)`：全局设置语言
- `dayjs.isDayjs(d)`：判断是否为 Dayjs 实例
- `dayjs.unix(timestamp)`：从秒级时间戳创建实例

## 边界条件和特殊情况

1. **无效日期**：`dayjs(null)` 创建无效日期，`isValid()` 返回 false
2. **时区处理**：`utcOffset()` 对时区偏移量按 15 分钟取整（修复 FF24 浏览器 bug）
3. **月末溢出**：设置月份时如果日期溢出（如 31日设为2月），自动取该月最后一天
4. **周起始日**：`startOf('week')` 依赖语言包配置的 `weekStart`（如中文为周一，英文为周日）
5. **字符串解析**：以 "Z" 结尾的字符串不走正则匹配，直接交给 `new Date()` 处理
6. **插件去重**：`extend` 通过 `plugin.$i` 标记防止重复安装
7. **diff 时区修正**：计算差值时考虑两个日期的时区差异
