/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试 dayjs() 工厂函数传入 Dayjs 实例时返回克隆', () => {
    const result = index("dayjs实例", null);
    expect(result).toBe("新的 Dayjs 实例，与原实例值相同但引用不同");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC003: 测试 dayjs() 工厂函数传入非 Dayjs 实例且 c 非对象', () => {
    const result = index("2023-01-01", null);
    expect(result).toBe("新的 Dayjs 实例，配置为空对象");
  });

  test('TC004: 测试 parseLocale 传入空 preset 返回全局语言', () => {
    const result = index(null, null, false);
    expect(result).toBe("L 的值（如 'en'）");
  });

  test('TC005: 测试 parseLocale 传入字符串 preset 且已加载', () => {
    const result = index("en", null, false);
    expect(result).toBe("preset 的小写形式（如 'en'）");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC007: 测试 parseLocale 传入字符串 preset 且未加载且无 object 参数，但包含连字符', () => {
    const result = index("zh-cn", null, false);
    expect(result).toBe("递归调用 parseLocale('zh') 的结果");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC009: 测试 parseLocale 传入字符串 preset 且 isLocal 为 true', () => {
    const result = index("en", null, true);
    expect(result).toBe("preset 的小写形式（如 'en'）");
  });

  test('TC010: 测试 parseLocale 传入字符串 preset 且未加载且无 object 参数且不包含连字符', () => {
    const result = index("unknown", null, false);
    expect(result).toBe("全局语言 L 的值");
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

  test('TC019: 测试 Dayjs.isValid() 有效日期', () => {
    const result = index("2023-01-01").isValid();
    expect(result).toBe(true);
  });

  test('TC020: 测试 Dayjs.isValid() 无效日期', () => {
    const result = index(null).isValid();
    expect(result).toBe(false);
  });

  test('TC021: 测试 Dayjs.isSame() 相同日期相同单位', () => {
    const result = index("2023-01-01", "day").isSame();
    expect(result).toBe(true);
  });

  test('TC022: 测试 Dayjs.isSame() 不同日期相同单位', () => {
    const result = index("2023-01-02", "day").isSame();
    expect(result).toBe(false);
  });

  test('TC023: 测试 Dayjs.isAfter() 日期在之后', () => {
    const result = index("2023-01-01", "day").isAfter();
    expect(result).toBe(true);
  });

  test('TC024: 测试 Dayjs.isAfter() 日期不在之后', () => {
    const result = index("2023-01-03", "day").isAfter();
    expect(result).toBe(false);
  });

  test('TC025: 测试 Dayjs.isBefore() 日期在之前', () => {
    const result = index("2023-01-03", "day").isBefore();
    expect(result).toBe(true);
  });

  test('TC026: 测试 Dayjs.isBefore() 日期不在之前', () => {
    const result = index("2023-01-01", "day").isBefore();
    expect(result).toBe(false);
  });

  test('TC028: 测试 Dayjs.$g() 有 input 参数（setter）', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("设置年份后的新实例");
  });

  test('TC029: 测试 Dayjs.unix()', () => {
    const result = index("2023-01-01T00:00:00Z").unix();
    expect(result).toBe(1672531200);
  });

  test('TC030: 测试 Dayjs.valueOf()', () => {
    const result = index("2023-01-01T00:00:00Z").valueOf();
    expect(result).toBe(1672531200000);
  });

  test('TC032: 测试 Dayjs.startOf() 单位 Y 且 isStartOf 为 false', () => {
    const result = index("year", false).startOf();
    expect(result).toBe("当年最后一天的 Dayjs 实例");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale 函数：传入字符串 preset 且 Ls 中不存在，且 preset 包含连字符', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("zh");
  });

  test('TC_SUP_005: 测试 parseDate 函数：utc 为 true 且 date 为匹配的字符串', () => {
    const result = index("2023-01-01T12:00:00.123", true);
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_006: 测试 $utils 方法', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_008: 测试 $g 方法：input 已定义', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_009: 测试 startOf 方法：C.W 分支，$u 为 true', () => {
    const result = index("week", true, "2023-01-01T12:00:00Z", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_010: 测试 startOf 方法：C.W 分支，$u 为 false', () => {
    const result = index("week", false, "2023-01-01T12:00:00");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_011: 测试 startOf 方法：C.Y 分支，isStartOf 为 false', () => {
    const result = index("year", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_012: 测试 startOf 方法：C.M 分支，isStartOf 为 false', () => {
    const result = index("month", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_013: 测试 startOf 方法：C.D 分支', () => {
    const result = index("day", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_014: 测试 startOf 方法：C.H 分支', () => {
    const result = index("hour", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_015: 测试 startOf 方法：C.MIN 分支', () => {
    const result = index("minute", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_016: 测试 startOf 方法：C.S 分支', () => {
    const result = index("second", true);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_017: 测试 $set 方法：C.D 分支', () => {
    const result = index("day", 15);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_018: 测试 $set 方法：C.M 分支', () => {
    const result = index("month", 5);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_019: 测试 $set 方法：C.Y 分支', () => {
    const result = index("year", 2024);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_020: 测试 set 方法', () => {
    const result = index("month", 6);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_021: 测试 get 方法', () => {
    const result = index("month");
    expect(result).toBe("月份值");
  });

  test('TC_SUP_022: 测试 add 方法：C.M 分支', () => {
    const result = index(2, "month");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_023: 测试 add 方法：C.Y 分支', () => {
    const result = index(1, "year");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_024: 测试 add 方法：C.D 分支', () => {
    const result = index(3, "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_025: 测试 add 方法：C.W 分支', () => {
    const result = index(2, "week");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_026: 测试 add 方法：C.MIN 分支', () => {
    const result = index(30, "minute");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_027: 测试 subtract 方法', () => {
    const result = index(1, "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_028: 测试 format 方法：无效日期', () => {
    expect(() => { index("YYYY-MM-DD", "invalid"); }).toThrow();
  });

  test('TC_SUP_029: 测试 format 方法：formatStr 为空', () => {
    const result = index(null, "2023-01-01");
    expect(result).toBe("默认格式字符串");
  });

  test('TC_SUP_030: 测试 format 方法：完整格式字符串', () => {
    const result = index("YYYY-MM-DD HH:mm:ss", "2023-01-01T12:30:45");
    expect(result).toBe("格式化字符串");
  });

  test('TC_SUP_031: 测试 utcOffset 方法', () => {
    const result = index("2023-01-01T12:00:00Z");
    expect(result).toBe("时区偏移分钟数");
  });

  test('TC_SUP_032: 测试 diff 方法：C.Y 分支', () => {
    const result = index("2024-01-01", "year", true);
    expect(result).toBe("年份差");
  });

  test('TC_SUP_033: 测试 diff 方法：C.M 分支', () => {
    const result = index("2023-03-01", "month", true);
    expect(result).toBe("月份差");
  });

  test('TC000: ', () => {
    const result = index("2023-04-01");
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_002: 测试 parseLocale 函数：传入字符串 preset 且 presetSplit.length > 1，覆盖 return parseLocale(presetSplit[0])', () => {
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
});
