/**
 * 自动生成的白盒测试用例 - index
 */
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('index 白盒测试', () => {
  test('TC001: isDayjs: Input is a Dayjs instance (mocked)', () => {
    const result = index({"$isDayjsObject": true, "clone": "mock_clone_function"});
    expect(result).toBe(true);
  });

  test('TC002: isDayjs: Input is an object without $isDayjsObject property', () => {
    const result = index({"someProp": "value"});
    expect(result).toBe(false);
  });

  test('TC003: isDayjs: Input is null', () => {
    const result = index(null);
    expect(result).toBe(false);
  });

  test('TC004: isDayjs: Input is undefined', () => {
    const result = index(null);
    expect(result).toBe(false);
  });

  test('TC005: parseLocale: preset is null, returns global L', () => {
    const result = index(null, null, false, "en", {"en": {"name": "en"}});
    expect(result).toBe("en");
  });

  test('TC006: parseLocale: preset is string, locale exists in Ls, not local, updates global L', () => {
    const result = index("es", null, false, "en", {"en": {"name": "en"}, "es": {"name": "es"}});
    expect(result).toBe("es");
  });

  test('TC007: parseLocale: preset is string, object provided, adds new locale, updates global L', () => {
    const result = index("fr", {"name": "fr"}, false, "en", {"en": {"name": "en"}});
    expect(result).toBe("fr");
  });

  test('TC008: parseLocale: preset is string \'zh-cn\', recursive call finds \'zh\', updates global L', () => {
    const result = index("zh-cn", null, false, "en", {"en": {"name": "en"}, "zh": {"name": "zh"}});
    expect(result).toBe("zh");
  });

  test('TC009: parseLocale: preset is string \'zh-cn\', recursive call to \'zh\' fails, returns global L', () => {
    const result = index("zh-cn", null, false, "en", {"en": {"name": "en"}});
    expect(result).toBe("en");
  });

  test('TC010: parseLocale: preset is an object, adds new locale, updates global L', () => {
    const result = index({"name": "de"}, null, false, "en", {"en": {"name": "en"}});
    expect(result).toBe("de");
  });

  test('TC011: parseLocale: preset is string, locale exists, isLocal is true (global L should not change)', () => {
    const result = index("es", null, true, "en", {"en": {"name": "en"}, "es": {"name": "es"}});
    expect(result).toBe("es");
  });

  test('TC012: parseLocale: preset is string, locale does not exist, no object, no hyphen, returns global L', () => {
    const result = index("xx", null, false, "en", {"en": {"name": "en"}});
    expect(result).toBe("en");
  });

  test('TC013: parseDate: date is null', () => {
    expect(() => { index({"date": null}); }).toThrow();
  });

  test('TC014: parseDate: date is undefined (Utils.u returns true)', () => {
    const result = index({"date": null});
    expect(result).toBe("Current Date");
  });

  test('TC015: parseDate: date is an instance of Date', () => {
    const result = index({"date": "new Date('2023-01-15T10:00:00.000Z')"});
    expect(result).toBe("2023-01-15T10:00:00.000Z");
  });

  test('TC016: parseDate: date is a string matching REGEX_PARSE, non-UTC', () => {
    const result = index({"date": "2023-01-15 10:30:45.123", "utc": false});
    expect(result).toBe("2023-01-15T10:30:45.123 Local Time");
  });

  test('TC017: parseDate: date is a string matching REGEX_PARSE, UTC', () => {
    const result = index({"date": "2023-01-15 10:30:45.123", "utc": true});
    expect(result).toBe("2023-01-15T10:30:45.123Z UTC Time");
  });

  test('TC018: parseDate: date is a string not matching REGEX_PARSE, no \'Z\'', () => {
    expect(() => { index({"date": "invalid date string", "utc": false}); }).toThrow();
  });

  test('TC019: parseDate: date is a string with \'Z\' (ISO format), falls through to new Date(date)', () => {
    const result = index({"date": "2023-01-15T10:30:45.123Z", "utc": false});
    expect(result).toBe("2023-01-15T10:30:45.123Z");
  });

  test('TC020: parseDate: date is a number (timestamp)', () => {
    const result = index({"date": 1673778645123, "utc": false});
    expect(result).toBe("Date from timestamp");
  });

  test('TC021: dayjs: date is a Dayjs instance, should clone', () => {
    const result = index({"$isDayjsObject": true, "clone": "mock_clone_function"}, {});
    expect(result).toBe("cloned Dayjs instance");
  });

  test('TC022: dayjs: date is not Dayjs, c is an object', () => {
    const result = index("new Date()", {"locale": "fr"});
    expect(result).toBe("Dayjs instance with locale 'fr'");
  });

  test('TC023: dayjs: date is not Dayjs, c is not an object', () => {
    const result = index("2023-01-15", "some string");
    expect(result).toBe("Dayjs instance with default config");
  });

  test('TC024: Dayjs constructor: with locale and x', () => {
    const result = index({"locale": "es", "x": {"pluginData": true}, "date": "2023-01-15"}, {"en": {"name": "en"}, "es": {"name": "es"}});
    expect(result).toBe("{'$L': 'es', '$x': {'pluginData': True}, '$isDayjsObject': True, '$d': '2023-01-15T00:00:00.000 Local Time'}");
  });

  test('TC025: Dayjs constructor: no locale, no x', () => {
    const result = index({"date": "2023-01-15"}, {"en": {"name": "en"}});
    expect(result).toBe("{'$L': 'en', '$x': {}, '$isDayjsObject': True, '$d': '2023-01-15T00:00:00.000 Local Time'}");
  });

  test('TC026: Dayjs.isValid: valid date', () => {
    const result = index("2023-01-15");
    expect(result).toBe(true);
  });

  test('TC027: Dayjs.isValid: invalid date', () => {
    const result = index(null);
    expect(result).toBe(false);
  });

  test('TC028: Dayjs.isSame: same year', () => {
    const result = index("2023-01-15", "2023-06-20", "year");
    expect(result).toBe(true);
  });

  test('TC029: Dayjs.isSame: different year', () => {
    const result = index("2023-01-15", "2024-06-20", "year");
    expect(result).toBe(false);
  });

  test('TC030: Dayjs.isAfter: instance is after that', () => {
    const result = index("2023-01-15", "2023-01-14", "day");
    expect(result).toBe(true);
  });

  test('TC031: Dayjs.isAfter: instance is not after that', () => {
    const result = index("2023-01-15", "2023-01-16", "day");
    expect(result).toBe(false);
  });

  test('TC032: Dayjs.isBefore: instance is before that', () => {
    const result = index("2023-01-15", "2023-01-16", "day");
    expect(result).toBe(true);
  });

  test('TC033: Dayjs.isBefore: instance is not before that', () => {
    const result = index("2023-01-15", "2023-01-14", "day");
    expect(result).toBe(false);
  });

  test('TC034: Dayjs.$g: input is undefined, should return getter value', () => {
    const result = index("2023-01-15", null, "$y", "year");
    expect(result).toBe(2023);
  });

  test('TC035: Dayjs.$g: input is defined, should call set', () => {
    const result = index("2023-01-15", 2024, "$y", "year");
    expect(result).toBe("Dayjs instance with year 2024");
  });

  test('TC036: Dayjs.startOf: unit \'year\', isStartOf true, non-UTC', () => {
    const result = index("2023-06-15T10:30:00.000", "year", true);
    expect(result).toBe("2023-01-01T00:00:00.000 Local Time");
  });

  test('TC037: Dayjs.startOf: unit \'year\', isStartOf false (endOf year), non-UTC', () => {
    const result = index("2023-06-15T10:30:00.000", "year", false);
    expect(result).toBe("2023-12-31T23:59:59.999 Local Time");
  });

  test('TC038: Dayjs.startOf: unit \'month\', isStartOf true, UTC', () => {
    const result = index("2023-06-15T10:30:00.000", true, "month", true);
    expect(result).toBe("2023-06-01T00:00:00.000Z UTC Time");
  });

  test('TC039: Dayjs.startOf: unit \'month\', isStartOf false (endOf month), UTC', () => {
    const result = index("2023-06-15T10:30:00.000", true, "month", false);
    expect(result).toBe("2023-06-30T23:59:59.999Z UTC Time");
  });

  test('TC040: Dayjs.startOf: unit \'week\', isStartOf true, weekStart 0 (Sunday)', () => {
    const result = index("2023-01-18", "week", true, 0);
    expect(result).toBe("2023-01-15T00:00:00.000 Local Time");
  });

  test('TC041: Dayjs.startOf: unit \'week\', isStartOf true, weekStart 1 (Monday), $W < weekStart', () => {
    const result = index("2023-01-15", "week", true, 1);
    expect(result).toBe("2023-01-09T00:00:00.000 Local Time");
  });

  test('TC042: Dayjs.startOf: unit \'day\', isStartOf true, non-UTC', () => {
    const result = index("2023-01-15T10:30:45.123", "day", true);
    expect(result).toBe("2023-01-15T00:00:00.000 Local Time");
  });

  test('TC043: Dayjs.startOf: unit \'hour\', isStartOf true, UTC', () => {
    const result = index("2023-01-15T10:30:45.123", true, "hour", true);
    expect(result).toBe("2023-01-15T10:00:00.000Z UTC Time");
  });

  test('TC044: Dayjs.startOf: unit \'minute\', isStartOf true, non-UTC', () => {
    const result = index("2023-01-15T10:30:45.123", "minute", true);
    expect(result).toBe("2023-01-15T10:30:00.000 Local Time");
  });

  test('TC045: Dayjs.startOf: unit \'second\', isStartOf true, non-UTC', () => {
    const result = index("2023-01-15T10:30:45.123", "second", true);
    expect(result).toBe("2023-01-15T10:30:45.000 Local Time");
  });

  test('TC046: Dayjs.startOf: unknown unit, should clone', () => {
    const result = index("2023-01-15", "unknown", true);
    expect(result).toBe("2023-01-15T00:00:00.000 Local Time");
  });

  test('TC047: Dayjs.endOf: unit \'day\'', () => {
    const result = index("2023-01-15T10:30:45.123", "day");
    expect(result).toBe("2023-01-15T23:59:59.999 Local Time");
  });

  test('TC048: Dayjs.$set: unit \'year\', non-UTC', () => {
    const result = index("2023-01-15", "year", 2024);
    expect(result).toBe("2024-01-15T00:00:00.000 Local Time");
  });

  test('TC049: Dayjs.$set: unit \'month\', non-UTC, target month has fewer days', () => {
    const result = index("2023-03-31", "month", 1);
    expect(result).toBe("2023-02-28T00:00:00.000 Local Time");
  });

  test('TC050: Dayjs.$set: unit \'day\' (day of week), non-UTC, set to next Friday', () => {
    const result = index("2023-01-15", "day", 5);
    expect(result).toBe("2023-01-20T00:00:00.000 Local Time");
  });

  test('TC051: Dayjs.$set: unit \'hour\', UTC', () => {
    const result = index("2023-01-15T10:30:00.000", true, "hour", 15);
    expect(result).toBe("2023-01-15T15:30:00.000Z UTC Time");
  });

  test('TC052: Dayjs.$set: unit \'millisecond\', non-UTC', () => {
    const result = index("2023-01-15T10:30:45.123", "millisecond", 500);
    expect(result).toBe("2023-01-15T10:30:45.500 Local Time");
  });

  test('TC053: Dayjs.$set: unknown unit, should not modify date', () => {
    const result = index("2023-01-15", "unknown", 100);
    expect(result).toBe("2023-01-15T00:00:00.000 Local Time");
  });

  test('TC054: Dayjs.set: calls $set on a clone', () => {
    const result = index("2023-01-15", "year", 2024);
    expect(result).toBe("2024-01-15T00:00:00.000 Local Time");
  });

  test('TC055: Dayjs.get: unit \'year\'', () => {
    const result = index("2023-01-15", "year");
    expect(result).toBe(2023);
  });

  test('TC056: Dayjs.add: unit \'month\'', () => {
    const result = index("2023-01-15", 2, "month");
    expect(result).toBe("2023-03-15T00:00:00.000 Local Time");
  });

  test('TC057: Dayjs.add: unit \'year\'', () => {
    const result = index("2023-01-15", 1, "year");
    expect(result).toBe("2024-01-15T00:00:00.000 Local Time");
  });

  test('TC058: Dayjs.add: unit \'day\'', () => {
    const result = index("2023-01-15", 5, "day");
    expect(result).toBe("2023-01-20T00:00:00.000 Local Time");
  });

  test('TC059: Dayjs.add: unit \'week\'', () => {
    const result = index("2023-01-15", 1, "week");
    expect(result).toBe("2023-01-22T00:00:00.000 Local Time");
  });

  test('TC060: Dayjs.add: unit \'hour\'', () => {
    const result = index("2023-01-15T10:00:00.000", 2, "hour");
    expect(result).toBe("2023-01-15T12:00:00.000 Local Time");
  });

  test('TC061: Dayjs.add: unit \'millisecond\'', () => {
    const result = index("2023-01-15T10:00:00.000", 500, "millisecond");
    expect(result).toBe("2023-01-15T10:00:00.500 Local Time");
  });

  test('TC062: Dayjs.add: unknown unit, defaults to milliseconds', () => {
    const result = index("2023-01-15T10:00:00.000", 100, "unknown");
    expect(result).toBe("2023-01-15T10:00:00.100 Local Time");
  });

  test('TC063: Dayjs.subtract: unit \'day\'', () => {
    const result = index("2023-01-15", 5, "day");
    expect(result).toBe("2023-01-10T00:00:00.000 Local Time");
  });

  test('TC064: Dayjs.format: invalid date, no locale invalidDate', () => {
    expect(() => { index(null, "YYYY-MM-DD", null); }).toThrow();
  });

  test('TC065: Dayjs.format: invalid date, with locale invalidDate', () => {
    const result = index(null, "YYYY-MM-DD", "Fecha inválida");
    expect(result).toBe("Fecha inválida");
  });

  test('TC066: Dayjs.format: default format string', () => {
    const result = index("2023-01-15T10:30:45.123", null);
    expect(result).toBe("2023-01-15T10:30:45+XX:XX");
  });

  test('TC067: Dayjs.format: all format tokens (YYYY, MM, DD, HH, mm, ss, SSS, Z, a, A, d, dd, ddd, dddd, M, MMM, MMMM, h, hh)', () => {
    const result = index("2023-01-15T10:30:05.007", "YYYY-MM-DD HH:mm:ss.SSS Z a A d dd ddd dddd M MMM MMMM h hh");
    expect(result).toBe("2023-01-15 10:30:05.007 +XX:XX am AM 0 Su Sun Sunday 1 Jan January 10 10");
  });

  test('TC068: Dayjs.format: locale with custom meridiem function', () => {
    const result = index("2023-01-15T14:30:00.000", "h A", "(h, m, lower) => lower ? (h < 12 ? 'ante' : 'post') : (h < 12 ? 'ANTE' : 'POST')");
    expect(result).toBe("02 POST");
  });

  test('TC069: Dayjs.format: escaped characters', () => {
    const result = index("2023-01-15", "[The year is] YYYY");
    expect(result).toBe("The year is 2023");
  });

  test('TC070: Dayjs.format: getShort with locale array as function (months)', () => {
    const result = index("2023-01-15", "MMMM", {"en": {"name": "en"}, "custom": {"name": "custom", "months": "mock_months_function_jan"}});
    expect(result).toBe("CustomJan");
  });

  test('TC071: Dayjs.format: getShort with locale array as function (months, other month)', () => {
    const result = index("2023-02-15", "MMMM", {"en": {"name": "en"}, "custom": {"name": "custom", "months": "mock_months_function_feb"}});
    expect(result).toBe("CustomMonth");
  });

  test('TC072: Dayjs.diff: unit \'year\', float true', () => {
    const result = index("2024-01-15", "2023-01-15", "year", true);
    expect(result).toBe(1.0);
  });

  test('TC073: Dayjs.diff: unit \'month\', float false', () => {
    const result = index("2023-03-15", "2023-01-15", "month", false);
    expect(result).toBe(2);
  });

  test('TC074: Dayjs.diff: unit \'quarter\', float true', () => {
    const result = index("2023-07-15", "2023-01-15", "quarter", true);
    expect(result).toBe(2.0);
  });

  test('TC075: Dayjs.diff: unit \'week\', float false, with timezone difference', () => {
    const result = index("2023-01-15T12:00:00.000", "2023-01-08T12:00:00.000", "week", false, 0, 60);
    expect(result).toBe(1);
  });

  test('TC076: Dayjs.diff: unit \'day\', float true', () => {
    const result = index("2023-01-15", "2023-01-14", "day", true);
    expect(result).toBe(1.0);
  });

  test('TC077: Dayjs.diff: unit \'hour\', float false', () => {
    const result = index("2023-01-15T12:00:00.000", "2023-01-15T10:00:00.000", "hour", false);
    expect(result).toBe(2);
  });

  test('TC078: Dayjs.diff: unit \'minute\', float true', () => {
    const result = index("2023-01-15T10:30:00.000", "2023-01-15T10:00:00.000", "minute", true);
    expect(result).toBe(30.0);
  });

  test('TC079: Dayjs.diff: unit \'second\', float false', () => {
    const result = index("2023-01-15T10:00:30.000", "2023-01-15T10:00:00.000", "second", false);
    expect(result).toBe(30);
  });

  test('TC080: Dayjs.diff: default unit (milliseconds), float true', () => {
    const result = index("2023-01-15T10:00:00.500", "2023-01-15T10:00:00.000", "unknown", true);
    expect(result).toBe(500.0);
  });

  test('TC081: Dayjs.daysInMonth: January', () => {
    const result = index("2023-01-15");
    expect(result).toBe(31);
  });

  test('TC082: Dayjs.daysInMonth: February (non-leap year)', () => {
    const result = index("2023-02-15");
    expect(result).toBe(28);
  });

  test('TC083: Dayjs.daysInMonth: February (leap year)', () => {
    const result = index("2024-02-15");
    expect(result).toBe(29);
  });

  test('TC084: Dayjs.locale: no preset, returns current locale name', () => {
    const result = index("2023-01-15", "es", null, null);
    expect(result).toBe("es");
  });

  test('TC085: Dayjs.locale: preset string, object provided, sets new locale on clone', () => {
    const result = index("2023-01-15", "en", "fr", {"name": "fr"}, {"en": {"name": "en"}});
    expect(result).toBe("{'$L': 'fr', '$d': '2023-01-15T00:00:00.000 Local Time'}");
  });

  test('TC086: Dayjs.locale: preset string, locale exists, switches locale on clone', () => {
    const result = index("2023-01-15", "en", "es", null, {"en": {"name": "en"}, "es": {"name": "es"}});
    expect(result).toBe("{'$L': 'es', '$d': '2023-01-15T00:00:00.000 Local Time'}");
  });

  test('TC087: Dayjs.locale: preset string, locale not found, returns clone with original locale', () => {
    const result = index("2023-01-15", "en", "xx", null, {"en": {"name": "en"}});
    expect(result).toBe("{'$L': 'en', '$d': '2023-01-15T00:00:00.000 Local Time'}");
  });

  test('TC088: Dayjs.toJSON: valid date', () => {
    const result = index("2023-01-15T10:00:00.000Z");
    expect(result).toBe("2023-01-15T10:00:00.000Z");
  });

  test('TC089: Dayjs.toJSON: invalid date', () => {
    const result = index(null);
    expect(result).toBe(null);
  });

  test('TC090: Dayjs.extend: plugin not installed', () => {
    const result = index("mock_plugin_function_not_installed", {"key": "value"});
    expect(result).toBe("dayjs function");
  });

  test('TC091: Dayjs.extend: plugin already installed', () => {
    const result = index({"$i": true, "func": "mock_plugin_function_installed"}, {"key": "value"});
    expect(result).toBe("dayjs function");
  });

  test('TC092: dayjs.unix: converts timestamp to Dayjs instance', () => {
    const result = index(1673778645);
    expect(result).toBe("2023-01-15T10:30:45.000 Local Time");
  });

  test('TC093: Dayjs.prototype.ms: get milliseconds', () => {
    const result = index("2023-01-15T10:30:45.123", null);
    expect(result).toBe(123);
  });

  test('TC094: Dayjs.prototype.ms: set milliseconds', () => {
    const result = index("2023-01-15T10:30:45.123", 500);
    expect(result).toBe("2023-01-15T10:30:45.500 Local Time");
  });

  test('TC095: Dayjs.prototype.day: get day of week (Sunday)', () => {
    const result = index("2023-01-15", null);
    expect(result).toBe(0);
  });

  test('TC096: Dayjs.prototype.day: set day of week (C.D unit in proto mapping) to Friday', () => {
    const result = index("2023-01-15", 5);
    expect(result).toBe("2023-01-20T00:00:00.000 Local Time");
  });

  test('TC097: Dayjs.prototype.date: get day of month', () => {
    const result = index("2023-01-15", null);
    expect(result).toBe(15);
  });

  test('TC098: Dayjs.prototype.date: set day of month', () => {
    const result = index("2023-01-15", 20);
    expect(result).toBe("2023-01-20T00:00:00.000 Local Time");
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

  test('TC_SUP_014: 测试 Dayjs.$utils() 方法，覆盖 L112', () => {
    const result = index("$utils", "dayjs('2023-01-15')");
    expect(result).toBe("Utils_object");
  });

  test('TC_SUP_015: 测试 Dayjs.isSame() 方法：日期相同，覆盖 L120, L121 binary-expr branch-0, branch-1', () => {
    const result = index("isSame", "dayjs('2023-01-15')", ["2023-01-15", "day"]).isSame();
    expect(result).toBe(true);
  });

  test('TC_SUP_016: 测试 Dayjs.isAfter() 方法：日期在后，覆盖 L125', () => {
    const result = index("isAfter", "dayjs('2023-01-16')", ["2023-01-15", "day"]).isAfter();
    expect(result).toBe(true);
  });

  test('TC_SUP_017: 测试 Dayjs.isBefore() 方法：日期在前，覆盖 L129', () => {
    const result = index("isBefore", "dayjs('2023-01-15')", ["2023-01-16", "day"]).isBefore();
    expect(result).toBe(true);
  });

  test('TC_SUP_019: 测试 Dayjs.$g() 方法：input 为有效值，覆盖 L133 if branch-1, L134', () => {
    const result = index("$g", "dayjs('2023-01-15')", [2024, "$y", "year"]);
    expect(result).toBe("2024-01-15T00:00:00.000Z");
  });

  test('TC_SUP_020: 测试 Dayjs.unix() 方法，覆盖 L138', () => {
    const result = index("unix", "dayjs('2023-01-01T00:00:00.000Z')").unix();
    expect(result).toBe(1672531200);
  });

  test('TC_SUP_021: 测试 Dayjs.valueOf() 方法，覆盖 L143', () => {
    const result = index("valueOf", "dayjs('2023-01-01T00:00:00.000Z')").valueOf();
    expect(result).toBe(1672531200000);
  });

  test('TC_SUP_022: 测试 Dayjs.startOf() 方法：不传 startOf 参数，覆盖 L147 cond-expr branch-0, L148, L149, L150 cond-expr branch-0, L152 cond-expr branch-0, L154, L155, L156, L157, L162, L163 cond-expr branch-0, L164 switch branch for C.D, L178, L159 cond-expr branch-0', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45')", ["day"]).startOf();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_023: 测试 Dayjs.startOf() 方法：传 startOf 参数为 true，覆盖 L147 cond-expr branch-1', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45')", ["day", true]).startOf();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_024: 测试 Dayjs.startOf() 方法：单位为 \'year\'，覆盖 L164 switch branch-0, L166 cond-expr branch-0', () => {
    const result = index("startOf", "dayjs('2023-01-15')", ["year"]).startOf();
    expect(result).toBe("2023-01-01T00:00:00.000");
  });

  test('TC_SUP_025: 测试 Dayjs.endOf() 方法：单位为 \'year\'，覆盖 L166 cond-expr branch-1, L152 cond-expr branch-1', () => {
    const result = index("endOf", "dayjs('2023-01-15')", ["year"]).endOf();
    expect(result).toBe("2023-12-31T23:59:59.999");
  });

  test('TC_SUP_026: 测试 Dayjs.startOf() 方法：单位为 \'month\'，覆盖 L164 switch branch-1, L169 cond-expr branch-0', () => {
    const result = index("startOf", "dayjs('2023-01-15')", ["month"]).startOf();
    expect(result).toBe("2023-01-01T00:00:00.000");
  });

  test('TC_SUP_027: 测试 Dayjs.endOf() 方法：单位为 \'month\'，覆盖 L169 cond-expr branch-1', () => {
    const result = index("endOf", "dayjs('2023-01-15')", ["month"]).endOf();
    expect(result).toBe("2023-01-31T23:59:59.999");
  });

  test('TC_SUP_028: 测试 Dayjs.startOf() 方法：单位为 \'week\' (默认 weekStart=0)，当前日期为周日，覆盖 L164 switch branch-2, L172 binary-expr branch-1, L173 cond-expr branch-1, L174 cond-expr branch-0', () => {
    const result = index("startOf", "dayjs('2023-01-15')", ["week"]).startOf();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_030: 测试 Dayjs.endOf() 方法：单位为 \'week\'，覆盖 L174 cond-expr branch-1', () => {
    const result = index("endOf", "dayjs('2023-01-18')", ["week"]).endOf();
    expect(result).toBe("2023-01-21T23:59:59.999");
  });

  test('TC_SUP_031: 测试 Dayjs.startOf() 方法：单位为 \'hour\'，覆盖 L164 switch branch-4, L180', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45')", ["hour"]).startOf();
    expect(result).toBe("2023-01-15T10:00:00.000");
  });

  test('TC_SUP_032: 测试 Dayjs.startOf() 方法：单位为 \'minute\'，覆盖 L164 switch branch-5, L182', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45')", ["minute"]).startOf();
    expect(result).toBe("2023-01-15T10:30:00.000");
  });

  test('TC_SUP_033: 测试 Dayjs.startOf() 方法：单位为 \'second\'，覆盖 L164 switch branch-6, L184', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45.123')", ["second"]).startOf();
    expect(result).toBe("2023-01-15T10:30:45.000");
  });

  test('TC_SUP_034: 测试 Dayjs.startOf() 方法：单位为未知，覆盖 L164 switch branch-8, L186', () => {
    const result = index("startOf", "dayjs('2023-01-15')", ["unknown"]).startOf();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_035: 测试 Dayjs.startOf() 方法：UTC 实例，覆盖 L150 cond-expr branch-1, L163 cond-expr branch-1', () => {
    const result = index("startOf", "dayjs('2023-01-15 10:30:45').utc(true)", ["day"]).startOf();
    expect(result).toBe("2023-01-15T00:00:00.000Z");
  });

  test('TC_SUP_036: 测试 Dayjs.$set() 方法：设置 \'day\'，覆盖 L195, L196 cond-expr branch-0, L197, L207 cond-expr branch-0, L215 if branch-0, L217, L218', () => {
    const result = index("$set", "dayjs('2023-01-15')", ["day", 3]);
    expect(result).toBe("2023-01-18T00:00:00.000");
  });

  test('TC_SUP_037: 测试 Dayjs.$set() 方法：设置 \'month\'，覆盖 L207 cond-expr branch-1, L209 if branch-0, L209 binary-expr branch-0, L211, L212, L213, L214', () => {
    const result = index("$set", "dayjs('2023-01-31')", ["month", 1]);
    expect(result).toBe("2023-02-28T00:00:00.000");
  });

  test('TC_SUP_038: 测试 Dayjs.$set() 方法：设置 \'year\'，覆盖 L209 binary-expr branch-1', () => {
    const result = index("$set", "dayjs('2023-01-15')", ["year", 2024]);
    expect(result).toBe("2024-01-15T00:00:00.000");
  });

  test('TC_SUP_039: 测试 Dayjs.$set() 方法：设置 \'hour\'，覆盖 L209 if branch-1', () => {
    const result = index("$set", "dayjs('2023-01-15 10:00:00')", ["hour", 15]);
    expect(result).toBe("2023-01-15T15:00:00.000");
  });

  test('TC_SUP_040: 测试 Dayjs.$set() 方法：UTC 实例，覆盖 L196 cond-expr branch-1', () => {
    const result = index("$set", "dayjs('2023-01-15 10:00:00').utc(true)", ["hour", 15]);
    expect(result).toBe("2023-01-15T15:00:00.000Z");
  });

  test('TC_SUP_041: 测试 Dayjs.$set() 方法：无效单位，覆盖 L215 if branch-1', () => {
    const result = index("$set", "dayjs('2023-01-15')", ["invalid", 1]);
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_042: 测试 Dayjs.set() 方法，覆盖 L222', () => {
    const result = index("set", "dayjs('2023-01-15')", ["year", 2024]).set();
    expect(result).toBe("2024-01-15T00:00:00.000");
  });

  test('TC_SUP_043: 测试 Dayjs.get() 方法，覆盖 L226', () => {
    const result = index("get", "dayjs('2023-01-15')", ["year"]).get();
    expect(result).toBe(2023);
  });

  test('TC_SUP_044: 测试 Dayjs.add() 方法：添加 \'month\'，覆盖 L230, L231, L236 if branch-0, L237', () => {
    const result = index("add", "dayjs('2023-01-15')", [1, "month"]).add();
    expect(result).toBe("2023-02-15T00:00:00.000");
  });

  test('TC_SUP_045: 测试 Dayjs.add() 方法：添加 \'year\'，覆盖 L236 if branch-1, L239 if branch-0, L240', () => {
    const result = index("add", "dayjs('2023-01-15')", [1, "year"]).add();
    expect(result).toBe("2024-01-15T00:00:00.000");
  });

  test('TC_SUP_046: 测试 Dayjs.add() 方法：添加 \'day\'，覆盖 L239 if branch-1, L242 if branch-0, L243, L232, L233, L234', () => {
    const result = index("add", "dayjs('2023-01-15')", [1, "day"]).add();
    expect(result).toBe("2023-01-16T00:00:00.000");
  });

  test('TC_SUP_047: 测试 Dayjs.add() 方法：添加 \'week\'，覆盖 L242 if branch-1, L245 if branch-0, L246', () => {
    const result = index("add", "dayjs('2023-01-15')", [1, "week"]).add();
    expect(result).toBe("2023-01-22T00:00:00.000");
  });

  test('TC_SUP_048: 测试 Dayjs.add() 方法：添加 \'hour\'，覆盖 L245 if branch-1, L248 binary-expr branch-0, L254, L255', () => {
    const result = index("add", "dayjs('2023-01-15 10:00:00')", [1, "hour"]).add();
    expect(result).toBe("2023-01-15T11:00:00.000");
  });

  test('TC_SUP_049: 测试 Dayjs.add() 方法：添加 \'minute\'', () => {
    const result = index("add", "dayjs('2023-01-15 10:00:00')", [1, "minute"]).add();
    expect(result).toBe("2023-01-15T10:01:00.000");
  });

  test('TC_SUP_050: 测试 Dayjs.add() 方法：添加 \'second\'', () => {
    const result = index("add", "dayjs('2023-01-15 10:00:00')", [1, "second"]).add();
    expect(result).toBe("2023-01-15T10:00:01.000");
  });

  test('TC_SUP_051: 测试 Dayjs.add() 方法：添加 \'millisecond\' (默认 step)，覆盖 L248 binary-expr branch-1', () => {
    const result = index("add", "dayjs('2023-01-15 10:00:00.000')", [1, "millisecond"]).add();
    expect(result).toBe("2023-01-15T10:00:00.001");
  });

  test('TC_SUP_052: 测试 Dayjs.subtract() 方法，覆盖 L259', () => {
    const result = index("subtract", "dayjs('2023-01-15')", [1, "day"]).subtract();
    expect(result).toBe("2023-01-14T00:00:00.000");
  });

  test('TC_SUP_053: 测试 Dayjs.format() 方法：无效日期，覆盖 L263, L265 if branch-0, L265 binary-expr branch-1', () => {
    expect(() => { index("format", "dayjs(null)", []).format(); }).toThrow();
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_055: 测试 Dayjs.format() 方法：无 formatStr 参数 (默认格式)，覆盖 L267 binary-expr branch-1, L268, L269, L272, L280 binary-expr branch-1, L281 cond-expr branch-0, L282 cond-expr branch-0, L285, L286 switch branches for default tokens', () => {
    const result = index("format", "dayjs('2023-01-15 10:30:45.123')", []).format();
    expect(result).toBe("2023-01-15T10:30:45-05:00");
  });

  test('TC_SUP_056: 测试 Dayjs.format() 方法：格式化 \'YY\'，覆盖 L286 switch branch-0, L288', () => {
    const result = index("format", "dayjs('2023-01-15')", ["YY"]).format();
    expect(result).toBe("23");
  });

  test('TC_SUP_057: 测试 Dayjs.format() 方法：格式化 \'YYYY\'，覆盖 L286 switch branch-1, L290, L267 binary-expr branch-0', () => {
    const result = index("format", "dayjs('2023-01-15')", ["YYYY"]).format();
    expect(result).toBe("2023");
  });

  test('TC_SUP_058: 测试 Dayjs.format() 方法：格式化 \'M\'，覆盖 L286 switch branch-2, L292', () => {
    const result = index("format", "dayjs('2023-01-15')", ["M"]).format();
    expect(result).toBe("1");
  });

  test('TC_SUP_059: 测试 Dayjs.format() 方法：格式化 \'MM\'，覆盖 L286 switch branch-3, L294', () => {
    const result = index("format", "dayjs('2023-01-05')", ["MM"]).format();
    expect(result).toBe("01");
  });

  test('TC_SUP_060: 测试 Dayjs.format() 方法：格式化 \'MMM\' (默认 locale)，覆盖 L286 switch branch-4, L296, L273, L274 binary-expr branch-0, branch-2', () => {
    const result = index("format", "dayjs('2023-01-15')", ["MMM"]).format();
    expect(result).toBe("Jan");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_062: 测试 Dayjs.format() 方法：格式化 \'MMMM\'，覆盖 L286 switch branch-5, L298, L274 binary-expr branch-1', () => {
    const result = index("format", "dayjs('2023-01-15')", ["MMMM"]).format();
    expect(result).toBe("January");
  });

  test('TC_SUP_063: 测试 Dayjs.format() 方法：格式化 \'D\'，覆盖 L286 switch branch-6, L300', () => {
    const result = index("format", "dayjs('2023-01-05')", ["D"]).format();
    expect(result).toBe("5");
  });

  test('TC_SUP_064: 测试 Dayjs.format() 方法：格式化 \'DD\'，覆盖 L286 switch branch-7, L302', () => {
    const result = index("format", "dayjs('2023-01-05')", ["DD"]).format();
    expect(result).toBe("05");
  });

  test('TC_SUP_065: 测试 Dayjs.format() 方法：格式化 \'d\'，覆盖 L286 switch branch-8, L304', () => {
    const result = index("format", "dayjs('2023-01-15')", ["d"]).format();
    expect(result).toBe("0");
  });

  test('TC_SUP_066: 测试 Dayjs.format() 方法：格式化 \'dd\'，覆盖 L286 switch branch-9, L306', () => {
    const result = index("format", "dayjs('2023-01-15')", ["dd"]).format();
    expect(result).toBe("Su");
  });

  test('TC_SUP_067: 测试 Dayjs.format() 方法：格式化 \'ddd\'，覆盖 L286 switch branch-10, L308', () => {
    const result = index("format", "dayjs('2023-01-15')", ["ddd"]).format();
    expect(result).toBe("Sun");
  });

  test('TC_SUP_068: 测试 Dayjs.format() 方法：格式化 \'dddd\'，覆盖 L286 switch branch-11, L310', () => {
    const result = index("format", "dayjs('2023-01-15')", ["dddd"]).format();
    expect(result).toBe("Sunday");
  });

  test('TC_SUP_069: 测试 Dayjs.format() 方法：格式化 \'H\'，覆盖 L286 switch branch-12, L312', () => {
    const result = index("format", "dayjs('2023-01-15 13:00:00')", ["H"]).format();
    expect(result).toBe("13");
  });

  test('TC_SUP_070: 测试 Dayjs.format() 方法：格式化 \'HH\'，覆盖 L286 switch branch-13, L314', () => {
    const result = index("format", "dayjs('2023-01-15 03:00:00')", ["HH"]).format();
    expect(result).toBe("03");
  });

  test('TC_SUP_071: 测试 Dayjs.format() 方法：格式化 \'h\' (1 PM)，覆盖 L286 switch branch-14, L316, L277 binary-expr branch-0', () => {
    const result = index("format", "dayjs('2023-01-15 13:00:00')", ["h"]).format();
    expect(result).toBe("1");
  });

  test('TC_SUP_072: 测试 Dayjs.format() 方法：格式化 \'h\' (12 PM)，覆盖 L277 binary-expr branch-1', () => {
    const result = index("format", "dayjs('2023-01-15 12:00:00')", ["h"]).format();
    expect(result).toBe("12");
  });

  test('TC_SUP_073: 测试 Dayjs.format() 方法：格式化 \'hh\'，覆盖 L286 switch branch-15, L318', () => {
    const result = index("format", "dayjs('2023-01-15 01:00:00')", ["hh"]).format();
    expect(result).toBe("01");
  });

  test('TC_SUP_074: 测试 Dayjs.format() 方法：格式化 \'a\' (10 AM)，覆盖 L286 switch branch-16, L320, L281 cond-expr branch-0, L282 cond-expr branch-0', () => {
    const result = index("format", "dayjs('2023-01-15 10:00:00')", ["a"]).format();
    expect(result).toBe("am");
  });

  test('TC_SUP_075: 测试 Dayjs.format() 方法：格式化 \'A\' (1 PM)，覆盖 L286 switch branch-17, L322, L281 cond-expr branch-1, L282 cond-expr branch-1', () => {
    const result = index("format", "dayjs('2023-01-15 13:00:00')", ["A"]).format();
    expect(result).toBe("PM");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_077: 测试 Dayjs.format() 方法：格式化 \'m\'，覆盖 L286 switch branch-18, L324', () => {
    const result = index("format", "dayjs('2023-01-15 10:05:00')", ["m"]).format();
    expect(result).toBe("5");
  });

  test('TC_SUP_078: 测试 Dayjs.format() 方法：格式化 \'mm\'，覆盖 L286 switch branch-19, L326', () => {
    const result = index("format", "dayjs('2023-01-15 10:05:00')", ["mm"]).format();
    expect(result).toBe("05");
  });

  test('TC_SUP_079: 测试 Dayjs.format() 方法：格式化 \'s\'，覆盖 L286 switch branch-20, L328', () => {
    const result = index("format", "dayjs('2023-01-15 10:00:05')", ["s"]).format();
    expect(result).toBe("5");
  });

  test('TC_SUP_080: 测试 Dayjs.format() 方法：格式化 \'ss\'，覆盖 L286 switch branch-21, L330', () => {
    const result = index("format", "dayjs('2023-01-15 10:00:05')", ["ss"]).format();
    expect(result).toBe("05");
  });

  test('TC_SUP_081: 测试 Dayjs.format() 方法：格式化 \'SSS\'，覆盖 L286 switch branch-22, L332', () => {
    const result = index("format", "dayjs('2023-01-15 10:00:00.005')", ["SSS"]).format();
    expect(result).toBe("005");
  });

  test('TC_SUP_082: 测试 Dayjs.format() 方法：格式化 \'Z\'，覆盖 L286 switch branch-23, L334', () => {
    const result = index("format", "dayjs('2023-01-15')", ["Z"]).format();
    expect(result).toBe("-05:00");
  });

  test('TC_SUP_083: 测试 Dayjs.format() 方法：格式化 \'ZZ\'，覆盖 L341 binary-expr branch-2', () => {
    const result = index("format", "dayjs('2023-01-15')", ["ZZ"]).format();
    expect(result).toBe("-0500");
  });

  test('TC_SUP_084: 测试 Dayjs.format() 方法：格式化带转义字符，覆盖 L341 binary-expr branch-0', () => {
    const result = index("format", "dayjs('2023-01-15')", ["[Year:]YYYY"]).format();
    expect(result).toBe("Year:2023");
  });

  test('TC_SUP_085: 测试 Dayjs.format() 方法：格式化标准 token，覆盖 L341 binary-expr branch-1', () => {
    const result = index("format", "dayjs('2023-01-15')", ["YYYY"]).format();
    expect(result).toBe("2023");
  });

  test('TC_SUP_086: 测试 Dayjs.format() 方法：格式化未知 token，覆盖 L286 switch branch-24, L336, L338', () => {
    const result = index("format", "dayjs('2023-01-15')", ["UNKNOWN"]).format();
    expect(result).toBe("UNKNOWN");
  });

  test('TC_SUP_087: 测试 Dayjs.utcOffset() 方法，覆盖 L347', () => {
    const result = index("utcOffset", "dayjs('2023-01-15')").utcOffset();
    expect(result).toBe(-300);
  });

  test('TC_SUP_088: 测试 Dayjs.diff() 方法：单位为 \'year\'，覆盖 L351, L352, L353, L354, L355, L358 switch branch-0, L360, L361, L388 cond-expr branch-1', () => {
    const result = index("diff", "dayjs('2024-01-15')", ["2023-01-15", "year"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_089: 测试 Dayjs.diff() 方法：单位为 \'month\'，覆盖 L358 switch branch-1, L363, L364', () => {
    const result = index("diff", "dayjs('2023-03-15')", ["2023-01-15", "month"]).diff();
    expect(result).toBe(2);
  });

  test('TC_SUP_090: 测试 Dayjs.diff() 方法：单位为 \'quarter\'，覆盖 L358 switch branch-2, L366, L367', () => {
    const result = index("diff", "dayjs('2023-07-15')", ["2023-01-15", "quarter"]).diff();
    expect(result).toBe(2);
  });

  test('TC_SUP_091: 测试 Dayjs.diff() 方法：单位为 \'week\'，覆盖 L358 switch branch-3, L369, L370', () => {
    const result = index("diff", "dayjs('2023-01-22')", ["2023-01-15", "week"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_092: 测试 Dayjs.diff() 方法：单位为 \'day\'，覆盖 L358 switch branch-4, L372, L373', () => {
    const result = index("diff", "dayjs('2023-01-16')", ["2023-01-15", "day"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_093: 测试 Dayjs.diff() 方法：单位为 \'hour\'，覆盖 L358 switch branch-5, L375, L376', () => {
    const result = index("diff", "dayjs('2023-01-15 11:00:00')", ["2023-01-15 10:00:00", "hour"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_094: 测试 Dayjs.diff() 方法：单位为 \'minute\'，覆盖 L358 switch branch-6, L378, L379', () => {
    const result = index("diff", "dayjs('2023-01-15 10:01:00')", ["2023-01-15 10:00:00", "minute"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_095: 测试 Dayjs.diff() 方法：单位为 \'second\'，覆盖 L358 switch branch-7, L381, L382', () => {
    const result = index("diff", "dayjs('2023-01-15 10:00:01')", ["2023-01-15 10:00:00", "second"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_096: 测试 Dayjs.diff() 方法：单位为 \'millisecond\' (默认)，覆盖 L358 switch branch-8, L384, L385', () => {
    const result = index("diff", "dayjs('2023-01-15 10:00:00.001')", ["2023-01-15 10:00:00.000", "millisecond"]).diff();
    expect(result).toBe(1);
  });

  test('TC_SUP_097: 测试 Dayjs.diff() 方法：float 为 true，覆盖 L388 cond-expr branch-0', () => {
    const result = index("diff", "dayjs('2023-01-15 10:30:00')", ["2023-01-15 10:00:00", "hour", true]).diff();
    expect(result).toBe(0.5);
  });

  test('TC_SUP_098: 测试 Dayjs.daysInMonth() 方法，覆盖 L392', () => {
    const result = index("daysInMonth", "dayjs('2023-01-15')").daysInMonth();
    expect(result).toBe(31);
  });

  test('TC_SUP_099: 测试 Dayjs.$locale() 方法，覆盖 L396', () => {
    expect(() => { index("$locale", "dayjs('2023-01-15')"); }).toThrow();
  });

  test('TC_SUP_100: 测试 Dayjs.locale() 方法：无参数，覆盖 L400 if branch-0', () => {
    const result = index("locale", "dayjs('2023-01-15')", []).locale();
    expect(result).toBe("en");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_102: 测试 Dayjs.locale() 方法：设置无效 locale，覆盖 L403 if branch-1', () => {
    const result = index("locale", "dayjs('2023-01-15')", ["invalid"]).locale();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_103: 测试 Dayjs.clone() 方法，覆盖 L408', () => {
    const result = index("clone", "dayjs('2023-01-15')").clone();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_104: 测试 Dayjs.toDate() 方法，覆盖 L412', () => {
    const result = index("toDate", "dayjs('2023-01-15')").toDate();
    expect(result).toBe("2023-01-15T00:00:00.000");
  });

  test('TC_SUP_105: 测试 Dayjs.toString() 方法，覆盖 L427', () => {
    const result = index("toString", "dayjs('2023-01-15T10:00:00.000Z')").toString();
    expect(result).toBe("Sun, 15 Jan 2023 10:00:00 GMT");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC000: ', () => {
    const result = index();
    expect(result).toBe("");
  });

  test('TC_SUP_108: 测试 dayjs.unix() 方法，覆盖 L461', () => {
    const result = index("dayjs.unix", [1672531200]).unix();
    expect(result).toBe("2023-01-01T00:00:00.000Z");
  });

  test('TC_SUP_109: 测试 Dayjs.endOf() 方法：单位为 \'day\'，覆盖 L159 cond-expr branch-1', () => {
    const result = index("endOf", "dayjs('2023-01-15 10:30:45')", ["day"]).endOf();
    expect(result).toBe("2023-01-15T23:59:59.999");
  });

  test('TC_SUP_001: 测试 parseLocale 函数，当 preset 是一个对象时，覆盖 L17 if branch-1 和 L31-L33。', () => {
    const result = index("dayjs.locale", [{"name": "custom-locale", "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "weekdays": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}]);
    expect(result).toBe("返回 'custom-locale'");
  });

  test('TC_SUP_002: 测试 parseLocale 函数，当 preset 是字符串且 object 存在时，覆盖 L23-L24。', () => {
    const result = index("dayjs.locale", ["fr", {"name": "fr", "months": ["janvier", "f\u00e9vrier", "mars", "avril", "mai", "juin", "juillet", "ao\u00fbt", "septembre", "octobre", "novembre", "d\u00e9cembre"]}]);
    expect(result).toBe("返回 'fr'");
  });

  test('TC_SUP_003: 测试 parseLocale 函数，当 preset 是 \'zh-cn\' 且 \'zh-cn\' 和 \'zh\' 都未加载时，触发 L27 if branch-0 和 L28。', () => {
    const result = index("dayjs.locale", ["zh-cn"]);
    expect(result).toBe("返回 'en' (或默认语言)");
  });

  test('TC_SUP_004: 测试 parseLocale 函数，当 preset 导致 l 为 falsy，且 isLocal 为 falsy时，覆盖 L36 binary-expr branch-2。', () => {
    const result = index("dayjs.locale", ["non-existent-locale"]);
    expect(result).toBe("返回当前全局语言 'en'");
  });

  test('TC_SUP_005: 测试 parseDate 函数，当日期字符串缺少日部分且 utc 为 true 时，覆盖 L74 binary-expr branches。', () => {
    const result = index("dayjs", ["2023-01", {"utc": true}]);
    expect(result).toBe("返回 2023-01-01T00:00:00.000Z 的 Dayjs 对象");
  });

  test('TC_SUP_006: 测试 parseDate 函数，当日期字符串缺少时间部分且 utc 为 true 时，覆盖 L75 binary-expr branches。', () => {
    const result = index("dayjs", ["2023-01-01", {"utc": true}]);
    expect(result).toBe("返回 2023-01-01T00:00:00.000Z 的 Dayjs 对象");
  });

  test('TC_SUP_007: 测试 parseDate 函数，当日期字符串缺少日部分且 utc 为 false 时，覆盖 L77 binary-expr branch-1。', () => {
    const result = index("dayjs", ["2023-01"]);
    expect(result).toBe("返回 2023-01-01T00:00:00.000 (本地时区) 的 Dayjs 对象");
  });

  test('TC_SUP_008: 测试 Dayjs.$utils() 方法，覆盖 L112。', () => {
    const result = index("dayjs().$utils", "2023-01-01");
    expect(result).toBe("返回 Utils 对象");
  });

  test('TC_SUP_009: 测试 Dayjs.$g() 方法，当 input 为 undefined 时，覆盖 L133 if branch-0。', () => {
    const result = index("dayjs().year", "2023-01-01", [null]);
    expect(result).toBe("返回当前年份 2023");
  });

  test('TC_SUP_010: 测试 Dayjs.$g() 方法，当 input 有定义时，覆盖 L133 if branch-1 和 L134。', () => {
    const result = index("dayjs().year", "2023-01-01", [2024]);
    expect(result).toBe("返回年份设置为 2024 的 Dayjs 对象");
  });

  test('TC_SUP_011: 测试 Dayjs.startOf(\'year\') 方法，当 utc 为 true 时，覆盖 L150 cond-expr branch-0 和 L163 cond-expr branch-0。', () => {
    const result = index("dayjs.utc().startOf", ["year"]);
    expect(result).toBe("返回 UTC 2023-01-01 00:00:00.000 的 Dayjs 对象");
  });

  test('TC_SUP_012: 测试 Dayjs.endOf(\'year\') 方法，覆盖 L166 cond-expr branch-1。', () => {
    const result = index("dayjs().endOf", "2023-06-15", ["year"]);
    expect(result).toBe("返回 2023-12-31 23:59:59.999 的 Dayjs 对象");
  });

  test('TC_SUP_013: 测试 Dayjs.startOf(\'month\', true) 方法，覆盖 L169 cond-expr branch-0。', () => {
    const result = index("dayjs().startOf", "2023-06-15", ["month", true]);
    expect(result).toBe("返回 2023-06-01 00:00:00.000 的 Dayjs 对象");
  });

  test('TC_SUP_014: 测试 Dayjs.startOf(\'week\') 方法，自定义 weekStart 且 $W < weekStart 为 true，覆盖 L172-L174。', () => {
    const result = index("dayjs().startOf", "2023-01-01", ["week"], {"weekStart": 1});
    expect(result).toBe("返回 2022-12-26 00:00:00.000 的 Dayjs 对象 (周一为一周开始，2023-01-01是周日)");
  });

  test('TC_SUP_015: 测试 Dayjs.endOf(\'week\') 方法，自定义 weekStart 且 $W < weekStart 为 false，覆盖 L173 cond-expr branch-1 和 L174 cond-expr branch-1。', () => {
    const result = index("dayjs().endOf", "2023-01-02", ["week"], {"weekStart": 1});
    expect(result).toBe("返回 2023-01-08 23:59:59.999 的 Dayjs 对象 (周一为一周开始，2023-01-02是周一)");
  });

  test('TC_SUP_016: 测试 Dayjs.startOf(\'hour\') 方法，覆盖 L180。', () => {
    const result = index("dayjs().startOf", "2023-01-01 12:34:56", ["hour"]);
    expect(result).toBe("返回 2023-01-01 12:00:00.000 的 Dayjs 对象");
  });

  test('TC_SUP_017: 测试 Dayjs.startOf(\'minute\') 方法，覆盖 L182。', () => {
    const result = index("dayjs().startOf", "2023-01-01 12:34:56", ["minute"]);
    expect(result).toBe("返回 2023-01-01 12:34:00.000 的 Dayjs 对象");
  });

  test('TC_SUP_018: 测试 Dayjs.startOf(\'second\') 方法，覆盖 L184。', () => {
    const result = index("dayjs().startOf", "2023-01-01 12:34:56.789", ["second"]);
    expect(result).toBe("返回 2023-01-01 12:34:56.000 的 Dayjs 对象");
  });

  test('TC_SUP_019: 测试 Dayjs.$set() 方法，设置月份导致日期调整，覆盖 L209 if branch-0 和 L211-L214。', () => {
    const result = index("dayjs().set", "2023-03-31", ["month", 1]);
    expect(result).toBe("返回 2023-02-28 的 Dayjs 对象");
  });

  test('TC_SUP_020: 测试 Dayjs.$set() 方法，设置非月份/年份单位，覆盖 L215 if branch-0。', () => {
    const result = index("dayjs().set", "2023-01-01", ["hour", 10]);
    expect(result).toBe("返回小时设置为 10 的 Dayjs 对象");
  });

  test('TC_SUP_021: 测试 Dayjs.add(1, \'month\') 方法，覆盖 L236 if branch-0 和 L237。', () => {
    const result = index("dayjs().add", "2023-01-31", [1, "month"]);
    expect(result).toBe("返回 2023-02-28 的 Dayjs 对象");
  });

  test('TC_SUP_022: 测试 Dayjs.add(1, \'year\') 方法，覆盖 L239 if branch-0 和 L240。', () => {
    const result = index("dayjs().add", "2024-02-29", [1, "year"]);
    expect(result).toBe("返回 2025-02-28 的 Dayjs 对象");
  });

  test('TC_SUP_023: 测试 Dayjs.add(1, \'day\') 方法，覆盖 L242 if branch-0 和 L243，以及 L233-L234。', () => {
    const result = index("dayjs().add", "2023-01-01", [1, "day"]);
    expect(result).toBe("返回 2023-01-02 的 Dayjs 对象");
  });

  test('TC_SUP_024: 测试 Dayjs.add(1, \'week\') 方法，覆盖 L245 if branch-0 和 L246。', () => {
    const result = index("dayjs().add", "2023-01-01", [1, "week"]);
    expect(result).toBe("返回 2023-01-08 的 Dayjs 对象");
  });

  test('TC_SUP_025: 测试 Dayjs.format() 方法，当日期无效时，覆盖 L265 if branch-1。', () => {
    expect(() => { index("dayjs", [null], "format").format(); }).toThrow();
  });

  test('TC_SUP_026: 测试 Dayjs.format() 方法，不传入 formatStr 参数，覆盖 L267 binary-expr branch-1 和 L268-L269, L272-L273, L276, L280, L285。', () => {
    const result = index("dayjs().format", "2023-01-01 12:34:56").format();
    expect(result).toBe("返回默认格式的日期字符串");
  });

  test('TC_SUP_027: 测试 Dayjs.format() 方法，自定义 locale 的 monthsShort 为函数，覆盖 L274 binary-expr branch-0, branch-1。', () => {
    const result = index("dayjs().format", "2023-01-01", ["MMM"], {"monthsShort": "(d, f) => 'CustomMonth'"}).format();
    expect(result).toBe("返回 'CustomMonth'");
  });

  test('TC_SUP_028: 测试 Dayjs.format() 方法，自定义 locale 的 monthsShort 为 undefined，回退到 slice，覆盖 L274 binary-expr branch-2, branch-3。', () => {
    const result = index("dayjs().format", "2023-01-01", ["MMM"], {"monthsShort": null}).format();
    expect(result).toBe("返回 'Jan'");
  });

  test('TC_SUP_029: 测试 Dayjs.format(\'h\') 方法，小时为 0 (12 AM)，覆盖 L277 binary-expr branch-0。', () => {
    const result = index("dayjs().format", "2023-01-01 00:30:00", ["h"]);
    expect(result).toBe("返回 '12'");
  });

  test('TC_SUP_030: 测试 Dayjs.format(\'h\') 方法，小时为 13 (1 PM)，覆盖 L277 binary-expr branch-1。', () => {
    const result = index("dayjs().format", "2023-01-01 13:30:00", ["h"]);
    expect(result).toBe("返回 '1'");
  });

  test('TC_SUP_031: 测试 Dayjs.format(\'a\') 方法，小时为 1 (AM)，覆盖 L281 cond-expr branch-0 和 L282 cond-expr branch-0。', () => {
    const result = index("dayjs().format", "2023-01-01 01:00:00", ["a"]);
    expect(result).toBe("返回 'am'");
  });

  test('TC_SUP_032: 测试 Dayjs.format(\'A\') 方法，小时为 13 (PM)，覆盖 L281 cond-expr branch-1 和 L282 cond-expr branch-1。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["A"]);
    expect(result).toBe("返回 'PM'");
  });

  test('TC_SUP_033: 测试 Dayjs.format() 方法，自定义 meridiem 函数，覆盖 L280 binary-expr branch-0。', () => {
    const result = index("dayjs().format", "2023-01-01 01:00:00", ["a"], {"meridiem": "(h, m, l) => l ? 'custom_am' : 'CUSTOM_AM'"}).format();
    expect(result).toBe("返回 'custom_am'");
  });

  test('TC_SUP_034: 测试 Dayjs.format(\'YY\') 格式化，覆盖 L286 switch branch-0 和 L288。', () => {
    const result = index("dayjs().format", "2023-01-01", ["YY"]);
    expect(result).toBe("返回 '23'");
  });

  test('TC_SUP_035: 测试 Dayjs.format(\'YYYY\') 格式化，覆盖 L286 switch branch-1 和 L290。', () => {
    const result = index("dayjs().format", "2023-01-01", ["YYYY"]);
    expect(result).toBe("返回 '2023'");
  });

  test('TC_SUP_036: 测试 Dayjs.format(\'M\') 格式化，覆盖 L286 switch branch-2 和 L292。', () => {
    const result = index("dayjs().format", "2023-01-01", ["M"]);
    expect(result).toBe("返回 '1'");
  });

  test('TC_SUP_037: 测试 Dayjs.format(\'MM\') 格式化，覆盖 L286 switch branch-3 和 L294。', () => {
    const result = index("dayjs().format", "2023-01-01", ["MM"]);
    expect(result).toBe("返回 '01'");
  });

  test('TC_SUP_038: 测试 Dayjs.format(\'MMM\') 格式化，覆盖 L286 switch branch-4 和 L296。', () => {
    const result = index("dayjs().format", "2023-01-01", ["MMM"]);
    expect(result).toBe("返回 'Jan'");
  });

  test('TC_SUP_039: 测试 Dayjs.format(\'MMMM\') 格式化，覆盖 L286 switch branch-5 和 L298。', () => {
    const result = index("dayjs().format", "2023-01-01", ["MMMM"]);
    expect(result).toBe("返回 'January'");
  });

  test('TC_SUP_040: 测试 Dayjs.format(\'D\') 格式化，覆盖 L286 switch branch-6 和 L300。', () => {
    const result = index("dayjs().format", "2023-01-01", ["D"]);
    expect(result).toBe("返回 '1'");
  });

  test('TC_SUP_041: 测试 Dayjs.format(\'DD\') 格式化，覆盖 L286 switch branch-7 和 L302。', () => {
    const result = index("dayjs().format", "2023-01-01", ["DD"]);
    expect(result).toBe("返回 '01'");
  });

  test('TC_SUP_042: 测试 Dayjs.format(\'d\') 格式化，覆盖 L286 switch branch-8 和 L304。', () => {
    const result = index("dayjs().format", "2023-01-01", ["d"]);
    expect(result).toBe("返回 '0'");
  });

  test('TC_SUP_043: 测试 Dayjs.format(\'dd\') 格式化，覆盖 L286 switch branch-9 和 L306。', () => {
    const result = index("dayjs().format", "2023-01-01", ["dd"]);
    expect(result).toBe("返回 'Su'");
  });

  test('TC_SUP_044: 测试 Dayjs.format(\'ddd\') 格式化，覆盖 L286 switch branch-10 和 L308。', () => {
    const result = index("dayjs().format", "2023-01-01", ["ddd"]);
    expect(result).toBe("返回 'Sun'");
  });

  test('TC_SUP_045: 测试 Dayjs.format(\'dddd\') 格式化，覆盖 L286 switch branch-11 和 L310。', () => {
    const result = index("dayjs().format", "2023-01-01", ["dddd"]);
    expect(result).toBe("返回 'Sunday'");
  });

  test('TC_SUP_046: 测试 Dayjs.format(\'H\') 格式化，覆盖 L286 switch branch-12 和 L312。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["H"]);
    expect(result).toBe("返回 '13'");
  });

  test('TC_SUP_047: 测试 Dayjs.format(\'HH\') 格式化，覆盖 L286 switch branch-13 和 L314。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["HH"]);
    expect(result).toBe("返回 '13'");
  });

  test('TC_SUP_048: 测试 Dayjs.format(\'h\') 格式化，覆盖 L286 switch branch-14 和 L316。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["h"]);
    expect(result).toBe("返回 '1'");
  });

  test('TC_SUP_049: 测试 Dayjs.format(\'hh\') 格式化，覆盖 L286 switch branch-15 和 L318。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["hh"]);
    expect(result).toBe("返回 '01'");
  });

  test('TC_SUP_050: 测试 Dayjs.format(\'a\') 格式化，覆盖 L286 switch branch-16 和 L320。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["a"]);
    expect(result).toBe("返回 'pm'");
  });

  test('TC_SUP_051: 测试 Dayjs.format(\'A\') 格式化，覆盖 L286 switch branch-17 和 L322。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00", ["A"]);
    expect(result).toBe("返回 'PM'");
  });

  test('TC_SUP_052: 测试 Dayjs.format(\'m\') 格式化，覆盖 L286 switch branch-18 和 L324。', () => {
    const result = index("dayjs().format", "2023-01-01 13:05:00", ["m"]);
    expect(result).toBe("返回 '5'");
  });

  test('TC_SUP_053: 测试 Dayjs.format(\'mm\') 格式化，覆盖 L286 switch branch-19 和 L326。', () => {
    const result = index("dayjs().format", "2023-01-01 13:05:00", ["mm"]);
    expect(result).toBe("返回 '05'");
  });

  test('TC_SUP_054: 测试 Dayjs.format(\'s\') 格式化，覆盖 L286 switch branch-20 和 L328。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:05", ["s"]);
    expect(result).toBe("返回 '5'");
  });

  test('TC_SUP_055: 测试 Dayjs.format(\'ss\') 格式化，覆盖 L286 switch branch-21 和 L330。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:05", ["ss"]);
    expect(result).toBe("返回 '05'");
  });

  test('TC_SUP_056: 测试 Dayjs.format(\'SSS\') 格式化，覆盖 L286 switch branch-22 和 L332。', () => {
    const result = index("dayjs().format", "2023-01-01 13:00:00.123", ["SSS"]);
    expect(result).toBe("返回 '123'");
  });

  test('TC_SUP_057: 测试 Dayjs.format(\'Z\') 格式化，覆盖 L286 switch branch-23 和 L334。', () => {
    const result = index("dayjs().format", "2023-01-01", ["Z"]);
    expect(result).toBe("返回时区偏移字符串，例如 '+08:00'");
  });

  test('TC_SUP_058: 测试 Dayjs.format(\'ZZ\') 格式化，覆盖 L341 binary-expr branch-2。', () => {
    const result = index("dayjs().format", "2023-01-01", ["ZZ"]);
    expect(result).toBe("返回时区偏移字符串（无冒号），例如 '+0800'");
  });

  test('TC_SUP_059: 测试 Dayjs.format(\'[escaped text]\') 格式化，覆盖 L341 binary-expr branch-0。', () => {
    const result = index("dayjs().format", "2023-01-01", ["[Hello]"]);
    expect(result).toBe("返回 'Hello'");
  });

  test('TC_SUP_060: 测试 Dayjs.format(\'X\') 格式化，覆盖 L286 switch branch-24 (default) 和 L336, L338。', () => {
    const result = index("dayjs().format", "2023-01-01", ["X"]);
    expect(result).toBe("返回 'X'");
  });

  test('TC_SUP_061: 测试 Dayjs.diff() 方法，按年计算差异，覆盖 L355, L358 switch branch-0, L360, L361。', () => {
    const result = index("dayjs().diff", "2024-01-01", ["2023-01-01", "year"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_062: 测试 Dayjs.diff() 方法，按月计算差异，覆盖 L358 switch branch-1, L363, L364。', () => {
    const result = index("dayjs().diff", "2023-02-01", ["2023-01-01", "month"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_063: 测试 Dayjs.diff() 方法，按季度计算差异，覆盖 L358 switch branch-2, L366, L367。', () => {
    const result = index("dayjs().diff", "2023-04-01", ["2023-01-01", "quarter"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_064: 测试 Dayjs.diff() 方法，按周计算差异，覆盖 L358 switch branch-3, L369, L370。', () => {
    const result = index("dayjs().diff", "2023-01-08", ["2023-01-01", "week"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_065: 测试 Dayjs.diff() 方法，按天计算差异，覆盖 L358 switch branch-4, L372, L373。', () => {
    const result = index("dayjs().diff", "2023-01-02", ["2023-01-01", "day"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_066: 测试 Dayjs.diff() 方法，按小时计算差异，覆盖 L358 switch branch-5, L375, L376。', () => {
    const result = index("dayjs().diff", "2023-01-01 01:00:00", ["2023-01-01 00:00:00", "hour"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_067: 测试 Dayjs.diff() 方法，按分钟计算差异，覆盖 L358 switch branch-6, L378, L379。', () => {
    const result = index("dayjs().diff", "2023-01-01 00:01:00", ["2023-01-01 00:00:00", "minute"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_068: 测试 Dayjs.diff() 方法，按秒计算差异，覆盖 L358 switch branch-7, L381, L382。', () => {
    const result = index("dayjs().diff", "2023-01-01 00:00:01", ["2023-01-01 00:00:00", "second"]).diff();
    expect(result).toBe("返回 1");
  });

  test('TC_SUP_069: 测试 Dayjs.diff() 方法，float 参数为 true，覆盖 L388 cond-expr branch-0。', () => {
    const result = index("dayjs().diff", "2023-01-01 12:00:00", ["2023-01-01 00:00:00", "day", true]).diff();
    expect(result).toBe("返回 0.5");
  });

  test('TC_SUP_070: 测试 Dayjs.locale() 方法，设置新语言环境，覆盖 L400 if branch-1, L401-L404。', () => {
    const result = index("dayjs().locale", "2023-01-01", ["es", {"name": "es", "months": ["enero", "febrero"]}]).locale();
    expect(result).toBe("返回一个设置了 'es' 语言环境的 Dayjs 对象");
  });

  test('TC_SUP_071: 测试 Dayjs.locale() 方法，设置不存在的语言环境，覆盖 L403 if branch-1。', () => {
    const result = index("dayjs().locale", "2023-01-01", ["nonexistent-locale"]).locale();
    expect(result).toBe("返回一个语言环境未改变的 Dayjs 对象");
  });

  test('TC_SUP_072: 测试 Dayjs.prototype 上的 getter/setter (例如 year)，覆盖 L444。', () => {
    const result = index("dayjs().year", "2023-01-01");
    expect(result).toBe("返回年份 2023");
  });

  test('TC_SUP_073: 测试 dayjs.extend() 方法，首次安装插件，覆盖 L449 if branch-0, L450, L451, L453。', () => {
    const result = index("dayjs.extend", ["plugin_function_1", {}]).extend();
    expect(result).toBe("返回 dayjs 对象");
  });

  test('TC_SUP_074: 测试 dayjs.extend() 方法，重复安装已安装插件，覆盖 L449 if branch-1 和 L453。', () => {
    const result = index("dayjs.extend", ["plugin_function_2", {}], "const plugin_function_2 = () => {}; dayjs.extend(plugin_function_2);").extend();
    expect(result).toBe("返回 dayjs 对象");
  });

  test('TC_SUP_075: 测试 dayjs.unix() 方法，覆盖 L461。', () => {
    const result = index("dayjs.unix", [1672531200]).unix();
    expect(result).toBe("返回对应时间戳的 Dayjs 对象 (2023-01-01 00:00:00 UTC)");
  });
});
