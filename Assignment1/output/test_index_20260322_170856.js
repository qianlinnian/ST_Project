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
    const result = index("2023-01-01 12:00:00");
    expect(result).toBe("一个表示 2023-01-01 12:00:00 的 Dayjs 对象");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC007: 测试 dayjs 函数传入无效的日期字符串', () => {
    const result = index("invalid date");
    expect(result).toBe("一个表示无效日期的 Dayjs 对象");
  });

  test('TC008: 测试 dayjs 函数传入数字时间戳', () => {
    const result = index(1672531200000);
    expect(result).toBe("一个表示 2023-01-01 的 Dayjs 对象");
  });

  test('TC009: 测试 isValid 方法在有效日期时返回 true', () => {
    const result = index("2023-01-01");
    expect(result).toBe(true);
  });

  test('TC010: 测试 isValid 方法在无效日期时返回 false', () => {
    const result = index(null);
    expect(result).toBe(false);
  });

  test('TC011: 测试 isSame 方法（相同日期，无单位）', () => {
    const result = index("2023-01-01", "2023-01-01");
    expect(result).toBe(true);
  });

  test('TC012: 测试 isSame 方法（不同日期，无单位）', () => {
    const result = index("2023-01-01", "2023-01-02");
    expect(result).toBe(false);
  });

  test('TC013: 测试 isAfter 方法（日期在前）', () => {
    const result = index("2023-01-02", "2023-01-01");
    expect(result).toBe(true);
  });

  test('TC014: 测试 isAfter 方法（日期在后）', () => {
    const result = index("2023-01-01", "2023-01-02");
    expect(result).toBe(false);
  });

  test('TC015: 测试 isBefore 方法（日期在后）', () => {
    const result = index("2023-01-01", "2023-01-02");
    expect(result).toBe(true);
  });

  test('TC016: 测试 isBefore 方法（日期在前）', () => {
    const result = index("2023-01-02", "2023-01-01");
    expect(result).toBe(false);
  });

  test('TC017: 测试 $g 方法（无输入参数）', () => {
    const result = index("2023-01-01", "$y");
    expect(result).toBe(2023);
  });

  test('TC018: 测试 $g 方法（有输入参数）', () => {
    const result = index("2023-01-01", 2024, "year");
    expect(result).toBe("一个表示 2024-01-01 的 Dayjs 对象");
  });

  test('TC019: 测试 startOf 方法（单位：年，isStartOf 为 true）', () => {
    const result = index("2023-06-15", "year");
    expect(result).toBe("一个表示 2023-01-01 的 Dayjs 对象");
  });

  test('TC020: 测试 startOf 方法（单位：年，isStartOf 为 false）', () => {
    const result = index("2023-06-15", "year", false);
    expect(result).toBe("一个表示 2023-12-31 的 Dayjs 对象");
  });

  test('TC021: 测试 startOf 方法（单位：月）', () => {
    const result = index("2023-06-15", "month");
    expect(result).toBe("一个表示 2023-06-01 的 Dayjs 对象");
  });

  test('TC022: 测试 startOf 方法（单位：周，$W >= weekStart）', () => {
    const result = index("2023-06-15", "week");
    expect(result).toBe("一个表示 2023-06-11 的 Dayjs 对象（假设 weekStart 为 0）");
  });

  test('TC023: 测试 startOf 方法（单位：周，$W < weekStart）', () => {
    const result = index("2023-06-11", "week");
    expect(result).toBe("一个表示 2023-06-11 的 Dayjs 对象（假设 weekStart 为 1）");
  });

  test('TC024: 测试 startOf 方法（单位：日）', () => {
    const result = index("2023-06-15 12:30:45", "day");
    expect(result).toBe("一个表示 2023-06-15 00:00:00 的 Dayjs 对象");
  });

  test('TC025: 测试 startOf 方法（单位：小时）', () => {
    const result = index("2023-06-15 12:30:45", "hour");
    expect(result).toBe("一个表示 2023-06-15 12:00:00 的 Dayjs 对象");
  });

  test('TC026: 测试 startOf 方法（单位：分钟）', () => {
    const result = index("2023-06-15 12:30:45", "minute");
    expect(result).toBe("一个表示 2023-06-15 12:30:00 的 Dayjs 对象");
  });

  test('TC027: 测试 startOf 方法（单位：秒）', () => {
    const result = index("2023-06-15 12:30:45.123", "second");
    expect(result).toBe("一个表示 2023-06-15 12:30:45.000 的 Dayjs 对象");
  });

  test('TC028: 测试 startOf 方法（无效单位）', () => {
    const result = index("2023-06-15", "invalid");
    expect(result).toBe("一个克隆的 Dayjs 对象");
  });

  test('TC029: 测试 endOf 方法', () => {
    const result = index("2023-06-15", "month");
    expect(result).toBe("一个表示 2023-06-30 的 Dayjs 对象");
  });

  test('TC030: 测试 $set 方法（单位：日）', () => {
    const result = index("2023-06-15", "date", 20);
    expect(result).toBe("一个表示 2023-06-20 的 Dayjs 对象");
  });

  test('TC031: 测试 $set 方法（单位：月）', () => {
    const result = index("2023-01-31", "month", 1);
    expect(result).toBe("一个表示 2023-02-28 的 Dayjs 对象");
  });

  test('TC032: 测试 $set 方法（单位：年）', () => {
    const result = index("2020-02-29", "year", 2021);
    expect(result).toBe("一个表示 2021-02-28 的 Dayjs 对象");
  });

  test('TC033: 测试 $set 方法（单位：小时）', () => {
    const result = index("2023-06-15 12:00:00", "hour", 15);
    expect(result).toBe("一个表示 2023-06-15 15:00:00 的 Dayjs 对象");
  });

  test('TC034: 测试 $set 方法（无效单位）', () => {
    const result = index("2023-06-15", "invalid", 1);
    expect(result).toBe("原始的 Dayjs 对象");
  });

  test('TC035: 测试 set 方法', () => {
    const result = index("2023-06-15", "date", 20);
    expect(result).toBe("一个新的表示 2023-06-20 的 Dayjs 对象");
  });

  test('TC036: 测试 get 方法', () => {
    const result = index("2023-06-15", "year");
    expect(result).toBe(2023);
  });

  test('TC_SUP_001: 测试 parseLocale 函数，传入字符串 preset 且 Ls 中已存在对应 locale', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale 函数，传入字符串 preset 且 Ls 中不存在，但包含连字符', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_005: 测试 parseLocale 函数，传入字符串 preset 且 isLocal 为 true', () => {
    const result = index("fr", null, true);
    expect(result).toBe("fr");
  });

  test('TC_SUP_008: 测试 parseDate 函数，传入字符串且 utc 为 true', () => {
    const result = index("2023-01-01T00:00:00", true);
    expect(result).toBe("UTC 时间的 Date 实例");
  });

  test('TC_SUP_009: 测试 $utils 方法', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_010: 测试 isSame 方法，传入日期字符串', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe("true 或 false");
  });

  test('TC_SUP_012: 测试 $g 方法，input 有值', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_013: 测试 unix 方法', () => {
    const result = index();
    expect(result).toBe("Unix 时间戳");
  });

  test('TC_SUP_014: 测试 valueOf 方法', () => {
    const result = index();
    expect(result).toBe("时间戳毫秒数");
  });

  test('TC_SUP_015: 测试 startOf 方法，units 为 \'year\'', () => {
    const result = index("year", true);
    expect(result).toBe("年初的 Dayjs 实例");
  });

  test('TC_SUP_016: 测试 startOf 方法，units 为 \'month\'', () => {
    const result = index("month", false);
    expect(result).toBe("月末的 Dayjs 实例");
  });

  test('TC_SUP_017: 测试 startOf 方法，units 为 \'week\'', () => {
    const result = index("week", true);
    expect(result).toBe("周初的 Dayjs 实例");
  });

  test('TC_SUP_018: 测试 startOf 方法，units 为 \'day\'', () => {
    const result = index("day", true);
    expect(result).toBe("日初的 Dayjs 实例");
  });

  test('TC_SUP_019: 测试 startOf 方法，units 为 \'hour\'', () => {
    const result = index("hour", true);
    expect(result).toBe("时初的 Dayjs 实例");
  });

  test('TC_SUP_020: 测试 startOf 方法，units 为 \'minute\'', () => {
    const result = index("minute", true);
    expect(result).toBe("分初的 Dayjs 实例");
  });

  test('TC_SUP_021: 测试 startOf 方法，units 为 \'second\'', () => {
    const result = index("second", true);
    expect(result).toBe("秒初的 Dayjs 实例");
  });

  test('TC_SUP_022: 测试 startOf 方法，units 为无效值', () => {
    const result = index("invalid", true);
    expect(result).toBe("克隆的 Dayjs 实例");
  });

  test('TC_SUP_023: 测试 endOf 方法', () => {
    const result = index("month");
    expect(result).toBe("月末的 Dayjs 实例");
  });

  test('TC_SUP_024: 测试 $set 方法，units 为 \'day\'', () => {
    const result = index("day", 15);
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_025: 测试 $set 方法，units 为 \'month\'', () => {
    const result = index("month", 5);
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_026: 测试 set 方法', () => {
    const result = index("year", 2024);
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_027: 测试 get 方法', () => {
    const result = index("month");
    expect(result).toBe("月份值");
  });

  test('TC_SUP_028: 测试 add 方法，units 为 \'month\'', () => {
    const result = index(2, "month");
    expect(result).toBe("增加月份后的 Dayjs 实例");
  });

  test('TC_SUP_029: 测试 add 方法，units 为 \'year\'', () => {
    const result = index(1, "year");
    expect(result).toBe("增加年份后的 Dayjs 实例");
  });

  test('TC_SUP_030: 测试 add 方法，units 为 \'day\'', () => {
    const result = index(3, "day");
    expect(result).toBe("增加天数后的 Dayjs 实例");
  });

  test('TC_SUP_031: 测试 add 方法，units 为 \'week\'', () => {
    const result = index(2, "week");
    expect(result).toBe("增加周数后的 Dayjs 实例");
  });

  test('TC_SUP_032: 测试 add 方法，units 为 \'minute\'', () => {
    const result = index(30, "minute");
    expect(result).toBe("增加分钟后的 Dayjs 实例");
  });

  test('TC_SUP_033: 测试 subtract 方法', () => {
    const result = index(5, "day");
    expect(result).toBe("减少天数后的 Dayjs 实例");
  });

  test('TC_SUP_034: 测试 format 方法，无效日期', () => {
    const result = index("YYYY-MM-DD");
    expect(result).toBe("无效日期字符串");
  });

  test('TC_SUP_036: 测试 format 方法，匹配 \'YY\'', () => {
    const result = index("YY");
    expect(result).toBe("两位年份");
  });

  test('TC_SUP_037: 测试 format 方法，匹配 \'YYYY\'', () => {
    const result = index("YYYY");
    expect(result).toBe("四位年份");
  });

  test('TC_SUP_001: 测试 parseLocale 函数：传入字符串 preset 且 Ls 中已存在对应语言环境', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale 函数：传入字符串 preset 且 Ls 中不存在，但包含连字符，递归调用', () => {
    const result = index("zh-CN", null, false);
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

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_011: 测试 isSame 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(true);
  });

  test('TC_SUP_012: 测试 isAfter 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(false);
  });

  test('TC_SUP_013: 测试 isBefore 方法', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe(false);
  });

  test('TC_SUP_015: 测试 $g 方法：input 有值时调用 set', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("Dayjs instance with year 2024");
  });

  test('TC_SUP_018: 测试 startOf 方法：startOf 参数为 false（即 endOf）', () => {
    const result = index("month", false);
    expect(result).toBe("Dayjs instance at end of month");
  });

  test('TC_SUP_019: 测试 startOf 方法：units 为 \'year\'', () => {
    const result = index("year", true);
    expect(result).toBe("Dayjs instance at start of year");
  });

  test('TC_SUP_020: 测试 startOf 方法：units 为 \'week\'，且 $W < weekStart', () => {
    const result = index("week", true);
    expect(result).toBe("Dayjs instance at start of week");
  });

  test('TC_SUP_021: 测试 startOf 方法：units 为 \'day\'', () => {
    const result = index("day", true);
    expect(result).toBe("Dayjs instance at start of day");
  });

  test('TC_SUP_022: 测试 startOf 方法：units 为 \'hour\'', () => {
    const result = index("hour", true);
    expect(result).toBe("Dayjs instance at start of hour");
  });

  test('TC_SUP_023: 测试 startOf 方法：units 为 \'minute\'', () => {
    const result = index("minute", true);
    expect(result).toBe("Dayjs instance at start of minute");
  });

  test('TC_SUP_024: 测试 startOf 方法：units 为 \'second\'', () => {
    const result = index("second", true);
    expect(result).toBe("Dayjs instance at start of second");
  });

  test('TC_SUP_025: 测试 startOf 方法：units 无效时返回克隆', () => {
    const result = index("invalid", true);
    expect(result).toBe("Dayjs instance clone");
  });

  test('TC_SUP_026: 测试 endOf 方法', () => {
    const result = index("month");
    expect(result).toBe("Dayjs instance at end of month");
  });

  test('TC_SUP_027: 测试 $set 方法：units 为 \'day\'，计算 arg', () => {
    const result = index("day", 15);
    expect(result).toBe("Dayjs instance with day set to 15");
  });

  test('TC_SUP_028: 测试 $set 方法：units 为 \'month\'', () => {
    const result = index("month", 5);
    expect(result).toBe("Dayjs instance with month set to 5");
  });

  test('TC_SUP_029: 测试 $set 方法：units 为 \'year\'', () => {
    const result = index("year", 2024);
    expect(result).toBe("Dayjs instance with year set to 2024");
  });

  test('TC_SUP_030: 测试 $set 方法：units 为 \'hour\'', () => {
    const result = index("hour", 14);
    expect(result).toBe("Dayjs instance with hour set to 14");
  });

  test('TC_SUP_031: 测试 set 方法', () => {
    const result = index("month", 6);
    expect(result).toBe("Dayjs instance with month set to 6");
  });

  test('TC_SUP_032: 测试 get 方法', () => {
    const result = index("year");
    expect(result).toBe(2023);
  });

  test('TC_SUP_033: 测试 add 方法：units 为 \'month\'', () => {
    const result = index(2, "month");
    expect(result).toBe("Dayjs instance with month added by 2");
  });

  test('TC_SUP_034: 测试 add 方法：units 为 \'year\'', () => {
    const result = index(1, "year");
    expect(result).toBe("Dayjs instance with year added by 1");
  });

  test('TC_SUP_035: 测试 add 方法：units 为 \'day\'', () => {
    const result = index(3, "day");
    expect(result).toBe("Dayjs instance with day added by 3");
  });

  test('TC_SUP_036: 测试 add 方法：units 为 \'week\'', () => {
    const result = index(2, "week");
    expect(result).toBe("Dayjs instance with week added by 2");
  });

  test('TC_SUP_037: 测试 add 方法：units 为 \'minute\'', () => {
    const result = index(30, "minute");
    expect(result).toBe("Dayjs instance with minute added by 30");
  });
});
