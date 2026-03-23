/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试 dayjs() 工厂函数传入 Dayjs 实例时返回克隆', () => {
    const result = index("dayjs实例", null);
    expect(result).toBe("新的 Dayjs 实例（克隆）");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC003: 测试 dayjs() 工厂函数传入非 Dayjs 实例且 c 非对象', () => {
    const result = index("2023-01-01", null);
    expect(result).toBe("新的 Dayjs 实例");
  });

  test('TC004: 测试 parseLocale 传入空 preset', () => {
    const result = index(null, null, false);
    expect(result).toBe("L（当前全局语言）");
  });

  test('TC005: 测试 parseLocale 传入字符串 preset 且已加载', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC007: 测试 parseLocale 传入字符串 preset 且未加载且无 object 但有连字符', () => {
    const result = index("zh-cn", null, false);
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC009: 测试 parseLocale 传入字符串 preset 且 isLocal 为 true', () => {
    const result = index("en", null, true);
    expect(result).toBe("en");
  });

  test('TC010: 测试 parseLocale 传入字符串 preset 且未找到语言且无连字符', () => {
    const result = index("xx", null, false);
    expect(result).toBe("L（当前全局语言）");
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
    expect(result).toBe("true");
  });

  test('TC020: 测试 Dayjs.isValid() 无效日期', () => {
    const result = index(null).isValid();
    expect(result).toBe("false");
  });

  test('TC021: 测试 Dayjs.isSame() 相同日期相同单位', () => {
    const result = index("2023-01-01", "day").isSame();
    expect(result).toBe("true");
  });

  test('TC022: 测试 Dayjs.isSame() 不同日期相同单位', () => {
    const result = index("2023-01-02", "day").isSame();
    expect(result).toBe("false");
  });

  test('TC023: 测试 Dayjs.isAfter() 日期在之后', () => {
    const result = index("2023-01-01", "day").isAfter();
    expect(result).toBe("true");
  });

  test('TC024: 测试 Dayjs.isAfter() 日期不在之后', () => {
    const result = index("2023-01-03", "day").isAfter();
    expect(result).toBe("false");
  });

  test('TC025: 测试 Dayjs.isBefore() 日期在之前', () => {
    const result = index("2023-01-03", "day").isBefore();
    expect(result).toBe("true");
  });

  test('TC026: 测试 Dayjs.isBefore() 日期不在之前', () => {
    const result = index("2023-01-01", "day").isBefore();
    expect(result).toBe("false");
  });

  test('TC028: 测试 Dayjs.$g() 有 input（setter）', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("设置后的新实例");
  });

  test('TC029: 测试 Dayjs.unix()', () => {
    const result = index("2023-01-01T00:00:00Z").unix();
    expect(result).toBe("1672531200");
  });

  test('TC030: 测试 Dayjs.valueOf()', () => {
    const result = index("2023-01-01T00:00:00Z").valueOf();
    expect(result).toBe("1672531200000");
  });

  test('TC031: 测试 Dayjs.startOf(\'year\', true)', () => {
    const result = index("year", true);
    expect(result).toBe("当年第一天的 Dayjs 实例");
  });

  test('TC032: 测试 Dayjs.startOf(\'year\', false)', () => {
    const result = index("year", false);
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

  test('TC_SUP_003: 测试parseLocale函数：传入字符串preset且object为空，但preset包含连字符，触发递归调用', () => {
    const result = index("zh-CN", null);
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_006: 测试parseDate函数：utc为true且日期字符串匹配正则，覆盖UTC日期构造', () => {
    const result = index("2023-12-31T23:59:59.999", true);
    expect(result).toBe("Date对象");
  });

  test('TC_SUP_007: 测试$utils方法：调用返回Utils对象', () => {
    const result = index();
    expect(result).toBe("Utils对象");
  });

  test('TC_SUP_009: 测试$g方法：input有值，调用set方法', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("设置后的Dayjs实例");
  });

  test('TC_SUP_012: 测试startOf方法：units为\'year\'且startOf为false，触发instanceFactory(31, 11)', () => {
    const result = index("year", false);
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_013: 测试startOf方法：units为\'month\'且startOf为false，触发instanceFactory(0, $M + 1)', () => {
    const result = index("month", false);
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_015: 测试startOf方法：units为\'day\'，触发instanceFactorySet调用', () => {
    const result = index("day");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_016: 测试startOf方法：units为\'hour\'，触发instanceFactorySet调用', () => {
    const result = index("hour");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_017: 测试startOf方法：units为\'minute\'，触发instanceFactorySet调用', () => {
    const result = index("minute");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_018: 测试startOf方法：units为\'second\'，触发instanceFactorySet调用', () => {
    const result = index("second");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_020: 测试$set方法：unit为\'day\'，计算arg = this.$D + (int - this.$W)', () => {
    const result = index("day", 1);
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_023: 测试$set方法：unit为\'hour\'，触发this.$d[name](arg)和init()', () => {
    const result = index("hour", 15);
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_024: 测试set方法：调用$set并返回克隆实例', () => {
    const result = index("month", 5);
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_025: 测试get方法：调用Utils.p(unit)并返回对应值', () => {
    const result = index("month");
    expect(result).toBe("月份值");
  });

  test('TC_SUP_027: 测试add方法：unit为\'month\'，触发set(C.M, this.$M + number)', () => {
    const result = index(2, "month");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_028: 测试add方法：unit为\'year\'，触发set(C.Y, this.$y + number)', () => {
    const result = index(1, "year");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_029: 测试add方法：unit为\'day\'，触发instanceFactorySet(1)', () => {
    const result = index(7, "day");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_030: 测试add方法：unit为\'week\'，触发instanceFactorySet(7)', () => {
    const result = index(2, "week");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_031: 测试add方法：unit为\'minute\'，覆盖step对象和nextTimeStamp计算', () => {
    const result = index(30, "minute");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_032: 测试subtract方法：调用add(number * -1, string)', () => {
    const result = index(5, "day");
    expect(result).toBe("Dayjs实例");
  });

  test('TC_SUP_034: 测试format方法：formatStr为空，使用默认格式', () => {
    const result = index(null);
    expect(result).toBe("格式化字符串");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale 函数：传入字符串 preset（带连字符）且 Ls 中不存在，覆盖 return parseLocale(presetSplit[0])', () => {
    const result = index("en-US", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_004: 测试 parseLocale 函数：传入字符串 preset 且 isLocal 为 true，覆盖 if (!isLocal && l) L = l 分支（不执行）', () => {
    const result = index("de", null, true);
    expect(result).toBe("de");
  });

  test('TC_SUP_006: 测试 parseDate 函数：utc 为 true，覆盖 Date.UTC 分支', () => {
    const result = index("2023-01-01T12:00:00", true);
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_007: 测试 $utils 方法：覆盖 return Utils', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_009: 测试 $g 方法：input 有值，覆盖 return this.set(set, input)', () => {
    const result = index(2024, "$y", "year");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_010: 测试 startOf 方法：isStartOf 为 false（即 endOf），覆盖 instanceFactory 中的三元表达式分支', () => {
    const result = index("year", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_011: 测试 startOf 方法：覆盖 instanceFactorySet 中的 argumentStart 和 argumentEnd 初始化', () => {
    const result = index("hour");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_012: 测试 startOf 方法：units 为 \'year\' 且 isStartOf 为 false，覆盖 return isStartOf ? instanceFactory(1, 0) : instanceFactory(31, 11)', () => {
    const result = index("year", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_013: 测试 startOf 方法：units 为 \'month\' 且 isStartOf 为 false，覆盖 return isStartOf ? instanceFactory(1, $M) : instanceFactory(0, $M + 1)', () => {
    const result = index("month", false);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_014: 测试 startOf 方法：units 为 \'week\'，覆盖 weekStart 逻辑和 gap 计算', () => {
    const result = index("week");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_015: 测试 startOf 方法：units 为 \'date\'，覆盖 instanceFactorySet 调用', () => {
    const result = index("date");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_016: 测试 startOf 方法：units 为 \'minute\'，覆盖 instanceFactorySet 调用', () => {
    const result = index("minute");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_017: 测试 startOf 方法：units 为 \'second\'，覆盖 instanceFactorySet 调用', () => {
    const result = index("second");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_018: 测试 $set 方法：覆盖 unit = Utils.p(units), utcPad, name 对象，arg 计算（unit === C.D）', () => {
    const result = index("day", 5);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_019: 测试 $set 方法：unit 为 \'month\'，覆盖 if (unit === C.M || unit === C.Y) 分支', () => {
    const result = index("month", 5);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_020: 测试 $set 方法：unit 为 \'year\'，覆盖 if (unit === C.M || unit === C.Y) 分支', () => {
    const result = index("year", 2025);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_021: 测试 $set 方法：unit 为 \'hour\'，覆盖 else if (name) this.$d[name](arg) 分支', () => {
    const result = index("hour", 10);
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_022: 测试 set 方法：覆盖 return this.clone().$set(string, int)', () => {
    const result = index("month", 6).clone();
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_023: 测试 get 方法：覆盖 return this[Utils.p(unit)]()', () => {
    const result = index("year");
    expect(result).toBe("年份值");
  });

  test('TC_SUP_024: 测试 add 方法：覆盖 number = Number(number), unit = Utils.p(units), instanceFactorySet 函数', () => {
    const result = index("2", "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_025: 测试 add 方法：unit 为 \'minute\'，覆盖 step 逻辑和 nextTimeStamp 计算', () => {
    const result = index(30, "minute");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_026: 测试 subtract 方法：覆盖 return this.add(number * -1, string)', () => {
    const result = index(1, "day");
    expect(result).toBe("Dayjs 实例");
  });

  test('TC_SUP_027: 测试 format 方法：覆盖 locale = this.$locale(), 无效日期分支', () => {
    const result = index("YYYY-MM-DD");
    expect(result).toBe("无效日期字符串");
  });

  test('TC_SUP_028: 测试 format 方法：formatStr 为空，覆盖 str = formatStr || C.FORMAT_DEFAULT', () => {
    const result = index(null);
    expect(result).toBe("格式化日期字符串");
  });

  test('TC_SUP_029: 测试 format 方法：覆盖 zoneStr = Utils.z(this), $H, $m, $M 解构，weekdays, months, meridiem 解构', () => {
    const result = index("YYYY-MM-DD HH:mm:ss");
    expect(result).toBe("格式化日期字符串");
  });

  test('TC_SUP_030: 测试 format 方法：覆盖 getShort 函数和 get$H 函数', () => {
    const result = index("MMM MMMM d dd ddd dddd");
    expect(result).toBe("格式化日期字符串");
  });

  test('TC_SUP_031: 测试 format 方法：覆盖 meridiemFunc 函数和 matches 函数中的多个 switch case', () => {
    const result = index("YY YYYY M MM D DD H HH h hh a A m mm s ss SSS Z");
    expect(result).toBe("格式化日期字符串");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });
});
