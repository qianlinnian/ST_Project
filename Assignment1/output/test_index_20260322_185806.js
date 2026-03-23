/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: isDayjs: Input is a Dayjs instance', () => {
    const result = index("new Dayjs({ date: new Date() })");
    expect(result).toBe("true");
  });

  test('TC002: isDayjs: Input is an object with $isDayjsObject property', () => {
    const result = index("{ $isDayjsObject: true }");
    expect(result).toBe("true");
  });

  test('TC003: isDayjs: Input is a plain object without $isDayjsObject', () => {
    const result = index("{}");
    expect(result).toBe("false");
  });

  test('TC004: isDayjs: Input is null', () => {
    const result = index("null");
    expect(result).toBe("false");
  });

  test('TC005: parseLocale: preset is null/undefined, return global L', () => {
    const result = index("null", "null", "false");
    expect(result).toBe("'en'");
  });

  test('TC006: parseLocale: preset is existing string locale, no object, not local', () => {
    const result = index("'en'", "null", "false");
    expect(result).toBe("'en'");
  });

  test('TC007: parseLocale: preset is new string locale, with object, not local', () => {
    const result = index("'fr'", "{ name: 'fr', weekdays: ['Dimanche'] }", "false");
    expect(result).toBe("'fr'");
  });

  test('TC008: parseLocale: preset is \'zh-cn\', triggers recursive call to \'zh\'', () => {
    const result = index("'zh-cn'", "null", "false");
    expect(result).toBe("'en'");
  });

  test('TC009: parseLocale: preset is object locale, not local', () => {
    const result = index("{ name: 'es', weekdays: ['Domingo'] }", "null", "false");
    expect(result).toBe("'es'");
  });

  test('TC010: parseLocale: preset is new string locale, with object, is local (don\'t update global L)', () => {
    const result = index("'de'", "{ name: 'de', weekdays: ['Sonntag'] }", "true");
    expect(result).toBe("'de'");
  });

  test('TC011: dayjs: Input is a Dayjs instance, should clone', () => {
    const result = index("dayjs(new Date(2023, 0, 1))", "null");
    expect(result).toBe("Dayjs instance with date 2023-01-01, different reference than input");
  });

  test('TC012: dayjs: Input is a Date object, c is an object', () => {
    const result = index("new Date(2023, 10, 15)", "{ locale: 'fr', utc: true }");
    expect(result).toBe("New Dayjs instance with date 2023-11-15, locale 'fr', utc true");
  });

  test('TC013: dayjs: Input is a string, c is undefined', () => {
    const result = index("'2023-11-15'", "undefined");
    expect(result).toBe("New Dayjs instance with date 2023-11-15, default locale 'en', utc false");
  });

  test('TC014: parseDate: date is null', () => {
    const result = index("{ date: null }");
    expect(result).toBe("Date(NaN)");
  });

  test('TC015: parseDate: date is undefined', () => {
    const result = index("{ date: undefined }");
    expect(result).toBe("Current Date object");
  });

  test('TC016: parseDate: date is a Date object', () => {
    const result = index("{ date: new Date(2023, 10, 15) }");
    expect(result).toBe("New Date object for 2023-11-15 (clone)");
  });

  test('TC017: parseDate: date is a string matching REGEX_PARSE, not ending with Z, utc false', () => {
    const result = index("{ date: '2023-11-15 10:30:45.123', utc: false }");
    expect(result).toBe("Local Date object for 2023-11-15 10:30:45.123");
  });

  test('TC018: parseDate: date is a string matching REGEX_PARSE, not ending with Z, utc true', () => {
    const result = index("{ date: '2023-11-15 10:30:45.123', utc: true }");
    expect(result).toBe("UTC Date object for 2023-11-15 10:30:45.123");
  });

  test('TC019: parseDate: date is a string not matching REGEX_PARSE, not ending with Z', () => {
    const result = index("{ date: 'invalid date string', utc: false }");
    expect(result).toBe("Date(NaN)");
  });

  test('TC020: parseDate: date is a string ending with Z (ISO format), bypass regex', () => {
    const result = index("{ date: '2023-11-15T10:30:45.123Z', utc: false }");
    expect(result).toBe("Date object for 2023-11-15T10:30:45.123Z (parsed by native Date)");
  });

  test('TC021: parseDate: date is a number (timestamp)', () => {
    const result = index("{ date: 1700000000000 }");
    expect(result).toBe("Date object for 2023-11-15T10:13:20.000Z (or local equivalent)");
  });

  test('TC022: Dayjs.constructor: cfg.locale and cfg.x are provided', () => {
    const result = index("{ date: '2023-01-01', locale: 'fr', x: { custom: true } }");
    expect(result).toBe("Dayjs instance with $L='fr', $x={ custom: true }, $isDayjsObject=true");
  });

  test('TC023: Dayjs.constructor: cfg.locale and cfg.x are not provided', () => {
    const result = index("{ date: '2023-01-01' }");
    expect(result).toBe("Dayjs instance with $L='en', $x={}, $isDayjsObject=true");
  });

  test('TC024: Dayjs.isValid: Date is valid', () => {
    const result = index("dayjs('2023-01-01')");
    expect(result).toBe("true");
  });

  test('TC025: Dayjs.isValid: Date is invalid', () => {
    const result = index("dayjs(null)");
    expect(result).toBe("false");
  });

  test('TC026: Dayjs.isSame: Same day, same unit \'day\'', () => {
    const result = index("dayjs('2023-11-15 10:00:00')", "'2023-11-15 11:00:00'", "'day'");
    expect(result).toBe("true");
  });

  test('TC027: Dayjs.isSame: Different day, same unit \'day\'', () => {
    const result = index("dayjs('2023-11-15 10:00:00')", "'2023-11-16 10:00:00'", "'day'");
    expect(result).toBe("false");
  });

  test('TC028: Dayjs.isSame: Same month, unit \'month\'', () => {
    const result = index("dayjs('2023-11-01')", "'2023-11-15'", "'month'");
    expect(result).toBe("true");
  });

  test('TC029: Dayjs.isAfter: that is before this.startOf(units)', () => {
    const result = index("dayjs('2023-11-15')", "'2023-11-14'", "'day'");
    expect(result).toBe("true");
  });

  test('TC030: Dayjs.isAfter: that is after this.startOf(units)', () => {
    const result = index("dayjs('2023-11-15')", "'2023-11-16'", "'day'");
    expect(result).toBe("false");
  });

  test('TC031: Dayjs.isBefore: that is after this.endOf(units)', () => {
    const result = index("dayjs('2023-11-15')", "'2023-11-16'", "'day'");
    expect(result).toBe("true");
  });

  test('TC032: Dayjs.isBefore: that is before this.endOf(units)', () => {
    const result = index("dayjs('2023-11-15')", "'2023-11-14'", "'day'");
    expect(result).toBe("false");
  });

  test('TC033: Dayjs.$g: input is undefined (getter)', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "undefined", "'$H'", "'hour'");
    expect(result).toBe("10");
  });

  test('TC034: Dayjs.$g: input is defined (setter)', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "12", "'$H'", "'hour'");
    expect(result).toBe("Dayjs instance with hour set to 12");
  });

  test('TC035: Dayjs.unix: returns seconds timestamp', () => {
    const result = index("dayjs(1700000000000)");
    expect(result).toBe("1700000000");
  });

  test('TC036: Dayjs.valueOf: returns milliseconds timestamp', () => {
    const result = index("dayjs(1700000000000)");
    expect(result).toBe("1700000000000");
  });

  test('TC037: Dayjs.startOf: unit \'year\', isStartOf true (default)', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'year'", "undefined");
    expect(result).toBe("Dayjs instance for 2023-01-01 00:00:00.000");
  });

  test('TC038: Dayjs.startOf: unit \'year\', isStartOf false (endOf)', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'year'", "false");
    expect(result).toBe("Dayjs instance for 2023-12-31 23:59:59.999");
  });

  test('TC039: Dayjs.startOf: unit \'month\', isStartOf true', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'month'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-01 00:00:00.000");
  });

  test('TC040: Dayjs.startOf: unit \'month\', isStartOf false', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'month'", "false");
    expect(result).toBe("Dayjs instance for 2023-11-30 23:59:59.999");
  });

  test('TC041: Dayjs.startOf: unit \'week\', isStartOf true, weekStart 0 (Sunday)', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'week'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-12 00:00:00.000 (Sunday)");
  });

  test('TC042: Dayjs.startOf: unit \'week\', isStartOf true, weekStart 1 (Monday), $W < weekStart', () => {
    const result = index("dayjs('2023-11-12 10:30:00').locale('mock-monday-start', { weekStart: 1 })", "'week'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-06 00:00:00.000 (Monday)");
  });

  test('TC043: Dayjs.startOf: unit \'day\', isStartOf true', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'day'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-15 00:00:00.000");
  });

  test('TC044: Dayjs.startOf: unit \'hour\', isStartOf true', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'hour'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-15 10:00:00.000");
  });

  test('TC045: Dayjs.startOf: unit \'minute\', isStartOf true', () => {
    const result = index("dayjs('2023-11-15 10:30:45')", "'minute'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-15 10:30:00.000");
  });

  test('TC046: Dayjs.startOf: unit \'second\', isStartOf true', () => {
    const result = index("dayjs('2023-11-15 10:30:45.123')", "'second'", "true");
    expect(result).toBe("Dayjs instance for 2023-11-15 10:30:45.000");
  });

  test('TC047: Dayjs.startOf: invalid unit, returns clone', () => {
    const result = index("dayjs('2023-11-15')", "'invalid'", "true");
    expect(result).toBe("Cloned Dayjs instance for 2023-11-15");
  });

  test('TC048: Dayjs.endOf: unit \'day\'', () => {
    const result = index("dayjs('2023-11-15 10:30:00')", "'day'");
    expect(result).toBe("Dayjs instance for 2023-11-15 23:59:59.999");
  });

  test('TC049: Dayjs.$set: unit \'month\', no date overflow', () => {
    const result = index("dayjs('2023-01-15')", "'month'", "1");
    expect(result).toBe("Dayjs instance for 2023-02-15");
  });

  test('TC050: Dayjs.$set: unit \'month\', with date overflow', () => {
    const result = index("dayjs('2023-01-31')", "'month'", "1");
    expect(result).toBe("Dayjs instance for 2023-02-28");
  });

  test('TC051: Dayjs.$set: unit \'year\'', () => {
    const result = index("dayjs('2023-01-15')", "'year'", "2024");
    expect(result).toBe("Dayjs instance for 2024-01-15");
  });

  test('TC052: Dayjs.$set: unit \'date\'', () => {
    const result = index("dayjs('2023-01-15')", "'date'", "20");
    expect(result).toBe("Dayjs instance for 2023-01-20");
  });

  test('TC053: Dayjs.$set: unit \'hour\', utc true', () => {
    const result = index("dayjs('2023-01-15 10:00:00', { utc: true })", "'hour'", "12");
    expect(result).toBe("Dayjs instance for 2023-01-15 12:00:00 UTC");
  });

  test('TC054: Dayjs.$set: invalid unit, no name match', () => {
    const result = index("dayjs('2023-01-15')", "'invalid'", "1");
    expect(result).toBe("Original Dayjs instance (no change to $d)");
  });

  test('TC055: Dayjs.set: sets a unit and returns a new instance', () => {
    const result = index("dayjs('2023-01-15')", "'month'", "2");
    expect(result).toBe("New Dayjs instance for 2023-03-15");
  });

  test('TC056: Dayjs.get: gets a unit value', () => {
    const result = index("dayjs('2023-01-15 10:30:00')", "'hour'");
    expect(result).toBe("10");
  });

  test('TC057: Dayjs.add: add months', () => {
    const result = index("dayjs('2023-01-15')", "2", "'month'");
    expect(result).toBe("Dayjs instance for 2023-03-15");
  });

  test('TC058: Dayjs.add: add years', () => {
    const result = index("dayjs('2023-01-15')", "1", "'year'");
    expect(result).toBe("Dayjs instance for 2024-01-15");
  });

  test('TC059: Dayjs.add: add days', () => {
    const result = index("dayjs('2023-01-15')", "5", "'day'");
    expect(result).toBe("Dayjs instance for 2023-01-20");
  });

  test('TC060: Dayjs.add: add weeks', () => {
    const result = index("dayjs('2023-01-15')", "1", "'week'");
    expect(result).toBe("Dayjs instance for 2023-01-22");
  });

  test('TC061: Dayjs.add: add hours (using milliseconds calculation)', () => {
    const result = index("dayjs('2023-01-15 10:00:00')", "2", "'hour'");
    expect(result).toBe("Dayjs instance for 2023-01-15 12:00:00");
  });

  test('TC062: Dayjs.add: add milliseconds (default step)', () => {
    const result = index("dayjs('2023-01-15 10:00:00.000')", "500", "'ms'");
    expect(result).toBe("Dayjs instance for 2023-01-15 10:00:00.500");
  });

  test('TC063: Dayjs.subtract: subtract days', () => {
    const result = index("dayjs('2023-01-15')", "5", "'day'");
    expect(result).toBe("Dayjs instance for 2023-01-10");
  });

  test('TC064: Dayjs.format: Invalid date', () => {
    expect(() => { index("dayjs(null)", "null"); }).toThrow();
  });

  test('TC065: Dayjs.format: Valid date, default format', () => {
    const result = index("dayjs('2023-11-15 10:30:45.123')", "null");
    expect(result).toBe("'2023-11-15T10:30:45+XX:XX' (timezone dependent)");
  });

  test('TC066: Dayjs.format: All format tokens (YY, YYYY, M, MM, MMM, MMMM, D, DD, d, dd, ddd, dddd, H, HH, h, hh, a, A, m, mm, s, ss, SSS, Z)', () => {
    const result = index("dayjs('2023-11-05 08:05:07.009')", "'YY YYYY M MM MMM MMMM D DD d dd ddd dddd H HH h hh a A m mm s ss SSS Z [escaped]'");
    expect(result).toBe("'23 2023 11 11 Nov November 5 05 0 Su Sun Sunday 8 08 8 08 am AM 5 05 7 07 009 +XX:XX escaped' (timezone dependent)");
  });

  test('TC067: Dayjs.format: meridiemFunc: hour >= 12', () => {
    const result = index("dayjs('2023-11-05 13:05:07.009')", "'h A'");
    expect(result).toBe("'1 PM'");
  });

  test('TC068: Dayjs.format: getShort: arr is a function', () => {
    const result = index("dayjs('2023-11-05').locale('mock-func-locale', { monthsShort: (d, f) => 'FnM' })", "'MMM'");
    expect(result).toBe("'FnM'");
  });

  test('TC069: Dayjs.format: getShort: arr is null, fallback to full.slice', () => {
    const result = index("dayjs('2023-11-05').locale('mock-no-short', { monthsShort: null })", "'MMM'");
    expect(result).toBe("'Nov'");
  });

  test('TC070: Dayjs.utcOffset: returns rounded timezone offset', () => {
    const result = index("dayjs(new Date(Date.UTC(2023, 0, 1)))");
    expect(result).toBe("0 (for UTC date) or local offset rounded to 15 minutes");
  });

  test('TC071: Dayjs.diff: unit \'year\', float false', () => {
    const result = index("dayjs('2024-01-15')", "'2023-01-15'", "'year'", "false");
    expect(result).toBe("1");
  });

  test('TC072: Dayjs.diff: unit \'month\', float true', () => {
    const result = index("dayjs('2023-03-15')", "'2023-01-15'", "'month'", "true");
    expect(result).toBe("2");
  });

  test('TC073: Dayjs.diff: unit \'quarter\', float false', () => {
    const result = index("dayjs('2023-07-01')", "'2023-01-01'", "'quarter'", "false");
    expect(result).toBe("2");
  });

  test('TC074: Dayjs.diff: unit \'day\', float false, with zoneDelta', () => {
    const result = index("dayjs('2023-01-01T00:00:00.000Z', { utc: true })", "dayjs('2022-12-31T23:00:00.000', { utc: false })", "'day'", "false");
    expect(result).toBe("1");
  });

  test('TC075: Dayjs.diff: unit \'hour\', float false', () => {
    const result = index("dayjs('2023-01-01 02:00:00')", "'2023-01-01 00:00:00'", "'hour'", "false");
    expect(result).toBe("2");
  });

  test('TC076: Dayjs.diff: unit \'minute\', float false', () => {
    const result = index("dayjs('2023-01-01 00:02:00')", "'2023-01-01 00:00:00'", "'minute'", "false");
    expect(result).toBe("2");
  });

  test('TC077: Dayjs.diff: unit \'second\', float false', () => {
    const result = index("dayjs('2023-01-01 00:00:02')", "'2023-01-01 00:00:00'", "'second'", "false");
    expect(result).toBe("2");
  });

  test('TC078: Dayjs.diff: default unit (milliseconds), float false', () => {
    const result = index("dayjs('2023-01-01 00:00:00.002')", "'2023-01-01 00:00:00.000'", "'invalid'", "false");
    expect(result).toBe("2");
  });

  test('TC079: Dayjs.daysInMonth: returns correct days for a month', () => {
    const result = index("dayjs('2023-02-15')");
    expect(result).toBe("28");
  });

  test('TC080: Dayjs.$locale: returns current locale object', () => {
    const result = index("dayjs('2023-01-01')");
    expect(result).toBe("en locale object");
  });

  test('TC081: Dayjs.locale: no preset, returns current locale name', () => {
    const result = index("dayjs('2023-01-01')", "null", "null");
    expect(result).toBe("'en'");
  });

  test('TC082: Dayjs.locale: with preset, returns new instance with new locale', () => {
    const result = index("dayjs('2023-01-01')", "'fr'", "{ name: 'fr', weekdays: ['Dimanche'] }");
    expect(result).toBe("New Dayjs instance with $L='fr'");
  });

  test('TC083: Dayjs.clone: returns a new instance with same date and config', () => {
    const result = index("dayjs('2023-01-01', { utc: true })");
    expect(result).toBe("New Dayjs instance for 2023-01-01, utc true, different reference");
  });

  test('TC084: Dayjs.toDate: returns a native Date object', () => {
    const result = index("dayjs('2023-01-01')");
    expect(result).toBe("Native Date object for 2023-01-01");
  });

  test('TC085: Dayjs.toJSON: valid date, returns ISO string', () => {
    const result = index("dayjs('2023-01-01')");
    expect(result).toBe("'2023-01-01TXX:XX:XX.XXXS' (ISO string)");
  });

  test('TC086: Dayjs.toJSON: invalid date, returns null', () => {
    const result = index("dayjs(null)");
    expect(result).toBe("null");
  });

  test('TC087: Dayjs.toISOString: returns ISO string', () => {
    const result = index("dayjs('2023-01-01T10:30:00.000Z')");
    expect(result).toBe("'2023-01-01T10:30:00.000Z'");
  });

  test('TC088: Dayjs.toString: returns UTC string', () => {
    const result = index("dayjs('2023-01-01T10:30:00.000Z')");
    expect(result).toBe("'Sun, 01 Jan 2023 10:30:00 GMT'");
  });

  test('TC089: Prototype method: millisecond() getter', () => {
    const result = index("dayjs('2023-01-01 10:30:45.123')", "'millisecond'", "undefined");
    expect(result).toBe("123");
  });

  test('TC090: Prototype method: second() setter', () => {
    const result = index("dayjs('2023-01-01 10:30:45.123')", "'second'", "50");
    expect(result).toBe("Dayjs instance with seconds set to 50");
  });

  test('TC091: Prototype method: month() getter', () => {
    const result = index("dayjs('2023-01-01')", "'month'", "undefined");
    expect(result).toBe("0");
  });

  test('TC092: Prototype method: year() setter', () => {
    const result = index("dayjs('2023-01-01')", "'year'", "2024");
    expect(result).toBe("Dayjs instance with year set to 2024");
  });

  test('TC093: dayjs.extend: plugin not installed yet', () => {
    const result = index("function mockPlugin(option, Dayjs, dayjs) { mockPlugin.called = true; mockPlugin.option = option; }", "{ foo: 'bar' }");
    expect(result).toBe("dayjs instance, mockPlugin.called = true, mockPlugin.option = { foo: 'bar' }, mockPlugin.$i = true");
  });

  test('TC094: dayjs.extend: plugin already installed', () => {
    const result = index("function mockPluginInstalled() { mockPluginInstalled.called = true; }; mockPluginInstalled.$i = true;", "{ foo: 'bar' }");
    expect(result).toBe("dayjs instance, mockPluginInstalled.called = undefined");
  });

  test('TC095: dayjs.locale: sets global locale', () => {
    const result = index("'fr'", "{ name: 'fr', weekdays: ['Dimanche'] }");
    expect(result).toBe("'fr'");
  });

  test('TC096: dayjs.isDayjs: calls isDayjs helper', () => {
    const result = index("dayjs(new Date())");
    expect(result).toBe("true");
  });

  test('TC097: dayjs.unix: creates instance from seconds timestamp', () => {
    const result = index("1700000000");
    expect(result).toBe("Dayjs instance for 2023-11-15T10:13:20.000Z (or local equivalent)");
  });

  test('TC_SUP_001: 测试 parseLocale: preset为已存在的字符串locale，无object，isLocal为false', () => {
    const result = index("parseLocale", ["en", null, false]);
    expect(result).toBe("en");
  });

  test('TC_SUP_002: 测试 parseLocale: preset为不存在的字符串locale，无object，无连字符，isLocal为false', () => {
    const result = index("parseLocale", ["fr", null, false]);
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_004: 测试 parseLocale: preset为带连字符的字符串locale，不存在，无object，isLocal为false (触发递归)', () => {
    const result = index("parseLocale", ["en-gb", null, false]);
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

  test('TC_SUP_007: 测试 dayjs: date参数为Dayjs对象 (触发clone)', () => {
    const result = index("dayjs", ["2023-01-01"]);
    expect(result).toBe("Dayjs object for 2023-01-01");
  });

  test('TC_SUP_008: 测试 parseDate: date参数为null', () => {
    expect(() => { index("dayjs", [null]); }).toThrow();
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_013: 测试 Dayjs.$utils() 方法', () => {
    const result = index("$utils", "dayjs()");
    expect(result).toBe("Utils object");
  });

  test('TC_SUP_014: 测试 Dayjs.isSame() 方法', () => {
    const result = index("isSame", "dayjs('2023-01-01')", ["2023-01-01", "day"]).isSame();
    expect(result).toBe(true);
  });

  test('TC_SUP_015: 测试 Dayjs.isAfter() 方法', () => {
    const result = index("isAfter", "dayjs('2023-01-02')", ["2023-01-01", "day"]).isAfter();
    expect(result).toBe(true);
  });

  test('TC_SUP_016: 测试 Dayjs.isBefore() 方法', () => {
    const result = index("isBefore", "dayjs('2023-01-01')", ["2023-01-02", "day"]).isBefore();
    expect(result).toBe(true);
  });

  test('TC_SUP_019: 测试 Dayjs.unix() 方法', () => {
    const result = index("unix", "dayjs('2023-01-01T00:00:00.000Z')").unix();
    expect(result).toBe(1672531200);
  });

  test('TC_SUP_020: 测试 Dayjs.valueOf() 方法', () => {
    const result = index("valueOf", "dayjs('2023-01-01T00:00:00.000Z')").valueOf();
    expect(result).toBe(1672531200000);
  });

  test('TC_SUP_021: 测试 Dayjs.startOf(\'year\') (isStartOf为true，本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15')", ["year"]);
    expect(result).toBe("Dayjs object for 2023-01-01 00:00:00.000 local");
  });

  test('TC_SUP_022: 测试 Dayjs.endOf(\'year\') (isStartOf为false，本地时间)', () => {
    const result = index("endOf", "dayjs('2023-06-15')", ["year"]);
    expect(result).toBe("Dayjs object for 2023-12-31 23:59:59.999 local");
  });

  test('TC_SUP_023: 测试 Dayjs.startOf(\'month\') (本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15')", ["month"]);
    expect(result).toBe("Dayjs object for 2023-06-01 00:00:00.000 local");
  });

  test('TC_SUP_024: 测试 Dayjs.endOf(\'month\') (本地时间)', () => {
    const result = index("endOf", "dayjs('2023-06-15')", ["month"]);
    expect(result).toBe("Dayjs object for 2023-06-30 23:59:59.999 local");
  });

  test('TC_SUP_025: 测试 Dayjs.startOf(\'week\') (本地时间, $W >= weekStart)', () => {
    const result = index("startOf", "dayjs('2023-06-15')", ["week"]);
    expect(result).toBe("Dayjs object for 2023-06-11 00:00:00.000 local");
  });

  test('TC_SUP_026: 测试 Dayjs.endOf(\'week\') (本地时间, $W >= weekStart)', () => {
    const result = index("endOf", "dayjs('2023-06-15')", ["week"]);
    expect(result).toBe("Dayjs object for 2023-06-17 23:59:59.999 local");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_028: 测试 Dayjs.startOf(\'day\') (本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15 12:30:45')", ["day"]);
    expect(result).toBe("Dayjs object for 2023-06-15 00:00:00.000 local");
  });

  test('TC_SUP_029: 测试 Dayjs.endOf(\'day\') (本地时间)', () => {
    const result = index("endOf", "dayjs('2023-06-15 12:30:45')", ["day"]);
    expect(result).toBe("Dayjs object for 2023-06-15 23:59:59.999 local");
  });

  test('TC_SUP_030: 测试 Dayjs.startOf(\'hour\') (本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15 12:30:45')", ["hour"]);
    expect(result).toBe("Dayjs object for 2023-06-15 12:00:00.000 local");
  });

  test('TC_SUP_031: 测试 Dayjs.startOf(\'minute\') (本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15 12:30:45')", ["minute"]);
    expect(result).toBe("Dayjs object for 2023-06-15 12:30:00.000 local");
  });

  test('TC_SUP_032: 测试 Dayjs.startOf(\'second\') (本地时间)', () => {
    const result = index("startOf", "dayjs('2023-06-15 12:30:45.789')", ["second"]);
    expect(result).toBe("Dayjs object for 2023-06-15 12:30:45.000 local");
  });

  test('TC_SUP_033: 测试 Dayjs.startOf() (未知单位，触发default)', () => {
    const result = index("startOf", "dayjs('2023-06-15')", ["unknown"]).startOf();
    expect(result).toBe("Dayjs object for 2023-06-15 00:00:00.000 local");
  });

  test('TC_SUP_034: 测试 Dayjs.startOf() (UTC模式)', () => {
    const result = index("startOf", "dayjs('2023-06-15').utc(true)", ["year"]).startOf();
    expect(result).toBe("Dayjs object for 2023-01-01 00:00:00.000 UTC");
  });

  test('TC_SUP_035: 测试 Dayjs.$set(\'year\') (本地时间)', () => {
    const result = index("$set", "dayjs('2023-06-15')", ["year", 2025]);
    expect(result).toBe("Dayjs object with year 2025");
  });

  test('TC_SUP_036: 测试 Dayjs.$set(\'month\') (本地时间，触发日期调整)', () => {
    const result = index("$set", "dayjs('2023-01-31')", ["month", 1]);
    expect(result).toBe("Dayjs object for 2023-02-28");
  });

  test('TC_SUP_037: 测试 Dayjs.$set(\'date\') (本地时间)', () => {
    const result = index("$set", "dayjs('2023-06-15')", ["date", 20]);
    expect(result).toBe("Dayjs object with date 20");
  });

  test('TC_SUP_038: 测试 Dayjs.$set(\'hour\') (本地时间)', () => {
    const result = index("$set", "dayjs('2023-06-15')", ["hour", 10]);
    expect(result).toBe("Dayjs object with hour 10");
  });

  test('TC_SUP_039: 测试 Dayjs.$set() (未知单位，name为falsy)', () => {
    const result = index("$set", "dayjs('2023-06-15')", ["unknown", 10]);
    expect(result).toBe("Dayjs object for 2023-06-15");
  });

  test('TC_SUP_040: 测试 Dayjs.$set(\'year\') (UTC模式)', () => {
    const result = index("$set", "dayjs('2023-06-15').utc(true)", ["year", 2025]);
    expect(result).toBe("Dayjs object with year 2025 UTC");
  });

  test('TC_SUP_041: 测试 Dayjs.set(\'year\')', () => {
    const result = index("set", "dayjs('2023-06-15')", ["year", 2025]);
    expect(result).toBe("Dayjs object with year 2025");
  });

  test('TC_SUP_042: 测试 Dayjs.get(\'year\')', () => {
    const result = index("get", "dayjs('2023-06-15')", ["year"]);
    expect(result).toBe(2023);
  });

  test('TC_SUP_043: 测试 Dayjs.add(1, \'month\') (触发月份调整)', () => {
    const result = index("add", "dayjs('2023-01-31')", [1, "month"]);
    expect(result).toBe("Dayjs object for 2023-02-28");
  });

  test('TC_SUP_044: 测试 Dayjs.add(2, \'year\')', () => {
    const result = index("add", "dayjs('2023-01-01')", [2, "year"]);
    expect(result).toBe("Dayjs object for 2025-01-01");
  });

  test('TC_SUP_045: 测试 Dayjs.add(5, \'day\')', () => {
    const result = index("add", "dayjs('2023-01-01')", [5, "day"]);
    expect(result).toBe("Dayjs object for 2023-01-06");
  });

  test('TC_SUP_046: 测试 Dayjs.add(1, \'week\')', () => {
    const result = index("add", "dayjs('2023-01-01')", [1, "week"]);
    expect(result).toBe("Dayjs object for 2023-01-08");
  });

  test('TC_SUP_047: 测试 Dayjs.add(30, \'minute\')', () => {
    const result = index("add", "dayjs('2023-01-01 10:00:00')", [30, "minute"]);
    expect(result).toBe("Dayjs object for 2023-01-01 10:30:00");
  });

  test('TC_SUP_048: 测试 Dayjs.add(1000, \'unknown\') (触发默认单位毫秒)', () => {
    const result = index("add", "dayjs('2023-01-01')", [1000, "unknown"]);
    expect(result).toBe("Dayjs object for 2023-01-01 00:00:01");
  });

  test('TC_SUP_049: 测试 Dayjs.subtract(2, \'day\')', () => {
    const result = index("subtract", "dayjs('2023-01-05')", [2, "day"]);
    expect(result).toBe("Dayjs object for 2023-01-03");
  });

  test('TC_SUP_050: 测试 Dayjs.format() (无效日期，无invalidDate locale)', () => {
    expect(() => { index("format", "dayjs(null)", []).format(); }).toThrow();
  });

  test('TC_SUP_051: 测试 Dayjs.format() (默认格式字符串)', () => {
    const result = index("format", "dayjs('2023-01-01')", []).format();
    expect(result).toBe("2023-01-01T00:00:00+XX:XX");
  });

  test('TC_SUP_052: 测试 Dayjs.format() (自定义格式字符串，覆盖大部分token)', () => {
    const result = index("format", "dayjs('2023-01-01 13:05:07.123')", ["YY YYYY M MM MMM MMMM D DD d dd ddd dddd H HH h hh a A m mm s ss SSS Z"]).format();
    expect(result).toBe("23 2023 1 01 Jan January 1 01 0 Su Sun Sunday 13 13 1 01 pm PM 5 05 7 07 123 +XX:XX");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_054: 测试 Dayjs.format() (meridiem的hour < 12)', () => {
    const result = index("format", "dayjs('2023-01-01 05:00:00')", ["a A"]).format();
    expect(result).toBe("am AM");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_056: 测试 Dayjs.format() (包含转义字符和未知token)', () => {
    const result = index("format", "dayjs('2023-01-01')", ["[ABC] [XYZ]"]).format();
    expect(result).toBe("ABC XYZ");
  });

  test('TC_SUP_057: 测试 Dayjs.utcOffset() 方法', () => {
    const result = index("utcOffset", "dayjs()").utcOffset();
    expect(result).toBe("number");
  });

  test('TC_SUP_058: 测试 Dayjs.diff(\'year\') (float为false)', () => {
    const result = index("diff", "dayjs('2024-01-01')", ["2023-01-01", "year"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_059: 测试 Dayjs.diff(\'month\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-03-01')", ["2023-01-01", "month"]);
    expect(result).toBe(2);
  });

  test('TC_SUP_060: 测试 Dayjs.diff(\'quarter\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-07-01')", ["2023-01-01", "quarter"]);
    expect(result).toBe(2);
  });

  test('TC_SUP_061: 测试 Dayjs.diff(\'week\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-01-08')", ["2023-01-01", "week"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_062: 测试 Dayjs.diff(\'day\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-01-02')", ["2023-01-01", "day"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_063: 测试 Dayjs.diff(\'hour\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-01-01 01:00:00')", ["2023-01-01 00:00:00", "hour"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_064: 测试 Dayjs.diff(\'minute\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-01-01 00:01:00')", ["2023-01-01 00:00:00", "minute"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_065: 测试 Dayjs.diff(\'second\') (float为false)', () => {
    const result = index("diff", "dayjs('2023-01-01 00:00:01')", ["2023-01-01 00:00:00", "second"]);
    expect(result).toBe(1);
  });

  test('TC_SUP_066: 测试 Dayjs.diff() (默认单位毫秒，float为false)', () => {
    const result = index("diff", "dayjs('2023-01-01 00:00:00.001')", ["2023-01-01 00:00:00.000"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_067: 测试 Dayjs.diff() (float为true)', () => {
    const result = index("diff", "dayjs('2023-01-01')", ["2022-12-15", "month", true]).diff();
    expect(result).toBe("number");
  });

  test('TC_SUP_068: 测试 Dayjs.daysInMonth() 方法', () => {
    const result = index("daysInMonth", "dayjs('2023-02-01')").daysInMonth();
    expect(result).toBe(28);
  });

  test('TC_SUP_069: 测试 Dayjs.$locale() 方法', () => {
    const result = index("$locale", "dayjs()");
    expect(result).toBe("en locale object");
  });

  test('TC_SUP_070: 测试 Dayjs.locale() (无参数，getter)', () => {
    const result = index("locale", "dayjs()", []).locale();
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_072: 测试 Dayjs.locale(\'unknown\') (setter，设置失败)', () => {
    const result = index("locale", "dayjs()", ["unknown"]);
    expect(result).toBe("Dayjs object with locale 'en'");
  });

  test('TC_SUP_073: 测试 Dayjs.clone() 方法', () => {
    const result = index("clone", "dayjs()").clone();
    expect(result).toBe("Dayjs object (clone)");
  });

  test('TC_SUP_074: 测试 Dayjs.toDate() 方法', () => {
    const result = index("toDate", "dayjs()").toDate();
    expect(result).toBe("Date object");
  });

  test('TC_SUP_075: 测试 Dayjs.toString() 方法', () => {
    const result = index("toString", "dayjs()").toString();
    expect(result).toBe("string");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_078: 测试 dayjs.unix() 方法', () => {
    const result = index("dayjs.unix", [1672531200]).unix();
    expect(result).toBe("Dayjs object for 2023-01-01 00:00:00.000 UTC");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_080: 测试 Dayjs.format() (h/hh token在12 AM/PM)', () => {
    const result = index("format", "dayjs('2023-01-01 00:00:00')", ["h hh"]).format();
    expect(result).toBe("12 12");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });
});
