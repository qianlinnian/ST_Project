# Requirements Document: convert_number_to_words.py

## Overview
Convert integers into their corresponding English word representation, supporting three numbering systems (short, long, and Indian).

## Module Structure

### 1. NumberingSystem (Enum Class)
Defines the units and magnitudes of the three numbering systems:

| System | Description | Maximum Value |
|--------|-------------|---------------|
| SHORT | Commonly used in English-speaking countries: thousand, million, billion, trillion, quadrillion | 10^18 - 1 |
| LONG | Used in some European countries: thousand, million, milliard, billiard | 10^21 - 1 |
| INDIAN | Used in India: thousand, lakh, crore, lakh crore, crore crore | 10^19 - 1 |

**Method**:
- `max_value(system: str) -> int`: returns the maximum supported value for the specified numbering system

### 2. NumberWords (Enum Class)
Stores the mapping tables for English number words:
- `ONES`: English words for 0-9 (`0` maps to an empty string)
- `TEENS`: English words for 10-19
- `TENS`: English words for 20, 30, ..., 90

### 3. convert_small_number(num: int) -> str
Converts a non-negative integer from 0 to 99 into English words.

**Input requirements**:
- Must be a non-negative integer (`num >= 0`)
- Must be less than 100 (`num < 100`)

**Conversion rules**:
- `0` → `"zero"`
- `1-9` → directly look up the ONES table (`"one"`, `"two"`, ...)
- `10-19` → look up the TEENS table (`"ten"`, `"eleven"`, ...)
- `20-99` → combine TENS and ONES with a hyphen `"-"` (for example, `"twenty-five"`)
- Exact tens do not use a trailing hyphen (for example, `"twenty"`, not `"twenty-"`)

**Exceptions**:
- `num < 0` → raise `ValueError("This function only accepts non-negative integers")`
- `num >= 100` → raise `ValueError("This function only converts numbers less than 100")`

### 4. convert_number(num: int, system: str = "short") -> str
Converts any integer into English words with support for a specified numbering system.

**Input requirements**:
- `num` must be an integer
- `system` must be one of `"short"` (default), `"long"`, or `"indian"`

**Conversion rules**:
- Negative numbers → prefix with `"negative"`, then convert the absolute value (for example, `-100` → `"negative one hundred"`)
- `0` → `"zero"`
- Numbers larger than the maximum supported by the selected system → raise `ValueError("Input number is too large")`
- Split the number from high to low according to the magnitudes defined in the numbering system and recursively convert each part
  - Digit groups `>= 100` are converted recursively via `convert_number`
  - Digit groups `< 100` are converted via `convert_small_number`
- Join the parts with spaces

**Output examples**:
- `convert_number(0)` → `"zero"`
- `convert_number(100)` → `"one hundred"`
- `convert_number(-100)` → `"negative one hundred"`
- `convert_number(123456789)` → `"one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine"`

## Boundary Conditions and Special Cases

1. **Zero handling**: when the input is `0`, `word_groups` is empty, so the second condition in `num > 0 or not word_groups` is taken
2. **Negative number handling**: add `"negative"` first, then take the absolute value of `num`
3. **Maximum-value boundary**: a value exactly equal to `max_value` should convert normally; `max_value + 1` should raise an exception
4. **Recursive calls**: digit groups `>= 100` trigger recursive calls to `convert_number`
5. **Numbering system validation**: if an invalid `system` string is passed, `NumberingSystem[system.upper()]` raises a `KeyError`
6. **Hyphen rule**: `21` → `"twenty-one"` (with hyphen), `20` → `"twenty"` (without hyphen)
7. **Teens special handling**: `10-19` have dedicated words and are not formed as combinations such as `"ten-one"`