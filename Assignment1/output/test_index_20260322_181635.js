/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试无效日期创建', () => {
    expect(() => { index(null); }).toThrow();
  });

  test('TC003: 测试有效日期创建', () => {
    const result = index("2023-10-01");
    expect(result).toBe("有效的 Date 对象");
  });

  test('TC004: 测试字符串解析为 Date', () => {
    const result = index("2023-10-01 10:20:30");
    expect(result).toBe("有效的 Date 对象");
  });

  test('TC005: 测试 Dayjs 实例克隆', () => {
    const result = index("2023-10-01");
    expect(result).toBe("克隆的 Dayjs 实例");
  });

  test('TC006: 测试语言解析为已加载语言', () => {
    const result = index("en");
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC008: 测试日期加法', () => {
    const result = index("2023-10-01", 5, "D");
    expect(result).toBe("2023-10-06");
  });

  test('TC009: 测试日期减法', () => {
    const result = index("2023-10-01", 5, "D");
    expect(result).toBe("2023-09-26");
  });

  test('TC010: 测试日期比较', () => {
    const result = index("2023-10-01", "2023-10-02", "D");
    expect(result).toBe("false");
  });

  test('TC011: 测试格式化无效日期', () => {
    expect(() => { index(null, "YYYY-MM-DD"); }).toThrow();
  });

  test('TC012: 测试获取年份', () => {
    const result = index("2023-10-01", "year");
    expect(result).toBe(2023);
  });

  test('TC013: 测试设置月份溢出', () => {
    const result = index("2023-01-31", "month", 2);
    expect(result).toBe("2023-02-28");
  });

  test('TC014: 测试时区偏移', () => {
    const result = index("2023-10-01T00:00:00Z");
    expect(result).toBe("0");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串参数且存在于 Ls 中', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，传入字符串参数且不存在于 Ls 中', () => {
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

  test('TC_SUP_007: 测试 startOf 函数，传入 \'month\'', () => {
    const result = index("month", true);
    expect(result).toBe("Dayjs instance");
  });

  test('TC_SUP_008: 测试 format 函数，传入无效日期', () => {
    expect(() => { index("YYYY-MM-DD"); }).toThrow();
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串并检查 locale 赋值', () => {
    const result = index("fr", null, false);
    expect(result).toBe("fr");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_007: 测试 Dayjs 类的 startOf 方法，传入 \'month\'', () => {
    const result = index("month", true);
    expect(result).toBe("Dayjs instance at start of month");
  });

  test('TC_SUP_008: 测试 Dayjs 类的 format 方法，传入格式字符串', () => {
    const result = index("YYYY-MM-DD");
    expect(result).toBe("formatted date string");
  });

  test('TC_SUP_009: 测试 Dayjs 类的 clone 方法', () => {
    const result = index();
    expect(result).toBe("Cloned Dayjs instance");
  });
});
