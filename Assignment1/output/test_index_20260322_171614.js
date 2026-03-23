/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC009: parseLocale called with no preset (falsy)', () => {
    const result = index(null, null, false);
    expect(result).toBe("L (global locale, 'en')");
  });

  test('TC010: parseLocale called with a string preset that exists in Ls', () => {
    const result = index("en", null, false);
    expect(result).toBe("The locale string ('en')");
  });

  test('TC012: parseLocale called with a string preset containing hyphen, where base locale does not exist', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("Result of parseLocale('zh')");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC028: Dayjs instance method .startOf() with an unknown unit', () => {
    const result = index("unknown").startOf();
    expect(result).toBe("A clone of the original instance");
  });

  test('TC039: Dayjs instance method .add() with an unsupported unit (defaults to milliseconds)', () => {
    const result = index(500, "ms").add();
    expect(result).toBe("A new Dayjs instance advanced by 500 milliseconds");
  });

  test('TC042: Dayjs instance method .format() with specific format tokens (e.g., YYYY-MM-DD HH:mm:ss)', () => {
    const result = index("YYYY-MM-DD HH:mm:ss").format();
    expect(result).toBe("Formatted string matching the pattern");
  });

  test('TC047: Dayjs instance method .locale() getter (no preset)', () => {
    const result = index(null, null).locale();
    expect(result).toBe("Current locale string (e.g., 'en')");
  });

  test('TC048: Dayjs instance method .locale() setter with string preset', () => {
    const result = index("fr", null).locale();
    expect(result).toBe("A new Dayjs instance with $L set to 'fr'");
  });

  test('TC050: Prototype getter/setter method (e.g., .month()) called with argument (setter)', () => {
    const result = index("month", 5).month();
    expect(result).toBe("A new Dayjs instance with month set to June");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC054: Static method dayjs.unix() with a timestamp', () => {
    const result = index(1672531200).unix();
    expect(result).toBe("A Dayjs instance representing 2023-01-01 00:00:00 UTC");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_002: 测试 parseLocale：字符串 preset 包含连字符 \'-\'，且无对应 locale。应递归调用 parseLocale。', () => {
    const result = index("en-US", null, false);
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

  test('TC_SUP_001: 测试parseLocale函数中传入带连字符的语言标识且该语言未加载的情况', () => {
    const result = index("zh-CN", null);
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_005: 测试parseDate函数传入null的情况', () => {
    const result = index(null);
    expect(result).toBe("Date对象包含NaN");
  });

  test('TC_SUP_006: 测试parseDate函数中utc模式下的日期字符串解析', () => {
    const result = index("2023-01-01T12:30:45.123", true);
    expect(result).toBe("对应的UTC时间Date对象");
  });

  test('TC_SUP_007: 测试startOf函数中的instanceFactory和instanceFactorySet未覆盖分支', () => {
    const result = index("2023-01-15T14:30:45.123", "year", false);
    expect(result).toBe("当年最后一天结束的时间");
  });

  test('TC_SUP_008: 测试startOf函数中的week单位计算，包含周开始日不为0的情况', () => {
    const result = index("2023-01-15T14:30:45.123", "week");
    expect(result).toBe("当周第一天的开始时间");
  });

  test('TC_SUP_009: 测试$set函数中设置月份和年份的特殊逻辑', () => {
    const result = index("2023-01-31", "month", 1);
    expect(result).toBe("2023-02-28（防止日期溢出）");
  });

  test('TC_SUP_010: 测试$set函数中设置星期（D单位）的特殊逻辑', () => {
    const result = index("2023-01-15", "day", 1);
    expect(result).toBe("调整到星期一的日期");
  });

  test('TC_SUP_011: 测试add函数中月份和年份的加法', () => {
    const result = index("2023-01-31", 1, "month");
    expect(result).toBe("2023-02-28");
  });

  test('TC_SUP_012: 测试add函数中的instanceFactorySet逻辑', () => {
    const result = index("2023-01-15", 3, "day");
    expect(result).toBe("2023-01-18");
  });

  test('TC_SUP_013: 测试format函数的各种格式标记，包括自定义locale', () => {
    const result = index("2023-06-15T14:30:45.123", "YYYY-MM-DD dddd HH:mm:ss.SSS A");
    expect(result).toBe("2023-06-15 Thursday 14:30:45.123 PM");
  });

  test('TC_SUP_014: 测试format函数中的switch语句多个分支', () => {
    const result = index("2023-06-15T14:30:45.123", "YY M MM MMM MMMM D DD d dd ddd dddd H HH h hh a A m mm s ss SSS Z");
    expect(result).toBe("完整格式化的日期字符串");
  });

  test('TC_SUP_015: 测试diff函数的所有单位计算', () => {
    const result = index("2023-01-01", "2024-01-01", "year", true);
    expect(result).toBe("1");
  });

  test('TC_SUP_016: 测试locale方法不传preset时返回当前locale', () => {
    const result = index("2023-01-01", null);
    expect(result).toBe("en");
  });

  test('TC_SUP_018: 测试dayjs.unix方法', () => {
    const result = index(1672531200);
    expect(result).toBe("2023-01-01 00:00:00对应的Dayjs对象");
  });

  test('TC_SUP_019: 测试toDate和toString方法', () => {
    const result = index("2023-01-01T12:30:45.123Z");
    expect(result).toBe("对应的Date对象和UTC字符串");
  });

  test('TC_SUP_020: 测试utcOffset方法', () => {
    const result = index("2023-01-01T12:30:45.123");
    expect(result).toBe("当前时区偏移量（分钟）");
  });

  test('TC_SUP_021: 测试$utils方法', () => {
    const result = index("2023-01-01");
    expect(result).toBe("Utils对象");
  });
});
