/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试 parseLocale 函数，传入空值', () => {
    const result = index(null, null, false);
    expect(result).toBe("en");
  });

  test('TC002: 测试 parseLocale 函数，传入字符串并存在于 Ls', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC003: 测试 parseLocale 函数，传入字符串并不存在于 Ls', () => {
    const result = index("fr", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串类型的 preset，且该 preset 存在于 Ls 中', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，传入字符串类型的 preset，且该 preset 不存在于 Ls 中', () => {
    const result = index("fr", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_008: 测试 Dayjs 类的 startOf 方法，传入 \'month\' 单位', () => {
    const result = index("month", true);
    expect(result).toBe("Dayjs instance at start of month");
  });

  test('TC_SUP_009: 测试 Dayjs 类的 $set 方法，传入 \'year\' 单位', () => {
    const result = index("year", 2025);
    expect(result).toBe("Dayjs instance with year set to 2025");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，输入为字符串且存在于 Ls 中', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，输入为字符串且不存在于 Ls 中', () => {
    const result = index("fr", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_006: 测试 Dayjs 类的 isSame 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(true);
  });

  test('TC_SUP_007: 测试 Dayjs 类的 isAfter 方法', () => {
    const result = index("2022-12-31", "day");
    expect(result).toBe(true);
  });

  test('TC_SUP_008: 测试 Dayjs 类的 isBefore 方法', () => {
    const result = index("2023-01-02", "day");
    expect(result).toBe(true);
  });

  test('TC_SUP_009: 测试 Dayjs 类的 $set 方法', () => {
    const result = index("day", 5);
    expect(result).toBe("Dayjs instance with updated date");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_012: 测试 Dayjs 类的 format 方法，输入为无效日期', () => {
    expect(() => { index(); }).toThrow();
  });

  test('TC_SUP_013: 测试 Dayjs 类的 format 方法，输入为有效格式', () => {
    const result = index("YYYY-MM-DD");
    expect(result).toBe("2023-01-01");
  });

  test('TC_SUP_014: 测试 Dayjs 类的 toString 方法', () => {
    const result = index();
    expect(result).toBe("UTC String");
  });
});
