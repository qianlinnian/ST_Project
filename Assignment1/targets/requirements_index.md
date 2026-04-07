# Requirements Document: index.js (Day.js Core Module)

## Overview
Day.js is a lightweight date and time manipulation library that provides an API similar to Moment.js.
This file is the core module of Day.js and contains the core functionality for date parsing, formatting, comparison, and calculation.

## Module Structure

### 1. Global State Management

- `L`: global default language (initial value: `"en"`)
- `Ls`: loaded locale objects (keyed by language name, value is the locale configuration)

### 2. Helper Functions

#### isDayjs(d) -> boolean
Determines whether an object is a Dayjs instance.
- The check is performed via `instanceof Dayjs` or the `d.$isDayjsObject` flag

#### parseLocale(preset, object, isLocal) -> string
Parses and sets the locale.
- When `preset` is a string: tries to find a loaded locale pack, with support for automatic fallback from `"zh-cn"` to `"zh"`
- When `preset` is an object: registers it directly as a locale pack
- When `isLocal` is false: updates the global default locale

#### parseDate(cfg) -> Date
Parses various date inputs into a JavaScript Date object.
- `null` → `new Date(NaN)` (invalid date)
- `undefined` → `new Date()` (current time)
- `Date` object → clone it
- String → use the regular expression `REGEX_PARSE` to match the `"YYYY-MM-DD HH:mm:ss.SSS"` format
  - Supports both UTC mode and local mode
  - Only strings that do not end with `"Z"` are matched by the regex
- Others → passed to `new Date()` (for example, timestamps)

### 3. dayjs(date, c) Factory Function
The entry function for creating Dayjs instances.
- If `date` is already a Dayjs instance, return a clone of it
- Otherwise, create a new Dayjs instance

### 4. Dayjs Class

#### Construction and Initialization
- `constructor(cfg)`: parses locale settings and calls parse initialization
- `parse(cfg)`: parses the date via `parseDate`, then calls `init`
- `init()`: extracts year, month, day, weekday, hour, minute, second, and millisecond from the Date object

#### Query Methods
- `isValid()`: determines whether the date is valid (by checking whether `toString()` is `"Invalid Date"`)
- `isSame(that, units)`: checks whether it is the same as another date (up to the specified unit)
- `isAfter(that, units)`: checks whether it is after another date
- `isBefore(that, units)`: checks whether it is before another date

#### Get/Set Methods
- `$g(input, get, set)`: general getter/setter proxy
- `get(unit)`: gets the value of the specified unit (year/month/day/hour/minute/second/millisecond)
- `set(string, int)`: sets the value of the specified unit (returns a new instance)
- `$set(units, int)`: internal set method (modifies the current instance directly)
  - Month/year updates require special handling to prevent date overflow (for example, when setting January 31 to February, use `min(31, 28)`)

#### Calculation Methods
- `add(number, units)`: date addition
  - Month/year: set via `set`
  - Day/week: calculated by days
  - Hour/minute/second: calculated by milliseconds
- `subtract(number, string)`: date subtraction (internally calls `add` with the sign reversed)
- `diff(input, units, float)`: calculates the difference between two dates
  - Supports year/month/quarter/week/day/hour/minute/second/millisecond units
  - The `float` parameter controls whether a floating-point result is returned
  - Considers timezone differences (`zoneDelta`)

#### Range Methods
- `startOf(units)`: gets the start time of a specified unit (for example, start of month, start of year, Monday for week)
  - The start day of the week is determined by the locale's `weekStart` setting
- `endOf(arg)`: gets the end time of a specified unit (for example, month end at `23:59:59.999`)
- `daysInMonth()`: gets the number of days in the current month

#### Formatting Methods
- `format(formatStr)`: outputs the date according to a format string
  - Supported format tokens: `YY`, `YYYY`, `M`, `MM`, `MMM`, `MMMM`, `D`, `DD`, `d`, `dd`, `ddd`, `dddd`, `H`, `HH`, `h`, `hh`, `a`, `A`, `m`, `mm`, `s`, `ss`, `SSS`, `Z`, `ZZ`
  - Invalid dates return `locale.invalidDate` or `"Invalid Date"`
  - Characters inside square brackets are output as-is (escaped)

#### Output Methods
- `valueOf()`: returns the millisecond timestamp
- `unix()`: returns the second-level timestamp
- `toDate()`: returns a native Date object
- `toJSON()`: returns an ISO string for valid dates, null for invalid dates
- `toISOString()`: returns an ISO 8601 string
- `toString()`: returns a UTC string

#### Locale-Related Methods
- `$locale()`: gets the current instance's locale configuration object
- `locale(preset, object)`: switches locale (returns a new instance)
- `clone()`: clones the current instance

### 5. Prototype Method Registration
Shortcuts are registered on the Dayjs prototype in a loop:
- `millisecond()`, `second()`, `minute()`, `hour()`, `day()`, `month()`, `year()`, `date()`
- These methods act as getters when called without arguments and setters when called with arguments

### 6. Static Methods
- `dayjs.extend(plugin, option)`: registers a plugin (each plugin is installed only once)
- `dayjs.locale(preset)`: sets the global locale
- `dayjs.isDayjs(d)`: checks whether the input is a Dayjs instance
- `dayjs.unix(timestamp)`: creates an instance from a second-level timestamp

## Boundary Conditions and Special Cases

1. **Invalid date**: `dayjs(null)` creates an invalid date, and `isValid()` returns false
2. **Timezone handling**: `utcOffset()` rounds timezone offsets to the nearest 15 minutes (fix for the FF24 browser bug)
3. **Month-end overflow**: when setting the month and the day overflows (for example, setting February from the 31st), automatically use the last day of that month
4. **Week start day**: `startOf('week')` depends on the locale's `weekStart` setting (for example, Monday in Chinese, Sunday in English)
5. **String parsing**: strings ending with `"Z"` do not go through regex matching; they are passed directly to `new Date()`
6. **Plugin deduplication**: `extend` uses the `plugin.$i` flag to prevent repeated installation
7. **Timezone correction in diff**: timezone differences between the two dates are considered when calculating the difference