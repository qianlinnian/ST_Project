/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC002: 测试 dayjs 函数传入 null 日期', () => {
    const result = index(null);
    expect(result).toBe("一个表示无效日期的 Dayjs 对象");
  });

  test('TC005: 测试 dayjs 函数传入有效的日期字符串（非 UTC）', () => {
    const result = index("2023-01-01 12:00:00.123");
    expect(result).toBe("一个表示 2023-01-01 12:00:00.123 的 Dayjs 对象");
  });

  test('TC006: 测试 dayjs 函数传入无效的日期字符串', () => {
    const result = index("invalid-date");
    expect(result).toBe("一个表示无效日期的 Dayjs 对象");
  });

  test('TC007: 测试 dayjs 函数传入数字时间戳', () => {
    const result = index(1672531200000);
    expect(result).toBe("一个表示 2023-01-01 的 Dayjs 对象");
  });

  test('TC008: 测试 parseLocale 函数传入空 preset', () => {
    const result = index(null);
    expect(result).toBe("当前全局 locale 'en'");
  });

  test('TC009: 测试 parseLocale 函数传入已存在的 locale 字符串', () => {
    const result = index("en");
    expect(result).toBe("'en'");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC011: 测试 parseLocale 函数传入带连字符的 locale 字符串且无对应对象', () => {
    const result = index("zh-CN");
    expect(result).toBe("'zh'");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC013: 测试 isValid 方法在有效日期时返回 true', () => {
    const result = index("2023-01-01");
    expect(result).toBe(true);
  });

  test('TC014: 测试 isValid 方法在无效日期时返回 false', () => {
    const result = index("invalid");
    expect(result).toBe(false);
  });

  test('TC015: 测试 isSame 方法在相同日期时返回 true', () => {
    const result = index("2023-01-01", "2023-01-01");
    expect(result).toBe(true);
  });

  test('TC016: 测试 isAfter 方法在当前日期晚于比较日期时返回 true', () => {
    const result = index("2023-01-02", "2023-01-01");
    expect(result).toBe(true);
  });

  test('TC017: 测试 isBefore 方法在当前日期早于比较日期时返回 true', () => {
    const result = index("2023-01-01", "2023-01-02");
    expect(result).toBe(true);
  });

  test('TC019: 测试 $g 方法在 input 有值时调用 set 方法', () => {
    const result = index("2023-01-01", 2024, "$y", "year");
    expect(result).toBe("一个年份为 2024 的 Dayjs 对象");
  });

  test('TC020: 测试 startOf 方法对年单位的处理（开始）', () => {
    const result = index("2023-06-15", "year");
    expect(result).toBe("一个表示 2023-01-01 00:00:00 的 Dayjs 对象");
  });

  test('TC021: 测试 startOf 方法对年单位的处理（结束）', () => {
    const result = index("2023-06-15", "year", false);
    expect(result).toBe("一个表示 2023-12-31 23:59:59.999 的 Dayjs 对象");
  });

  test('TC022: 测试 startOf 方法对周单位的处理', () => {
    const result = index("2023-06-15", "week");
    expect(result).toBe("一个表示当周第一天的 Dayjs 对象");
  });

  test('TC023: 测试 startOf 方法对小时单位的处理', () => {
    const result = index("2023-06-15 12:30:45", "hour");
    expect(result).toBe("一个表示 2023-06-15 12:00:00 的 Dayjs 对象");
  });

  test('TC024: 测试 startOf 方法对无效单位的处理', () => {
    const result = index("2023-06-15", "invalid");
    expect(result).toBe("一个克隆的 Dayjs 对象");
  });

  test('TC025: 测试 $set 方法对月份单位的设置', () => {
    const result = index("2023-01-15", "month", 5);
    expect(result).toBe("一个月份为 6 月的 Dayjs 对象");
  });

  test('TC026: 测试 $set 方法对日期单位的设置', () => {
    const result = index("2023-01-15", "date", 20);
    expect(result).toBe("一个日期为 20 日的 Dayjs 对象");
  });

  test('TC027: 测试 add 方法添加月份', () => {
    const result = index("2023-01-15", 2, "month");
    expect(result).toBe("一个月份为 3 月的 Dayjs 对象");
  });

  test('TC028: 测试 add 方法添加天数', () => {
    const result = index("2023-01-15", 10, "day");
    expect(result).toBe("一个日期为 2023-01-25 的 Dayjs 对象");
  });

  test('TC029: 测试 add 方法添加小时', () => {
    const result = index("2023-01-15 12:00:00", 3, "hour");
    expect(result).toBe("一个时间为 15:00:00 的 Dayjs 对象");
  });

  test('TC030: 测试 format 方法使用默认格式', () => {
    const result = index("2023-01-01 12:30:45", null);
    expect(result).toBe("2023-01-01T12:30:45+00:00");
  });

  test('TC031: 测试 format 方法使用自定义格式 YYYY-MM-DD', () => {
    const result = index("2023-01-01", "YYYY-MM-DD");
    expect(result).toBe("2023-01-01");
  });

  test('TC032: 测试 format 方法在无效日期时返回无效字符串', () => {
    expect(() => { index("invalid", "YYYY-MM-DD"); }).toThrow();
  });

  test('TC033: 测试 diff 方法计算月份差', () => {
    const result = index("2023-06-01", "2023-01-01", "month");
    expect(result).toBe(5);
  });

  test('TC034: 测试 diff 方法计算天数差（浮点数）', () => {
    const result = index("2023-01-02 12:00:00", "2023-01-01", "day", true);
    expect(result).toBe(1.5);
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC036: 测试 dayjs.unix 方法', () => {
    const result = index(1672531200);
    expect(result).toBe("一个表示 2023-01-01 的 Dayjs 对象");
  });

  test('TC038: 测试 parseDate 函数传入 UTC 日期字符串', () => {
    const result = index("2023-01-01T12:00:00Z", true);
    expect(result).toBe("一个 UTC 时间的 Date 对象");
  });

  test('TC_SUP_002: 测试 parseDate 函数中 utc=true 且日期字符串包含可选字段的情况', () => {
    const result = index("2023-05-15T10:30:45.123", true);
    expect(result).toBe("UTC 日期对象");
  });

  test('TC_SUP_003: 测试 $utils 方法', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_004: 测试 unix 方法', () => {
    const result = index("2023-01-01T00:00:00.000Z");
    expect(result).toBe(1672531200);
  });

  test('TC_SUP_005: 测试 startOf 方法中 units 为 \'minute\' 的情况', () => {
    const result = index("2023-05-15T10:30:45.123", "minute");
    expect(result).toBe("2023-05-15T10:30:00.000");
  });

  test('TC_SUP_006: 测试 startOf 方法中 units 为 \'second\' 的情况', () => {
    const result = index("2023-05-15T10:30:45.123", "second");
    expect(result).toBe("2023-05-15T10:30:45.000");
  });

  test('TC_SUP_007: 测试 get 方法', () => {
    const result = index("2023-05-15T10:30:45.123", "month");
    expect(result).toBe(4);
  });

  test('TC_SUP_008: 测试 add 方法中 units 为 \'year\' 的情况', () => {
    const result = index("2023-05-15", 1, "year");
    expect(result).toBe("2024-05-15");
  });

  test('TC_SUP_009: 测试 add 方法中 units 为 \'week\' 的情况', () => {
    const result = index("2023-05-15", 1, "week");
    expect(result).toBe("2023-05-22");
  });

  test('TC_SUP_010: 测试 subtract 方法', () => {
    const result = index("2023-05-15", 1, "day");
    expect(result).toBe("2023-05-14");
  });

  test('TC_SUP_011: 测试 format 方法中 formatStr 包含 \'YY\' 的情况', () => {
    const result = index("2023-05-15", "YY");
    expect(result).toBe("23");
  });

  test('TC_SUP_012: 测试 format 方法中 formatStr 包含 \'M\' 的情况', () => {
    const result = index("2023-05-15", "M");
    expect(result).toBe("5");
  });

  test('TC_SUP_013: 测试 format 方法中 formatStr 包含 \'MMM\' 的情况', () => {
    const result = index("2023-05-15", "MMM");
    expect(result).toBe("May");
  });

  test('TC_SUP_014: 测试 format 方法中 formatStr 包含 \'MMMM\' 的情况', () => {
    const result = index("2023-05-15", "MMMM");
    expect(result).toBe("May");
  });

  test('TC_SUP_015: 测试 format 方法中 formatStr 包含 \'D\' 的情况', () => {
    const result = index("2023-05-15", "D");
    expect(result).toBe("15");
  });

  test('TC_SUP_016: 测试 format 方法中 formatStr 包含 \'d\' 的情况', () => {
    const result = index("2023-05-15", "d");
    expect(result).toBe("1");
  });

  test('TC_SUP_017: 测试 format 方法中 formatStr 包含 \'dd\' 的情况', () => {
    const result = index("2023-05-15", "dd");
    expect(result).toBe("Mo");
  });

  test('TC_SUP_018: 测试 format 方法中 formatStr 包含 \'ddd\' 的情况', () => {
    const result = index("2023-05-15", "ddd");
    expect(result).toBe("Mon");
  });

  test('TC_SUP_019: 测试 format 方法中 formatStr 包含 \'dddd\' 的情况', () => {
    const result = index("2023-05-15", "dddd");
    expect(result).toBe("Monday");
  });

  test('TC_SUP_020: 测试 format 方法中 formatStr 包含 \'H\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "H");
    expect(result).toBe("14");
  });

  test('TC_SUP_021: 测试 format 方法中 formatStr 包含 \'h\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "h");
    expect(result).toBe("2");
  });

  test('TC_SUP_022: 测试 format 方法中 formatStr 包含 \'hh\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "hh");
    expect(result).toBe("02");
  });

  test('TC_SUP_023: 测试 format 方法中 formatStr 包含 \'a\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "a");
    expect(result).toBe("pm");
  });

  test('TC_SUP_024: 测试 format 方法中 formatStr 包含 \'A\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "A");
    expect(result).toBe("PM");
  });

  test('TC_SUP_025: 测试 format 方法中 formatStr 包含 \'m\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "m");
    expect(result).toBe("30");
  });

  test('TC_SUP_026: 测试 format 方法中 formatStr 包含 \'s\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "s");
    expect(result).toBe("45");
  });

  test('TC_SUP_027: 测试 format 方法中 formatStr 包含 \'SSS\' 的情况', () => {
    const result = index("2023-05-15T14:30:45.123", "SSS");
    expect(result).toBe("123");
  });

  test('TC_SUP_028: 测试 format 方法中 formatStr 包含不匹配的字符的情况', () => {
    const result = index("2023-05-15", "X");
    expect(result).toBe("X");
  });

  test('TC_SUP_029: 测试 diff 方法中 units 为 \'year\' 的情况', () => {
    const result = index("2023-05-15", "2021-05-15", "year");
    expect(result).toBe(2);
  });

  test('TC_SUP_030: 测试 diff 方法中 units 为 \'quarter\' 的情况', () => {
    const result = index("2023-08-15", "2023-02-15", "quarter");
    expect(result).toBe(2);
  });

  test('TC_SUP_031: 测试 diff 方法中 units 为 \'week\' 的情况', () => {
    const result = index("2023-05-22", "2023-05-15", "week");
    expect(result).toBe(1);
  });

  test('TC_SUP_032: 测试 diff 方法中 units 为 \'hour\' 的情况', () => {
    const result = index("2023-05-15T14:00:00", "2023-05-15T10:00:00", "hour");
    expect(result).toBe(4);
  });

  test('TC_SUP_033: 测试 diff 方法中 units 为 \'minute\' 的情况', () => {
    const result = index("2023-05-15T14:30:00", "2023-05-15T14:00:00", "minute");
    expect(result).toBe(30);
  });

  test('TC_SUP_034: 测试 diff 方法中 units 为 \'second\' 的情况', () => {
    const result = index("2023-05-15T14:30:45", "2023-05-15T14:30:00", "second");
    expect(result).toBe(45);
  });

  test('TC_SUP_036: 测试 locale 方法中 preset 为 null 的情况', () => {
    const result = index("2023-05-15", null);
    expect(result).toBe("en");
  });

  test('TC_SUP_037: 测试 toJSON 方法中无效日期的情况', () => {
    const result = index("invalid date");
    expect(result).toBe(null);
  });

  test('TC_SUP_038: 测试 toString 方法', () => {
    const result = index("2023-05-15T14:30:45.123Z");
    expect(result).toBe("Mon, 15 May 2023 14:30:45 GMT");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串 preset 且 Ls 中已存在对应语言', () => {
    const result = index("en");
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale 函数，传入带连字符的字符串 preset 且无对应语言，触发递归', () => {
    const result = index("zh-CN");
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

  test('TC_SUP_006: 测试 parseLocale 函数，传入空字符串 preset 且 isLocal 为 true', () => {
    const result = index("", true);
    expect(result).toBe("en");
  });

  test('TC_SUP_010: 测试 parseDate 函数，传入字符串且 utc 为 true', () => {
    const result = index("2023-01-01T00:00:00", true);
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_011: 测试 $utils 方法', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_013: 测试 isAfter 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(false);
  });

  test('TC_SUP_014: 测试 isBefore 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(false);
  });

  test('TC_SUP_015: 测试 $g 方法，传入 input 参数', () => {
    const result = index(15, "$D", "date");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_016: 测试 unix 方法', () => {
    const result = index();
    expect(result).toBe(1672531200);
  });

  test('TC_SUP_017: 测试 valueOf 方法', () => {
    const result = index();
    expect(result).toBe(1672531200000);
  });

  test('TC_SUP_018: 测试 startOf 方法，units 为 \'year\'，startOf 为 false', () => {
    const result = index("year", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_019: 测试 startOf 方法，units 为 \'month\'', () => {
    const result = index("month");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_020: 测试 startOf 方法，units 为 \'week\'，且 $W < weekStart', () => {
    const result = index("week");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_021: 测试 startOf 方法，units 为 \'day\'', () => {
    const result = index("day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_022: 测试 startOf 方法，units 为 \'hour\'', () => {
    const result = index("hour");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_023: 测试 startOf 方法，units 为 \'minute\'', () => {
    const result = index("minute");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_024: 测试 startOf 方法，units 为 \'second\'', () => {
    const result = index("second");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_025: 测试 startOf 方法，units 为无效值', () => {
    const result = index("invalid");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_026: 测试 endOf 方法', () => {
    const result = index("month");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_027: 测试 $set 方法，units 为 \'day\'', () => {
    const result = index("day", 15);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_028: 测试 $set 方法，units 为 \'month\'', () => {
    const result = index("month", 5);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_029: 测试 $set 方法，units 为 \'year\'', () => {
    const result = index("year", 2024);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_030: 测试 $set 方法，units 为 \'hour\'', () => {
    const result = index("hour", 10);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_031: 测试 set 方法', () => {
    const result = index("date", 15);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_032: 测试 get 方法', () => {
    const result = index("year");
    expect(result).toBe(2023);
  });

  test('TC_SUP_033: 测试 add 方法，units 为 \'month\'', () => {
    const result = index(2, "month");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_034: 测试 add 方法，units 为 \'year\'', () => {
    const result = index(1, "year");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_035: 测试 add 方法，units 为 \'day\'', () => {
    const result = index(5, "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_036: 测试 add 方法，units 为 \'week\'', () => {
    const result = index(2, "week");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_037: 测试 add 方法，units 为 \'minute\'', () => {
    const result = index(30, "minute");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_038: 测试 subtract 方法', () => {
    const result = index(5, "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_039: 测试 format 方法，无效日期', () => {
    expect(() => { index("YYYY-MM-DD"); }).toThrow();
  });

  test('TC_SUP_040: 测试 format 方法，无 formatStr 参数', () => {
    const result = index();
    expect(result).toBe("2023-01-01T00:00:00+08:00");
  });

  test('TC_SUP_041: 测试 format 方法，包含多种格式符', () => {
    const result = index("YYYY-MM-DD HH:mm:ss ddd");
    expect(result).toBe("2023-01-01 00:00:00 Sun");
  });

  test('TC_SUP_042: 测试 format 方法，匹配 \'YY\'', () => {
    const result = index("YY");
    expect(result).toBe("23");
  });
});
