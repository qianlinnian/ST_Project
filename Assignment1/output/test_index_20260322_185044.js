/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试dayjs工厂函数：当输入已经是Dayjs实例时，返回其克隆体', () => {
    const result = index("（一个Dayjs实例）", "未提供");
    expect(result).toBe("一个新的Dayjs实例，其内部日期值与输入实例相同");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC003: 测试dayjs工厂函数：当输入是字符串日期且第二个参数不是对象时，使用空配置', () => {
    const result = index("2023-04-15", null);
    expect(result).toBe("一个新的Dayjs实例，其$L为默认值（如'en'）");
  });

  test('TC004: 测试parseLocale：当preset为undefined时，返回当前全局语言L', () => {
    const result = index(null, null, false);
    expect(result).toBe("当前全局语言标识符（初始为'en'）");
  });

  test('TC005: 测试parseLocale：当preset为已加载的语言字符串时，返回该语言标识', () => {
    const result = index("en", null, false);
    expect(result).toBe("'en'");
  });

  test('TC006: 测试parseLocale：当preset为未加载的语言字符串，但提供了object时，注册并返回该语言标识', () => {
    const result = index("fr", "一个语言包对象", false);
    expect(result).toBe("'fr'");
  });

  test('TC007: 测试parseLocale：当preset为带连字符的语言字符串且未单独注册时，回退到主语言', () => {
    const result = index("zh-cn", null, false);
    expect(result).toBe("'zh' （假设'zh'已注册）或全局语言");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC009: 测试parseLocale：isLocal参数为true时，不更新全局语言L', () => {
    const result = index("fr", "一个语言包对象", true);
    expect(result).toBe("'fr'，但全局L应保持不变（如'en'）");
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

  test('TC018: 测试Dayjs.isValid：对于有效日期，返回true', () => {
    const result = index("dayjs('2023-04-15')");
    expect(result).toBe(true);
  });

  test('TC019: 测试Dayjs.isValid：对于无效日期（如dayjs(null)），返回false', () => {
    const result = index("dayjs(null)");
    expect(result).toBe(false);
  });

  test('TC020: 测试Dayjs.isSame：两个相同日期，不带单位参数', () => {
    const result = index("dayjs('2023-04-15')", "dayjs('2023-04-15')", null);
    expect(result).toBe(true);
  });

  test('TC021: 测试Dayjs.isSame：两个不同日期，带\'day\'单位，但日期部分相同', () => {
    const result = index("dayjs('2023-04-15T10:00:00')", "dayjs('2023-04-15T20:00:00')", "day");
    expect(result).toBe(true);
  });

  test('TC022: 测试Dayjs.isAfter：日期在另一个之后（不带单位）', () => {
    const result = index("dayjs('2023-04-16')", "dayjs('2023-04-15')", null);
    expect(result).toBe(true);
  });

  test('TC023: 测试Dayjs.isBefore：日期在另一个之前（带\'year\'单位）', () => {
    const result = index("dayjs('2023-12-31')", "dayjs('2024-01-01')", "year");
    expect(result).toBe(true);
  });

  test('TC024: 测试Dayjs.$g：无输入参数时作为getter返回内部值', () => {
    const result = index("dayjs('2023-04-15')", null, "$D", "D");
    expect(result).toBe(15);
  });

  test('TC025: 测试Dayjs.$g：有输入参数时作为setter调用set方法', () => {
    const result = index("dayjs('2023-04-15')", 25, "$D", "D");
    expect(result).toBe("一个新的Dayjs实例，日期部分变为25");
  });

  test('TC026: 测试Dayjs.unix和valueOf：验证秒级和毫秒级时间戳', () => {
    const result = index("dayjs('1970-01-01T00:00:01.500Z')");
    expect(result).toBe("{'unix': 1, 'valueOf': 1500}");
  });

  test('TC027: 测试Dayjs.startOf：单位是\'year\'且是开始', () => {
    const result = index("dayjs('2023-06-15')", "year", null);
    expect(result).toBe("一个新的Dayjs实例，表示2023-01-01 00:00:00.000");
  });

  test('TC028: 测试Dayjs.startOf：单位是\'week\'，且语言包配置weekStart为1（周一）', () => {
    const result = index("dayjs('2023-04-19')", "week", "一个设置weekStart为1的语言包");
    expect(result).toBe("一个新的Dayjs实例，表示2023-04-17（周一）的开始");
  });

  test('TC029: 测试Dayjs.startOf：单位是\'hour\'且是结束（通过endOf调用）', () => {
    const result = index("dayjs('2023-04-15T12:30:45.123')", "hour");
    expect(result).toBe("一个新的Dayjs实例，表示2023-04-15T12:59:59.999");
  });

  test('TC030: 测试Dayjs.startOf：单位不匹配任何case，返回克隆体', () => {
    const result = index("dayjs('2023-04-15')", "invalid_unit", null);
    expect(result).toBe("一个新的Dayjs实例，日期与原实例相同");
  });

  test('TC031: 测试Dayjs.$set：设置月份，且日期不会溢出（如1月15日设置为2月）', () => {
    const result = index("dayjs('2023-01-15')", "month", 1);
    expect(result).toBe("this指向的实例月份变为2月，日期仍为15日");
  });

  test('TC032: 测试Dayjs.$set：设置月份，日期溢出（如1月31日设置为2月）', () => {
    const result = index("dayjs('2023-01-31')", "month", 1);
    expect(result).toBe("this指向的实例月份变为2月，日期变为28日（2023年2月）");
  });

  test('TC033: 测试Dayjs.$set：设置日期（unit为C.D），同时调整星期（arg包含this.$D + (int - this.$W)逻辑）', () => {
    const result = index("dayjs('2023-04-15')", "day", 1);
    expect(result).toBe("this指向的实例星期变为1（但此逻辑由$set用于内部，通常set('day')调用$set('D')）");
  });

  test('TC034: 测试Dayjs.set：调用公共set方法，应返回新实例，不影响原实例', () => {
    const result = index("dayjs('2023-04-15')", "month", 5);
    expect(result).toBe("一个新的Dayjs实例，月份为6月，原实例月份不变");
  });

  test('TC035: 测试Dayjs.get：获取月份', () => {
    const result = index("dayjs('2023-04-15')", "month");
    expect(result).toBe(3);
  });

  test('TC036: 测试Dayjs.add：增加月份', () => {
    const result = index("dayjs('2023-01-31')", 1, "month");
    expect(result).toBe("一个新的Dayjs实例，表示2023-02-28");
  });

  test('TC037: 测试Dayjs.add：增加天数', () => {
    const result = index("dayjs('2023-04-15')", 10, "day");
    expect(result).toBe("一个新的Dayjs实例，表示2023-04-25");
  });

  test('TC038: 测试Dayjs.add：增加小时（通过毫秒计算）', () => {
    const result = index("dayjs('2023-04-15T12:00:00')", 1.5, "hour");
    expect(result).toBe("一个新的Dayjs实例，表示2023-04-15T13:30:00");
  });

  test('TC039: 测试Dayjs.subtract：减少天数（内部调用add）', () => {
    const result = index("dayjs('2023-04-15')", 5, "day");
    expect(result).toBe("一个新的Dayjs实例，表示2023-04-10");
  });

  test('TC040: 测试Dayjs.format：无效日期，返回语言包配置的invalidDate或默认字符串', () => {
    expect(() => { index("dayjs(null)", "YYYY-MM-DD"); }).toThrow();
  });

  test('TC041: 测试Dayjs.format：有效日期，使用默认格式字符串', () => {
    const result = index("dayjs('2023-04-15T12:30:45.123')", null);
    expect(result).toBe("2023-04-15T12:30:45.123+00:00");
  });

  test('TC042: 测试Dayjs.format：覆盖多个格式匹配项（如YYYY, MM, DD, HH, mm, ss, SSS, a, dddd）', () => {
    const result = index("dayjs('2023-04-15T14:30:45.123')", "YYYY-MM-DD HH:mm:ss.SSS A dddd");
    expect(result).toBe("2023-04-15 14:30:45.123 PM Saturday （英文环境）");
  });

  test('TC043: 测试Dayjs.utcOffset：时区偏移量取整到15分钟（模拟修复的FF24 bug）', () => {
    const result = index("dayjs()");
    expect(result).toBe("一个能被15整除的分钟数");
  });

  test('TC044: 测试Dayjs.diff：计算两个日期的月份差（浮点数）', () => {
    const result = index("dayjs('2023-06-15')", "2022-12-10", "month", true);
    expect(result).toBe("一个浮点数（如6.xx）");
  });

  test('TC045: 测试Dayjs.diff：计算两个日期的天数差，且时区不同，考虑zoneDelta', () => {
    const result = index("dayjs('2023-04-15T00:00:00+08:00')", "2023-04-15T00:00:00+00:00", "day", false);
    expect(result).toBe("0 或 -1 （取决于算法）");
  });

  test('TC046: 测试Dayjs.daysInMonth：获取当月天数', () => {
    const result = index("dayjs('2023-02-15')");
    expect(result).toBe(28);
  });

  test('TC047: 测试Dayjs.$locale：获取当前实例的语言配置', () => {
    const result = index("dayjs().locale('zh-cn')");
    expect(result).toBe("中文语言包对象");
  });

  test('TC048: 测试Dayjs.locale：切换语言（返回新实例）', () => {
    const result = index("dayjs('2023-04-15')", "zh-cn", null);
    expect(result).toBe("一个新的Dayjs实例，其$L属性为'zh-cn'");
  });

  test('TC049: 测试Dayjs.clone：克隆实例', () => {
    const result = index("dayjs('2023-04-15')");
    expect(result).toBe("一个新的Dayjs实例，所有内部属性值相同，但不是同一个引用");
  });

  test('TC050: 测试Dayjs.toJSON：有效日期返回ISO字符串，无效返回null', () => {
    const result = index("dayjs('2023-04-15')");
    expect(result).toBe("'2023-04-15T00:00:00.000Z'");
  });

  test('TC051: 测试Dayjs.toJSON：无效日期返回null', () => {
    const result = index("dayjs(null)");
    expect(result).toBe(null);
  });

  test('TC052: 测试原型快捷方法：.year()作为getter和setter', () => {
    const result = index("dayjs('2023-04-15')", "先get后set").year();
    expect(result).toBe("get返回2023，set后返回一个新的2024年实例");
  });

  test('TC053: 测试静态方法dayjs.extend：安装插件（仅一次）', () => {
    const result = index("一个包含$i属性的函数", "插件选项");
    expect(result).toBe("dayjs函数本身（链式调用）");
  });

  test('TC054: 测试静态方法dayjs.isDayjs：判断对象', () => {
    const result = index("一个普通对象");
    expect(result).toBe(false);
  });

  test('TC055: 测试静态方法dayjs.unix：从秒级时间戳创建', () => {
    const result = index(1681527600);
    expect(result).toBe("一个Dayjs实例，表示2023-04-15 12:30:00");
  });

  test('TC_SUP_001: 测试 parseLocale 当 preset 为字符串且 Ls 中已存在时', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_003: 测试 parseLocale 当 preset 为带连字符的字符串时', () => {
    const result = index("en-US", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_005: 测试 parseLocale 当 isLocal 为 true 时不影响全局 L', () => {
    const result = index("es", null, true);
    expect(result).toBe("es");
  });

  test('TC_SUP_007: 测试 parseDate 当 date 为 null 时', () => {
    const result = index(null, false);
    expect(result).toBe("Date 对象，值为 NaN");
  });

  test('TC_SUP_009: 测试 parseDate 当 date 是字符串且 utc 为 true 时', () => {
    const result = index("2023-01-01T12:00:00", true);
    expect(result).toBe("UTC 时间的 Date 对象");
  });

  test('TC_SUP_010: 测试 Dayjs.$utils 方法返回 Utils', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_011: 测试 isSame 方法带 units 参数', () => {
    const result = index("2023-01-01", "2023-01-01", "day");
    expect(result).toBe(true);
  });

  test('TC_SUP_012: 测试 $g 方法当 input 未定义时返回 get，否则调用 set', () => {
    const result = index("$D", 15);
    expect(result).toBe("设置后的 Dayjs 实例");
  });

  test('TC_SUP_013: 测试 startOf 方法所有 unit cases，包括 week 和小时等', () => {
    const result = index("2023-06-15T12:30:45", "week", true);
    expect(result).toBe("一周开始的 Dayjs 实例");
  });

  test('TC_SUP_014: 测试 $set 方法当 unit 是月份时', () => {
    const result = index("2023-01-15", "month", 5);
    expect(result).toBe("月份设置为 5 的 Dayjs 实例");
  });

  test('TC_SUP_015: 测试 add 方法对不同 units，如周和分钟', () => {
    const result = index("2023-01-01", 2, "week");
    expect(result).toBe("增加两周后的 Dayjs 实例");
  });

  test('TC_SUP_016: 测试 format 方法的各种格式字符串，如 MMM 和 Z', () => {
    const result = index("2023-06-15T14:30:00", "YYYY-MM-DD HH:mm:ss Z");
    expect(result).toBe("格式化后的字符串");
  });

  test('TC_SUP_017: 测试 diff 方法对年、月等 units，带 float 参数', () => {
    const result = index("2023-01-01", "2024-01-01", "year", true);
    expect(result).toBe(1);
  });

  test('TC_SUP_018: 测试 locale 方法当 preset 为空时返回当前 $L', () => {
    const result = index("2023-01-01", null, null);
    expect(result).toBe("当前 locale 名称");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_020: 测试 dayjs.unix 函数', () => {
    const result = index(1672531200);
    expect(result).toBe("对应时间的 Dayjs 实例");
  });

  test('TC_SUP_001: 调用 parseLocale，preset 为字符串 \'en\'，object 为 null，isLocal 为 false，覆盖已存在 locale 的分支', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 调用 parseLocale，preset 为字符串 \'fr\'，object 为自定义 locale 对象，isLocal 为 false，覆盖设置新 locale 的分支', () => {
    const result = index("fr", {"name": "fr", "weekdays": []}, false);
    expect(result).toBe("fr");
  });

  test('TC_SUP_003: 调用 parseLocale，preset 为带连字符的字符串 \'zh-CN\'，object 为 null，isLocal 为 false，覆盖递归调用分支', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("zh");
  });

  test('TC_SUP_004: 调用 parseLocale，preset 为 locale 对象，isLocal 为 false，覆盖对象分支', () => {
    const result = index({"name": "custom", "weekdays": []}, null, false);
    expect(result).toBe("custom");
  });

  test('TC_SUP_005: 调用 parseLocale，preset 为字符串 \'en\'，isLocal 为 true，覆盖不设置全局 locale 的分支', () => {
    const result = index("en", null, true);
    expect(result).toBe("en");
  });

  test('TC_SUP_006: 调用 dayjs 函数，输入为 dayjs 实例，覆盖克隆分支', () => {
    const result = index("dayjs_instance", null);
    expect(result).toBe("克隆的 dayjs 实例");
  });

  test('TC_SUP_007: 调用 parseDate，date 为 Date 实例，utc 为 false', () => {
    const result = index("new Date()", false);
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_008: 调用 parseDate，date 为字符串且 utc 为 true，覆盖 UTC 解析分支', () => {
    const result = index("2023-01-01T00:00:00", true);
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_009: 调用 $utils 方法，返回 Utils 对象', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_010: 调用 isSame 方法，带 units 参数', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe("布尔值");
  });

  test('TC_SUP_011: 调用 isAfter 方法，带 units 参数', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe("布尔值");
  });

  test('TC_SUP_012: 调用 isBefore 方法，带 units 参数', () => {
    const result = index("2023-01-01", "day");
    expect(result).toBe("布尔值");
  });

  test('TC_SUP_013: 调用 $g 方法，input 有值，触发 set 分支', () => {
    const result = index(1, "$D", "D");
    expect(result).toBe("设置后的实例");
  });

  test('TC_SUP_014: 调用 unix 方法，返回 Unix 时间戳', () => {
    const result = index();
    expect(result).toBe("数字");
  });

  test('TC_SUP_015: 调用 valueOf 方法，返回时间戳', () => {
    const result = index();
    expect(result).toBe("数字");
  });

  test('TC_SUP_016: 调用 startOf 方法，units 为 \'year\'，startOf 为 true', () => {
    const result = index("year", true);
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_017: 调用 startOf 方法，units 为 \'week\'，startOf 为 false', () => {
    const result = index("week", false);
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_018: 调用 endOf 方法，参数为 \'day\'', () => {
    const result = index("day");
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_019: 调用 $set 方法，units 为 \'month\'，int 为 1，覆盖月份设置分支', () => {
    const result = index("month", 1);
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_020: 调用 set 方法，设置日期', () => {
    const result = index("date", 15);
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_021: 调用 get 方法，获取月份', () => {
    const result = index("month");
    expect(result).toBe("数字");
  });

  test('TC_SUP_022: 调用 add 方法，添加天数', () => {
    const result = index(5, "day");
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_023: 调用 add 方法，添加分钟，覆盖 step 分支', () => {
    const result = index(10, "minute");
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_024: 调用 subtract 方法，减去年份', () => {
    const result = index(1, "year");
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_025: 调用 format 方法，带格式化字符串，覆盖无效日期分支', () => {
    const result = index("YYYY-MM-DD");
    expect(result).toBe("字符串");
  });

  test('TC_SUP_026: 调用 utcOffset 方法，返回时区偏移', () => {
    const result = index();
    expect(result).toBe("数字");
  });

  test('TC_SUP_027: 调用 diff 方法，units 为 \'month\'，float 为 true', () => {
    const result = index("2023-02-01", "month", true);
    expect(result).toBe("数字");
  });

  test('TC_SUP_028: 调用 daysInMonth 方法，返回月份天数', () => {
    const result = index();
    expect(result).toBe("数字");
  });

  test('TC_SUP_029: 调用 $locale 方法，返回 locale 对象', () => {
    const result = index();
    expect(result).toBe("locale 对象");
  });

  test('TC_SUP_030: 调用 locale 方法，preset 为 null，返回当前 locale 名称', () => {
    const result = index(null, null);
    expect(result).toBe("字符串");
  });

  test('TC_SUP_031: 调用 clone 方法，返回克隆实例', () => {
    const result = index();
    expect(result).toBe("dayjs 实例");
  });

  test('TC_SUP_032: 调用 toDate 方法，返回 Date 对象', () => {
    const result = index();
    expect(result).toBe("Date 实例");
  });

  test('TC_SUP_033: 调用 toString 方法，返回 UTC 字符串', () => {
    const result = index();
    expect(result).toBe("字符串");
  });

  test('TC_SUP_034: 调用 dayjs.extend 方法，安装插件', () => {
    const result = index({"$i": false, "function": "plugin"}, {});
    expect(result).toBe("dayjs 函数");
  });

  test('TC_SUP_035: 调用 dayjs.unix 方法，传入 Unix 时间戳', () => {
    const result = index(1609459200);
    expect(result).toBe("dayjs 实例");
  });
});
