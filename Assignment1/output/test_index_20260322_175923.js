/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: 测试 dayjs() 工厂函数使用 null 作为输入，创建无效日期', () => {
    const result = index(null);
    expect(result).toBe("Dayjs 实例，其 .isValid() 返回 false");
  });

  test('TC004: 测试 dayjs() 工厂函数传入一个有效格式的字符串（不含Z），且 cfg.utc 为 false', () => {
    const result = index("2024-01-15 10:30:45.123");
    expect(result).toBe("Dayjs 实例，其 .$d 表示本地时间的 2024-01-15T10:30:45.123");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC006: 测试 dayjs() 工厂函数传入一个无效/不匹配正则的字符串', () => {
    expect(() => { index("Invalid Date String"); }).toThrow();
  });

  test('TC007: 测试 dayjs() 工厂函数传入一个以Z结尾的字符串', () => {
    const result = index("2024-01-15T10:30:45.123Z");
    expect(result).toBe("Dayjs 实例，其 .$d 表示该UTC时间");
  });

  test('TC008: 测试 dayjs() 工厂函数传入一个数字时间戳', () => {
    const result = index(1705314600000);
    expect(result).toBe("Dayjs 实例，其 .$d 表示 2024-01-15T10:30:00.000Z");
  });

  test('TC009: 测试 dayjs() 工厂函数传入另一个 Dayjs 实例', () => {
    const result = index("由 dayjs('2024-01-15') 创建的实例");
    expect(result).toBe("输入实例的一个克隆，与原实例值相同但引用不同");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index("一个 Dayjs 实例");
    expect(result).toBe(true);
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index(null);
    expect(result).toBe(false);
  });

  test('TC011: 测试 parseLocale 函数，传入字符串 preset（已存在），不传入 object', () => {
    const result = index("en");
    expect(result).toBe("en");
  });

  test('TC012: 测试 parseLocale 函数，传入字符串 preset（不存在），并传入 object', () => {
    const result = index("fr", "一个模拟的语言对象");
    expect(result).toBe("fr");
  });

  test('TC013: 测试 parseLocale 函数，传入带连字符的字符串 preset（如zh-cn），且 Ls[\'zh-cn\'] 不存在', () => {
    const result = index("zh-cn");
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC015: 测试 parseLocale 函数，传入空 preset', () => {
    const result = index(null);
    expect(result).toBe("L (全局语言)");
  });

  test('TC016: 测试 Dayjs 实例的 .isValid() 方法，对有效日期返回 true', () => {
    const result = index("2024-01-15").isValid();
    expect(result).toBe(true);
  });

  test('TC017: 测试 Dayjs 实例的 .isSame() 方法，两个日期相同，不带 units 参数', () => {
    const result = index("2024-01-15T10:30:00", "2024-01-15T10:30:00").isSame();
    expect(result).toBe(true);
  });

  test('TC018: 测试 Dayjs 实例的 .isSame() 方法，两个日期不同，带 units=\'month\'', () => {
    const result = index("2024-01-15T10:30:00", "2024-01-20T10:30:00", "month").isSame();
    expect(result).toBe(true);
  });

  test('TC019: 测试 Dayjs 实例的 .isAfter() 方法', () => {
    const result = index("2024-01-16", "2024-01-15", "day").isAfter();
    expect(result).toBe(true);
  });

  test('TC020: 测试 Dayjs 实例的 .isBefore() 方法', () => {
    const result = index("2024-01-14", "2024-01-15", "day").isBefore();
    expect(result).toBe(true);
  });

  test('TC021: 测试 .get() 方法获取月份', () => {
    const result = index("2024-05-15", "month").get();
    expect(result).toBe(5);
  });

  test('TC022: 测试 .set() 方法设置日期，并验证克隆行为', () => {
    const result = index("2024-01-15", "date", 25).set();
    expect(result).toBe("新 Dayjs 实例，日期为 2024-01-25");
  });

  test('TC023: 测试 .$set() 内部方法设置月份，并处理月末溢出（如从 1月31日 设置为 2月）', () => {
    const result = index("2024-01-31", "month", 1);
    expect(result).toBe("当前实例的日期变为 2024-02-29");
  });

  test('TC024: 测试 .add() 方法增加月份', () => {
    const result = index("2024-01-15", 2, "month").add();
    expect(result).toBe("Dayjs 实例，日期为 2024-03-15");
  });

  test('TC025: 测试 .add() 方法增加天数', () => {
    const result = index("2024-01-31", 1, "day").add();
    expect(result).toBe("Dayjs 实例，日期为 2024-02-01");
  });

  test('TC026: 测试 .add() 方法增加小时（通过毫秒计算）', () => {
    const result = index("2024-01-15T10:00:00", 1.5, "hour").add();
    expect(result).toBe("Dayjs 实例，日期为 2024-01-15T11:30:00");
  });

  test('TC027: 测试 .subtract() 方法', () => {
    const result = index("2024-01-15", 5, "day").subtract();
    expect(result).toBe("Dayjs 实例，日期为 2024-01-10");
  });

  test('TC028: 测试 .startOf() 方法，units=\'year\'', () => {
    const result = index("2024-05-15T10:30:45", "year").startOf();
    expect(result).toBe("Dayjs 实例，日期为 2024-01-01T00:00:00.000");
  });

  test('TC029: 测试 .startOf() 方法，units=\'week\'，且 weekStart = 1 (Monday)', () => {
    const result = index("2024-01-18", "week").startOf();
    expect(result).toBe("Dayjs 实例，日期为 2024-01-15T00:00:00.000 (假设 locale 配置 weekStart=1)");
  });

  test('TC030: 测试 .endOf() 方法，units=\'month\'', () => {
    const result = index("2024-02-15", "month").endOf();
    expect(result).toBe("Dayjs 实例，日期为 2024-02-29T23:59:59.999");
  });

  test('TC031: 测试 .format() 方法，使用多种格式符', () => {
    const result = index("2024-01-15T14:30:45.678", "YYYY-MM-DD HH:mm:ss.SSS dddd").format();
    expect(result).toBe("2024-01-15 14:30:45.678 Monday");
  });

  test('TC032: 测试 .format() 方法，对无效日期', () => {
    expect(() => { index(null, "YYYY-MM-DD").format(); }).toThrow();
  });

  test('TC033: 测试 .diff() 方法，units=\'day\', float=false', () => {
    const result = index("2024-01-20", "2024-01-15", "day", false).diff();
    expect(result).toBe(5);
  });

  test('TC034: 测试 .diff() 方法，units=\'month\', float=true', () => {
    const result = index("2024-03-15", "2024-01-01", "month", true).diff();
    expect(result).toBe(2.451612903225806);
  });

  test('TC035: 测试 .daysInMonth() 方法', () => {
    const result = index("2024-02-15").daysInMonth();
    expect(result).toBe(29);
  });

  test('TC036: 测试 .locale() 方法切换语言并返回新实例', () => {
    const result = index("2024-01-15", "fr", "一个模拟的 fr 语言对象").locale();
    expect(result).toBe("新 Dayjs 实例，其 .$L 为 'fr'");
  });

  test('TC037: 测试 .utcOffset() 方法', () => {
    const result = index("2024-01-15").utcOffset();
    expect(result).toBe("当前环境的时区偏移（分钟数，按15分钟取整）");
  });

  test('TC038: 测试 .toISOString() 和 .toJSON()（有效日期）', () => {
    const result = index("2024-01-15T10:30:45.123Z").toISOString();
    expect(result).toBe("toISOString 返回 '2024-01-15T10:30:45.123Z'， toJSON 返回相同字符串");
  });

  test('TC039: 测试 .toJSON()（无效日期）', () => {
    const result = index(null).toJSON();
    expect(result).toBe(null);
  });

  test('TC040: 测试 dayjs.unix() 静态方法', () => {
    const result = index(1705314600).unix();
    expect(result).toBe("Dayjs 实例，表示 2024-01-15T10:30:00.000Z");
  });

  test('TC041: 测试 dayjs.locale() 静态方法（设置全局语言）', () => {
    const result = index("自定义语言名", "一个模拟的语言对象").locale();
    expect(result).toBe("自定义语言名");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index("第一次调用，插件.$i 未定义");
    expect(result).toBe("dayjs 函数，插件被调用安装");
  });

  test('TC000: ', () => {
    const result = index("第二次调用，插件.$i 已为 true");
    expect(result).toBe("dayjs 函数，插件未被调用");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index("2024-01-15", "get");
    expect(result).toBe(1);
  });

  test('TC000: ', () => {
    const result = index("2024-01-15", "set", 5);
    expect(result).toBe("新 Dayjs 实例，日期为 2024-06-15");
  });

  test('TC_SUP_001: 测试 parseLocale：传入字符串 preset（locale 已存在）但不传入 object，不应覆盖现有 locale', () => {
    const result = index("en", null, false);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_003: 测试 parseLocale：传入带连字符的字符串（如\'zh-CN\'），且父级 locale 不存在', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("zh");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_007: 测试 $g 方法：不传 input，应返回 getter 值', () => {
    const result = index("$y");
    expect(result).toBe("年份数字");
  });

  test('TC_SUP_008: 测试 startOf(\'year\', false) 即 endOf(\'year\') 的逻辑', () => {
    const result = index("2023-06-15", "year", false);
    expect(result).toBe("2023-12-31 23:59:59.999");
  });

  test('TC_SUP_009: 测试 startOf(\'week\') 且 $W < weekStart，测试周起始日计算', () => {
    const result = index("2023-12-31", "week", 1);
    expect(result).toBe("2023-12-25 00:00:00.000 (假设 locale 周一开始)");
  });

  test('TC_SUP_010: 测试 startOf(\'hour\'), startOf(\'minute\'), startOf(\'second\') 路径', () => {
    const result = index("2023-01-01 12:30:45.678", ["hour", "minute", "second"]);
    expect(result).toBe("['2023-01-01 12:00:00.000', '2023-01-01 12:30:00.000', '2023-01-01 12:30:45.000']");
  });

  test('TC_SUP_011: 测试 $set 方法：设置月份（unit === C.M）', () => {
    const result = index("2023-01-31", "month", 1);
    expect(result).toBe("2023-02-28 (防止日期溢出)");
  });

  test('TC_SUP_012: 测试 $set 方法：设置其他单位（如小时）', () => {
    const result = index("2023-01-01", "hour", 15);
    expect(result).toBe("2023-01-01 15:00:00.000");
  });

  test('TC_SUP_013: 测试 add 方法：增加天数（unit === C.D），触发 instanceFactorySet', () => {
    const result = index("2023-01-01", 5, "day");
    expect(result).toBe("2023-01-06");
  });

  test('TC_SUP_014: 测试 add 方法：增加周数（unit === C.W）', () => {
    const result = index("2023-01-01", 2, "week");
    expect(result).toBe("2023-01-15");
  });

  test('TC_SUP_015: 测试 format 方法：使用各种未覆盖的格式标记', () => {
    const result = index("2023-05-15 14:30:45.678", "YY-M-MMM-MMMM-D-d-SSS");
    expect(result).toBe("23-5-May-May-15-1-678");
  });

  test('TC_SUP_016: 测试 format 方法：使用 12 小时制相关标记 (h, hh, a, A) 和分钟标记 (m)', () => {
    const result = index("2023-01-01 00:30:00", "h-hh-a-A-m");
    expect(result).toBe("12-12-am-AM-30");
  });

  test('TC_SUP_017: 测试 format 方法：匹配未覆盖的 switch case 和默认情况', () => {
    const result = index("2023-01-01", "YYYY-[unmatched]");
    expect(result).toBe("2023-[unmatched]");
  });

  test('TC_SUP_018: 测试 diff 方法：计算月份差（unit === C.M），且 float = false', () => {
    const result = index("2023-01-15", "2023-03-10", "month", false);
    expect(result).toBe(1);
  });

  test('TC_SUP_019: 测试 diff 方法：计算季度、周、天、小时、分钟、秒差', () => {
    const result = index("2023-01-01 00:00:00", "2023-04-01 12:00:00", ["quarter", "week", "day", "hour", "minute", "second"], true);
    expect(result).toBe("[1.0, 13.0, 91.5, 2196.0, 131760.0, 7905600.0]");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_021: 测试 $utils 方法', () => {
    const result = index();
    expect(result).toBe("Utils 对象");
  });

  test('TC_SUP_022: 测试原型上快捷方法（如 .year(), .month() 等）的 setter 路径', () => {
    const result = index("2023-01-01", "year", 2024).year();
    expect(result).toBe("2024-01-01");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_024: 测试 dayjs.unix 方法', () => {
    const result = index(1672531200);
    expect(result).toBe("2023-01-01 00:00:00 (UTC)");
  });

  test('TC_SUP_025: 测试 toString 方法', () => {
    const result = index("2023-01-01T00:00:00Z");
    expect(result).toBe("Sun, 01 Jan 2023 00:00:00 GMT");
  });

  test('TC_SUP_001: 测试parseLocale当preset为字符串且object不为空时，设置新locale并返回locale名称', () => {
    const result = index("zh-cn", {"name": "zh-cn", "weekdays": []}, false);
    expect(result).toBe("zh-cn");
  });

  test('TC_SUP_002: 测试parseLocale当preset为字符串且包含连字符，但基础locale不存在时，递归调用', () => {
    const result = index("zh-CN", null, false);
    expect(result).toBe("en");
  });

  test('TC_SUP_003: 测试parseLocale当preset为对象时，直接设置locale并返回名称', () => {
    const result = index({"name": "fr", "weekdays": []}, null, false);
    expect(result).toBe("fr");
  });

  test('TC_SUP_004: 测试parseLocale当isLocal为true时，不更新全局L', () => {
    const result = index("es", {"name": "es"}, true);
    expect(result).toBe("es");
  });

  test('TC_SUP_005: 测试dayjs函数当date是dayjs对象时返回克隆', () => {
    const result = index("dayjs_instance", null);
    expect(result).toBe("cloned dayjs instance");
  });

  test('TC_SUP_006: 测试parseDate当utc为true时使用Date.UTC解析日期字符串，部分字段缺失', () => {
    const result = index("2023-01", true);
    expect(result).toBe("Date object representing UTC 2023-01-01");
  });

  test('TC_SUP_007: 测试Dayjs实例的$utils方法返回Utils对象', () => {
    const result = index("dayjs_instance");
    expect(result).toBe("Utils object");
  });

  test('TC_SUP_008: 测试$g方法当input有值时调用set方法', () => {
    const result = index("dayjs_instance", 2024, "$y", "year");
    expect(result).toBe("dayjs instance with year set to 2024");
  });

  test('TC_SUP_009: 测试startOf方法当units为year且isStartOf为false（即endOf year）', () => {
    const result = index("dayjs_instance", "year", false);
    expect(result).toBe("dayjs instance representing end of year");
  });

  test('TC_SUP_010: 测试startOf方法当units为week，且locale的weekStart设置为1（周一）', () => {
    const result = index("dayjs_instance_with_custom_locale", "week");
    expect(result).toBe("dayjs instance representing start of week based on custom weekStart");
  });

  test('TC_SUP_011: 测试startOf方法当units为hour, minute, second', () => {
    const result = index("dayjs_instance", ["hour", "minute", "second"]);
    expect(result).toBe("dayjs instances representing start of hour, minute, second");
  });

  test('TC_SUP_012: 测试$set方法当units为month时，调整日期并处理月份天数', () => {
    const result = index("dayjs_instance", "month", 2);
    expect(result).toBe("dayjs instance with month set and date adjusted");
  });

  test('TC_SUP_013: 测试$set方法当units为day时，直接设置日期', () => {
    const result = index("dayjs_instance", "day", 15);
    expect(result).toBe("dayjs instance with day set to 15");
  });

  test('TC_SUP_014: 测试add方法当units为day时，使用instanceFactorySet', () => {
    const result = index("dayjs_instance", 1, "day");
    expect(result).toBe("dayjs instance with one day added");
  });

  test('TC_SUP_015: 测试add方法当units为month时，直接设置月份', () => {
    const result = index("dayjs_instance", 1, "month");
    expect(result).toBe("dayjs instance with one month added");
  });

  test('TC_SUP_016: 测试format方法当locale的monthsShort是函数时，调用函数获取值', () => {
    const result = index("dayjs_instance_with_custom_locale_func", "MMM");
    expect(result).toBe("Custom month short name");
  });

  test('TC_SUP_017: 测试format方法的小时格式化，使用12小时制（小时为13时）', () => {
    const result = index("dayjs_instance", "h");
    expect(result).toBe("1");
  });

  test('TC_SUP_018: 测试format方法的meridiem格式化，下午且小写', () => {
    const result = index("dayjs_instance", "a");
    expect(result).toBe("pm");
  });

  test('TC_SUP_019: 测试format方法的各种格式匹配，覆盖未覆盖的switch cases', () => {
    const result = index("dayjs_instance", "YY M MMM MMMM D d dd ddd dddd H h hh a A m s SSS");
    expect(result).toBe("Formatted string with all tokens");
  });

  test('TC_SUP_020: 测试diff方法的各种单位计算（年、月、季度、周、天、小时、分钟、秒）', () => {
    const result = index("dayjs_instance1", "dayjs_instance2", ["year", "month", "quarter", "week", "day", "hour", "minute", "second"]);
    expect(result).toBe("Difference values for each unit");
  });

  test('TC_SUP_021: 测试diff方法当float为true时返回浮点数', () => {
    const result = index("dayjs_instance1", "dayjs_instance2", "day", true);
    expect(result).toBe("Floating point difference");
  });

  test('TC_SUP_022: 测试locale方法当preset存在时更新实例的locale', () => {
    const result = index("dayjs_instance", "zh-cn", null);
    expect(result).toBe("dayjs instance with updated locale");
  });

  test('TC_SUP_023: 测试locale方法当preset无效时，不更新locale', () => {
    const result = index("dayjs_instance", "invalid-locale", null);
    expect(result).toBe("cloned dayjs instance with original locale");
  });

  test('TC_SUP_024: 测试toString方法返回UTC字符串', () => {
    const result = index("dayjs_instance");
    expect(result).toBe("UTC string from $d.toUTCString()");
  });

  test('TC_SUP_025: 测试dayjs.extend方法当插件未安装时安装插件', () => {
    const result = index("plugin_function", {});
    expect(result).toBe("dayjs function");
  });

  test('TC_SUP_026: 测试dayjs.extend方法当插件已安装时不重复安装', () => {
    const result = index("plugin_with_i", {});
    expect(result).toBe("dayjs function");
  });

  test('TC_SUP_027: 测试dayjs.unix方法从时间戳创建实例', () => {
    const result = index(1609459200);
    expect(result).toBe("dayjs instance representing 2021-01-01");
  });
});
