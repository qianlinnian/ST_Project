/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试无效日期输入', () => {
    expect(() => { index(null); }).toThrow();
  });

  test('TC003: 测试有效日期字符串输入', () => {
    const result = index("2023-10-01 12:00:00");
    expect(result).toBe("有效日期对象");
  });

  test('TC004: 测试UTC日期字符串输入', () => {
    const result = index("2023-10-01T12:00:00Z");
    expect(result).toBe("有效UTC日期对象");
  });

  test('TC005: 测试Dayjs实例克隆', () => {
    const result = index("2023-10-01 12:00:00");
    expect(result).toBe("克隆的Dayjs实例");
  });

  test('TC006: 测试语言解析 - 已加载语言', () => {
    const result = index("en");
    expect(result).toBe("en");
  });

  test('TC007: 测试语言解析 - 未加载语言', () => {
    const result = index("fr");
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC009: 测试日期加法', () => {
    const result = index("2023-10-01", 5, "D");
    expect(result).toBe("2023-10-06");
  });

  test('TC010: 测试日期减法', () => {
    const result = index("2023-10-01", 5, "D");
    expect(result).toBe("2023-09-26");
  });

  test('TC011: 测试日期比较 - isSame', () => {
    const result = index("2023-10-01", "2023-10-01", "D");
    expect(result).toBe(true);
  });

  test('TC012: 测试日期比较 - isAfter', () => {
    const result = index("2023-10-01", "2023-09-30", "D");
    expect(result).toBe(true);
  });

  test('TC013: 测试日期比较 - isBefore', () => {
    const result = index("2023-09-30", "2023-10-01", "D");
    expect(result).toBe(true);
  });

  test('TC014: 测试格式化无效日期', () => {
    expect(() => { index(null, "YYYY-MM-DD"); }).toThrow();
  });

  test('TC015: 测试格式化有效日期', () => {
    const result = index("2023-10-01", "YYYY-MM-DD");
    expect(result).toBe("2023-10-01");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串类型的 preset，且存在于 Ls 中', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，传入字符串类型的 preset，且不存在于 Ls 中', () => {
    const result = index("fr", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_008: 测试 Dayjs 类的 startOf 方法，传入 \'day\' 单位', () => {
    const result = index("day", true);
    expect(result).toBe("Dayjs instance");
  });

  test('TC_SUP_009: 测试 Dayjs 类的 endOf 方法，传入 \'day\' 单位', () => {
    const result = index("day");
    expect(result).toBe("Dayjs instance");
  });

  test('TC_SUP_010: 测试 Dayjs 类的 format 方法，传入无效日期', () => {
    expect(() => { index(null); }).toThrow();
  });

  test('TC_SUP_013: 测试 Dayjs 类的 toString 方法', () => {
    const result = index();
    expect(result).toBe("string");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串类型的 preset，且 Ls 中没有该 locale', () => {
    const result = index("fr", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，传入字符串类型的 preset，且 Ls 中存在该 locale', () => {
    const result = index("en", null, false);
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

  test('TC_SUP_008: 测试 Dayjs 类的 startOf 方法，传入 \'month\'', () => {
    const result = index("month", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_009: 测试 Dayjs 类的 endOf 方法，传入 \'day\'', () => {
    const result = index("day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_010: 测试 Dayjs 类的 format 方法，传入无效日期', () => {
    expect(() => { index("YYYY-MM-DD"); }).toThrow();
  });

  test('TC_SUP_013: 测试 Dayjs 类的 toString 方法', () => {
    const result = index();
    expect(result).toBe("UTC 字符串");
  });
});
