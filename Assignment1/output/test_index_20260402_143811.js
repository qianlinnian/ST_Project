const _indexModule = require('../targets/index.js');
const dayjs = _indexModule.default || _indexModule;
const { parseDate, parseLocale, loadedLocales } = _indexModule;

// Mock constants (C) based on common dayjs usage and the provided source code.
// These are internal to the module, but we need them for interpreting expected outputs.
const C = {
  REGEX_PARSE: /(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[^0-9]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?\.?(\d+)?/,
  INVALID_DATE_STRING: 'Invalid Date',
  FORMAT_DEFAULT: 'YYYY-MM-DDTHH:mm:ssZ',
  Y: 'year',
  M: 'month',
  Q: 'quarter',
  W: 'week',
  D: 'day',
  DATE: 'date',
  H: 'hour',
  MIN: 'minute',
  S: 'second',
  MS: 'millisecond',
  MILLISECONDS_A_MINUTE: 60 * 1000,
  MILLISECONDS_A_HOUR: 60 * 60 * 1000,
  MILLISECONDS_A_SECOND: 1000,
  MILLISECONDS_A_DAY: 24 * 60 * 60 * 1000,
  MILLISECONDS_A_WEEK: 7 * 24 * 60 * 60 * 1000
};

// Helper function to create Date objects from descriptive strings in JSON
const createDateFromString = (dateString) => {
  if (!dateString.startsWith('Date object for ')) {
    return new Date(dateString); // Assume it's a direct date string
  }
  const actualDateStr = dateString.substring('Date object for '.length);
  // Handle UTC dates explicitly marked with Z
  if (actualDateStr.endsWith('Z')) {
    return new Date(actualDateStr);
  }
  // Handle local dates like "YYYY-MM-DD HH:mm:ss.SSS"
  const match = actualDateStr.match(/(\d{4})-(\d{2})-(\d{2})(?: (\d{2}):(\d{2}):(\d{2})(?:\.(\d{3}))?)?/);
  if (match) {
    const [, year, month, day, hour = 0, minute = 0, second = 0, millisecond = 0] = match;
    return new Date(
      parseInt(year, 10),
      parseInt(month, 10) - 1,
      parseInt(day, 10),
      parseInt(hour, 10),
      parseInt(minute, 10),
      parseInt(second, 10),
      parseInt(millisecond, 10)
    );
  }
  // Fallback for simpler date strings like "YYYY-MM-DD"
  return new Date(actualDateStr);
};

// Helper to compare Dayjs instances or their internal $d property
const compareDayjsInstance = (received, expected) => {
  if (expected === null) {
    return received === null;
  }
  if (!received || typeof received.valueOf !== 'function') {
    return false; // Not a Dayjs instance
  }

  if (expected.$d) {
    const expectedDate = createDateFromString(expected.$d);
    // For Dayjs instances, compare their internal Date object's time
    return received && received.$d && received.$d.getTime() === expectedDate.getTime();
  }
  // For other properties like $L, $x, $isDayjsObject
  let match = true;
  if (expected.$L !== undefined) match = match && received.$L === expected.$L;
  if (expected.$x !== undefined) match = match && JSON.stringify(received.$x) === JSON.stringify(expected.$x);
  if (expected.$isDayjsObject !== undefined) match = match && received.$isDayjsObject === expected.$isDayjsObject;
  // The 'cloned' property in JSON is a flag, not a direct value to compare.
  // It implies the result should be a valid Dayjs object, which is covered by other checks.
  return match;
};

// Custom matcher for Dayjs instances
expect.extend({
  toBeDayjsInstance(received, expected) {
    const pass = compareDayjsInstance(received, expected);
    if (pass) {
      return {
        message: () => `expected ${JSON.stringify(received)} not to be a Dayjs instance matching ${JSON.stringify(expected)}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${JSON.stringify(received)} to be a Dayjs instance matching ${JSON.stringify(expected)}. Received: ${JSON.stringify({ $d: received?.$d?.toISOString(), $L: received?.$L, $x: received?.$x, $isDayjsObject: received?.$isDayjsObject })}`,
        pass: false,
      };
    }
  },
});

// Store initial locale state to reset before tests
const initialDefaultLocale = dayjs.locale();
const initialLoadedLocales = JSON.parse(JSON.stringify(dayjs.Ls)); // Deep copy

describe('dayjs module', () => {
  // Reset global locale state before each test that modifies it
  beforeEach(() => {
    // Clear all dynamically added locales
    for (const key in loadedLocales) {
      if (key !== 'en') { // Keep 'en' as it's the default
        delete loadedLocales[key];
      }
    }
    // Restore 'en' to its initial state if it was modified
    loadedLocales.en = JSON.parse(JSON.stringify(initialLoadedLocales.en));
    // Reset global L to initialDefaultLocale
    dayjs.locale(initialDefaultLocale, initialLoadedLocales[initialDefaultLocale]);
  });

  describe('isDayjs', () => {
    test('TC001: d is an instance of Dayjs', () => {
      // The actual Dayjs class is internal, so we need to create a dayjs instance
      const d = dayjs();
      expect(dayjs.isDayjs(d)).toBe(true);
    });

    test('TC002: d has $isDayjsObject property', () => {
      const d = { $isDayjsObject: true };
      expect(dayjs.isDayjs(d)).toBe(true);
    });

    test('TC003: d is a plain object without $isDayjsObject', () => {
      const d = { foo: 'bar' };
      expect(dayjs.isDayjs(d)).toBe(false);
    });

    test('TC004: 测试 isDayjs: 输入 null', () => {
      const d = null;
      expect(dayjs.isDayjs(d)).toBe(false);
    });

    test('TC005: 测试 isDayjs: 输入 undefined', () => {
      const d = undefined; // JSON input was null, but description says undefined, testing undefined
      expect(dayjs.isDayjs(d)).toBe(false);
    });
  });

  describe('parseLocale', () => {
    test('TC006: 测试 parseLocale: preset 为 null (返回全局 L)', () => {
      const result = parseLocale(null, null, false);
      expect(result).toBe('en');
      expect(dayjs.locale()).toBe('en'); // Global L should remain 'en'
    });

    test('TC007: 测试 parseLocale: preset 为已加载的字符串 locale (返回该 locale)', () => {
      // Ensure 'en' is loaded
      dayjs.locale('en', { name: 'en' });
      const result = parseLocale('en', null, false);
      expect(result).toBe('en');
      expect(dayjs.locale()).toBe('en'); // Global L should remain 'en'
    });

    test('TC008: 测试 parseLocale: preset 为未加载的字符串 locale, 带有 object (加载并返回)', () => {
      const newLocale = { name: 'fr', months: ['Janvier'] };
      const result = parseLocale('fr', newLocale, false);
      expect(result).toBe('fr');
      expect(dayjs.locale()).toBe('fr'); // Global L should be updated
      expect(loadedLocales.fr).toEqual(newLocale);
    });

    test('TC009: 测试 parseLocale: preset 为带连字符的字符串 locale, 未加载, 无 object (递归调用)', () => {
      // Assuming 'zh' is not loaded, and 'zh-cn' is not loaded
      const result = parseLocale('zh-cn', null, false);
      // It should try to load 'zh', fail, and return the current global locale 'en'
      expect(result).toBe('en');
      expect(dayjs.locale()).toBe('en'); // Global L should remain 'en'
      expect(loadedLocales['zh-cn']).toBeUndefined();
      expect(loadedLocales.zh).toBeUndefined();
    });

    test('TC010: 测试 parseLocale: preset 为未加载的字符串 locale, 无 object, 无连字符 (返回全局 L)', () => {
      const result = parseLocale('es', null, false);
      expect(result).toBe('en');
      expect(dayjs.locale()).toBe('en'); // Global L should remain 'en'
      expect(loadedLocales.es).toBeUndefined();
    });

    test('TC011: 测试 parseLocale: preset 为对象 locale (加载并返回)', () => {
      const newLocale = { name: 'de', months: ['Januar'] };
      const result = parseLocale(newLocale, null, false);
      expect(result).toBe('de');
      expect(dayjs.locale()).toBe('de'); // Global L should be updated
      expect(loadedLocales.de).toEqual(newLocale);
    });

    test('TC012: 测试 parseLocale: preset 为未加载的字符串 locale, 带有 object, isLocal 为 true (加载但不改变全局 L)', () => {
      const newLocale = { name: 'fr', months: ['Janvier'] };
      const initialGlobalLocale = dayjs.locale(); // Should be 'en'
      const result = parseLocale('fr', newLocale, true);
      expect(result).toBe('fr');
      expect(dayjs.locale()).toBe(initialGlobalLocale); // Global L should NOT be updated
      expect(loadedLocales.fr).toEqual(newLocale);
    });
  });

  describe('dayjs function', () => {
    test('TC013: dayjs(date) - date is a Dayjs instance, should clone', () => {
      const original = dayjs();
      const cloned = dayjs(original);
      expect(cloned).not.toBe(original); // Should be a new instance
      expect(cloned.valueOf()).toBe(original.valueOf()); // But same date value
      expect(dayjs.isDayjs(cloned)).toBe(true);
    });

    test('TC014: dayjs(date) - date is a string', () => {
      const d = dayjs('2023-01-01');
      expect(d).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(d.$L).toBe('en');
      expect(d.$x).toEqual({});
      expect(d.$isDayjsObject).toBe(true);
    });

    test('TC015: dayjs() - no arguments, current date', () => {
      const now = dayjs();
      // Cannot assert exact date, but check type and validity
      expect(dayjs.isDayjs(now)).toBe(true);
      expect(now.isValid()).toBe(true);
    });

    test('TC016: dayjs(date, c) - c is an object with locale and x', () => {
      const newLocale = { name: 'fr', months: ['Janvier'] };
      dayjs.locale('fr', newLocale); // Load 'fr' globally first
      const d = dayjs('2023-01-01', { locale: 'fr', x: { foo: 'bar' } });
      expect(d).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(d.$L).toBe('fr');
      expect(d.$x).toEqual({ foo: 'bar' });
      expect(d.$isDayjsObject).toBe(true);
    });
  });

  describe('parseDate', () => {
    test('TC018: cfg.date is null', () => {
      const cfg = { date: null };
      const date = parseDate(cfg);
      expect(date.toString()).toBe(C.INVALID_DATE_STRING);
    });

    test('TC019: cfg.date is a UTC string (ending with Z)', () => {
      const cfg = { date: '2023-01-01T00:00:00.000Z' };
      const date = parseDate(cfg);
      expect(date.toISOString()).toBe('2023-01-01T00:00:00.000Z');
    });

    test('TC020: cfg.date is a UTC string (ending with Z) with time', () => {
      const cfg = { date: '2023-01-01T12:30:00.000Z' };
      const date = parseDate(cfg);
      expect(date.toISOString()).toBe('2023-01-01T12:30:00.000Z');
    });

    test('TC021: cfg.date is a custom format string, utc is true', () => {
      const cfg = { date: '2023-01-01 12:30:45.123', utc: true };
      const date = parseDate(cfg);
      // Date.UTC expects year, month (0-11), day, hour, minute, second, millisecond
      const expectedDate = new Date(Date.UTC(2023, 0, 1, 12, 30, 45, 123));
      expect(date.getTime()).toBe(expectedDate.getTime());
    });

    test('TC022: cfg.date is a custom format string, utc is false', () => {
      const cfg = { date: '2023-01-01 12:30:45.123', utc: false };
      const date = parseDate(cfg);
      const expectedDate = new Date(2023, 0, 1, 12, 30, 45, 123);
      expect(date.getTime()).toBe(expectedDate.getTime());
    });

    test('TC023: cfg.date is an invalid date string', () => {
      const cfg = { date: 'invalid date string' };
      const date = parseDate(cfg);
      expect(date.toString()).toBe(C.INVALID_DATE_STRING);
    });

    test('TC024: cfg.date is a timestamp', () => {
      const cfg = { date: 1672531200000 }; // 2023-01-01T00:00:00.000Z
      const date = parseDate(cfg);
      expect(date.getTime()).toBe(1672531200000);
    });

    test('TC025: cfg.date is a simple YYYY-MM-DD string', () => {
      const cfg = { date: '2023-01-01' };
      const date = parseDate(cfg);
      const expectedDate = new Date(2023, 0, 1);
      expect(date.getTime()).toBe(expectedDate.getTime());
    });

    test('TC104: cfg.date is a YYYY string', () => {
      const cfg = { date: '2023' };
      const date = parseDate(cfg);
      const expectedDate = new Date(2023, 0, 1); // Dayjs parses 'YYYY' as YYYY-01-01
      expect(date.getTime()).toBe(expectedDate.getTime());
    });

    test('TC105: cfg.date is a YYYY-MM string', () => {
      const cfg = { date: '2023-03' };
      const date = parseDate(cfg);
      const expectedDate = new Date(2023, 2, 1); // Dayjs parses 'YYYY-MM' as YYYY-MM-01
      expect(date.getTime()).toBe(expectedDate.getTime());
    });
  });

  describe('Dayjs class constructor and init', () => {
    test('TC026: Dayjs constructor with default locale and no x', () => {
      const d = dayjs('2023-01-01'); // Use dayjs function to create instance
      expect(d).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(d.$L).toBe('en');
      expect(d.$x).toEqual({});
      expect(d.$isDayjsObject).toBe(true);
      expect(d.$y).toBe(2023);
      expect(d.$M).toBe(0);
      expect(d.$D).toBe(1);
    });

    test('TC030: Dayjs constructor with custom locale', () => {
      const newLocale = { name: 'fr', months: ['Janvier'] };
      dayjs.locale('fr', newLocale);
      const d = dayjs('2023-01-01', { locale: 'fr' });
      expect(d).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(d.$L).toBe('fr');
    });

    test('TC034: Dayjs constructor with custom x object', () => {
      const d = dayjs('2023-01-01', { x: { custom: 1 } });
      expect(d).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(d.$x).toEqual({ custom: 1 });
    });
  });

  describe('Dayjs methods', () => {
    test('TC027: 测试 Dayjs.isValid: 有效日期', () => {
      const instance = dayjs('2023-01-01');
      expect(instance.isValid()).toBe(true);
    });

    test('TC028: 测试 Dayjs.isValid: 无效日期', () => {
      const instance = dayjs(null);
      expect(instance.isValid()).toBe(false);
    });

    test('TC029: 测试 Dayjs.isSame: 相同日期, 相同单位 (年)', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2023-06-20');
      expect(instance.isSame(that, 'year')).toBe(true);
    });

    test('TC030: 测试 Dayjs.isSame: 相同日期, 相同单位 (月), 边界值', () => {
      const instance = dayjs('2023-01-01');
      const that = dayjs('2023-01-31');
      expect(instance.isSame(that, 'month')).toBe(true);
    });

    test('TC031: 测试 Dayjs.isSame: 不同日期, 相同单位, 外部 (之前)', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2022-12-31');
      expect(instance.isSame(that, 'year')).toBe(false);
    });

    test('TC032: 测试 Dayjs.isSame: 不同日期, 相同单位, 外部 (之后)', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2024-01-01');
      expect(instance.isSame(that, 'year')).toBe(false);
    });

    test('TC033: 测试 Dayjs.isAfter: this 在 that 之后', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2023-01-14');
      expect(instance.isAfter(that, 'day')).toBe(true);
    });

    test('TC034: 测试 Dayjs.isAfter: this 在 that 之前', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2023-01-16');
      expect(instance.isAfter(that, 'day')).toBe(false);
    });

    test('TC035: 测试 Dayjs.isBefore: this 在 that 之前', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2023-01-16');
      expect(instance.isBefore(that, 'day')).toBe(true);
    });

    test('TC036: 测试 Dayjs.isBefore: this 在 that 之后', () => {
      const instance = dayjs('2023-01-15');
      const that = dayjs('2023-01-14');
      expect(instance.isBefore(that, 'day')).toBe(false);
    });

    test('TC037: 测试 Dayjs.$g: 作为 getter', () => {
      const instance = dayjs('2023-01-01');
      // $g is an internal method, we test the public API that uses it.
      expect(instance.year()).toBe(2023);
    });

    test('TC038: 测试 Dayjs.$g: 作为 setter', () => {
      const instance = dayjs('2023-01-01');
      // $g is an internal method, we test the public API that uses it.
      const result = instance.year(2024);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2024-01-01' });
    });

    test('TC039: 测试 Dayjs.unix: 返回 Unix 时间戳', () => {
      const instance = dayjs('1970-01-01T00:00:00.000Z');
      expect(instance.unix()).toBe(0);
    });

    test('TC040: 测试 Dayjs.valueOf: 返回毫秒时间戳', () => {
      const instance = dayjs('1970-01-01T00:00:00.000Z');
      expect(instance.valueOf()).toBe(0);
    });

    test('TC041: 测试 Dayjs.startOf: "year"', () => {
      const instance = dayjs('2023-06-15');
      const result = instance.startOf('year');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-01 00:00:00.000' });
    });

    test('TC042: 测试 Dayjs.endOf: "year"', () => {
      const instance = dayjs('2023-06-15');
      const result = instance.endOf('year');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-12-31 23:59:59.999' });
    });

    test('TC043: 测试 Dayjs.startOf: "month"', () => {
      const instance = dayjs('2023-06-15');
      const result = instance.startOf('month');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-06-01 00:00:00.000' });
    });

    test('TC044: 测试 Dayjs.endOf: "month"', () => {
      const instance = dayjs('2023-06-15');
      const result = instance.endOf('month');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-06-30 23:59:59.999' });
    });

    test('TC045: 测试 Dayjs.startOf: "week" (Sunday weekStart)', () => {
      const instance = dayjs('2023-01-15'); // Sunday
      const result = instance.startOf('week');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 00:00:00.000' });
    });

    test('TC046: 测试 Dayjs.startOf: "week" (Wednesday, Sunday weekStart)', () => {
      const instance = dayjs('2023-01-18'); // Wednesday
      const result = instance.startOf('week');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 00:00:00.000' });
    });

    test('TC047: 测试 Dayjs.endOf: "week"', () => {
      const instance = dayjs('2023-01-15'); // Sunday
      const result = instance.endOf('week');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-21 23:59:59.999' });
    });

    test('TC048: 测试 Dayjs.startOf: "day"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.startOf('day');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 00:00:00.000' });
    });

    test('TC049: 测试 Dayjs.endOf: "day"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.endOf('day');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 23:59:59.999' });
    });

    test('TC050: 测试 Dayjs.startOf: "hour"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.startOf('hour');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:00:00.000' });
    });

    test('TC051: 测试 Dayjs.endOf: "hour"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.endOf('hour');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:59:59.999' });
    });

    test('TC052: 测试 Dayjs.startOf: "minute"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.startOf('minute');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:00.000' });
    });

    test('TC053: 测试 Dayjs.endOf: "minute"', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.endOf('minute');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:59.999' });
    });

    test('TC054: 测试 Dayjs.startOf: "second"', () => {
      const instance = dayjs('2023-01-15 10:30:45.123');
      const result = instance.startOf('second');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:45.000' });
    });

    test('TC055: 测试 Dayjs.endOf: "second"', () => {
      const instance = dayjs('2023-01-15 10:30:45.123');
      const result = instance.endOf('second');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:45.999' });
    });

    test('TC056: 测试 Dayjs.startOf: 默认单位 (clone)', () => {
      const instance = dayjs('2023-01-15 10:30:45.123');
      const result = instance.startOf('invalid-unit'); // Invalid unit should return clone
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:45.123' });
      expect(result).not.toBe(instance); // Should be a clone
    });

    test('TC057: 测试 Dayjs.$set: 设置 C.D (日期)', () => {
      const instance = dayjs('2023-01-15');
      // $set is an internal method, we directly call it on a cloned instance to avoid modifying the original
      const result = instance.clone().$set('date', 20);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-20' });
    });

    test('TC058: 测试 Dayjs.$set: 设置 C.M (月份), 正常情况', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.clone().$set('month', 5); // Month is 0-indexed, so 5 is June
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-06-15' });
    });

    test('TC059: 测试 Dayjs.$set: 设置 C.M (月份), 目标月份天数少于当前日期', () => {
      const instance = dayjs('2023-03-31'); // March 31st
      const result = instance.clone().$set('month', 3); // April (0-indexed 3), which has 30 days
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-04-30' });
    });

    test('TC060: 测试 Dayjs.$set: 设置 C.Y (年份), 正常情况', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.clone().$set('year', 2024);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2024-01-15' });
    });

    test('TC061: 测试 Dayjs.$set: 设置 C.Y (年份), 闰年/非闰年边界 (2月29日)', () => {
      const instance = dayjs('2024-02-29'); // Leap year
      const result = instance.clone().$set('year', 2023); // Non-leap year
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-02-28' });
    });

    test('TC062: 测试 Dayjs.$set: 设置 C.H (小时)', () => {
      const instance = dayjs('2023-01-15 10:30:45');
      const result = instance.clone().$set('hour', 14);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 14:30:45' });
    });

    test('TC063: 测试 Dayjs.$set: 设置 C.MS (毫秒)', () => {
      const instance = dayjs('2023-01-15 10:30:45.123');
      const result = instance.clone().$set('millisecond', 456);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:30:45.456' });
    });

    test('TC064: 测试 Dayjs.$set: 设置无效单位 (不应改变日期)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.clone().$set('invalid', 100);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15' });
    });

    test('TC106: 测试 Dayjs.$set: 设置 C.W (周), 应该通过 C.D 间接设置', () => {
      // As analyzed in thought process, `set('week', int)` directly on `$set`
      // does not have a specific handler in the switch statement for 'W'.
      // `Utils.p('week')` returns 'W'.
      // The `name` map in `$set` does not contain 'W'.
      // So `name` will be undefined, and `this.$d[name](arg)` will not execute.
      // The date should remain unchanged.
      const initialDate = '2023-01-15';
      const instance = dayjs(initialDate);
      const result = instance.clone().$set('week', 1);
      expect(result).toBeDayjsInstance({ $d: `Date object for ${initialDate}` }); // Date should not change
    });

    test('TC065: 测试 Dayjs.set: 设置 C.D (日期)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.set('date', 20);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-20' });
      expect(result).not.toBe(instance); // Should return a new instance
    });

    test('TC066: 测试 Dayjs.get: 获取年份', () => {
      const instance = dayjs('2023-01-15');
      expect(instance.get('year')).toBe(2023);
    });

    test('TC067: 测试 Dayjs.add: 增加月份 (正数)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.add(2, 'month');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-03-15' });
    });

    test('TC068: 测试 Dayjs.add: 增加年份 (负数)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.add(-1, 'year');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2022-01-15' });
    });

    test('TC069: 测试 Dayjs.add: 增加天数 (正数)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.add(5, 'day');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-20' });
    });

    test('TC070: 测试 Dayjs.add: 增加周数 (正数)', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.add(2, 'week');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-29' });
    });

    test('TC071: 测试 Dayjs.add: 增加小时 (正数)', () => {
      const instance = dayjs('2023-01-15 10:00:00');
      const result = instance.add(3, 'hour');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 13:00:00' });
    });

    test('TC072: 测试 Dayjs.add: 增加毫秒 (正数)', () => {
      const instance = dayjs('2023-01-15 10:00:00.000');
      const result = instance.add(500, 'millisecond');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 10:00:00.500' });
    });

    test('TC073: 测试 Dayjs.subtract: 减去天数', () => {
      const instance = dayjs('2023-01-15');
      const result = instance.subtract(5, 'day');
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-10' });
    });

    test('TC074: 测试 Dayjs.format: 无效日期', () => {
      const instance = dayjs(null);
      expect(instance.format('YYYY-MM-DD')).toBe('Invalid Date');
    });

    test('TC075: 测试 Dayjs.format: 默认格式', () => {
      // Cannot assert exact timezone, so check format structure
      const instance = dayjs('2023-01-01T12:30:45.123Z');
      const formatted = instance.format(); // Uses C.FORMAT_DEFAULT: 'YYYY-MM-DDTHH:mm:ssZ'
      // The `format` function replaces 'Z' with the actual timezone offset (e.g., "+0000" or "-0800").
      const expectedRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{4}$/;
      expect(formatted).toMatch(expectedRegex);
    });

    test('TC076: 测试 Dayjs.format: 包含所有主要格式令牌', () => {
      const instance = dayjs('2023-01-15T10:30:45.123'); // Local time
      // The format string `YYYY-MM-DD HH:mm:ss.SSS ddd A [Year:]YYYY` does not have 'Z' or 'ZZ'.
      // So the output should not contain timezone offset.
      const expected = '2023-01-15 10:30:45.123 Sun AM Year:2023';
      expect(instance.format('YYYY-MM-DD HH:mm:ss.SSS ddd A [Year:]YYYY')).toBe(expected);
    });

    test('TC077: 测试 Dayjs.format: AM/PM 格式 (h, hh, a, A) - AM', () => {
      const instance = dayjs('2023-01-15T01:05:00.000'); // Local time
      expect(instance.format('h hh a A')).toBe('1 01 am AM');
    });

    test('TC078: 测试 Dayjs.format: PM 格式 (h, hh, a, A) - PM', () => {
      const instance = dayjs('2023-01-15T13:05:00.000'); // Local time
      expect(instance.format('h hh a A')).toBe('1 01 pm PM');
    });

    test('TC125: 测试 Dayjs.format: Z (timezone offset) token', () => {
      const instance = dayjs('2023-01-15T10:30:45.123'); // Local time
      // Calculate the expected offset based on the test runner's timezone.
      const offsetMinutes = -instance.$d.getTimezoneOffset(); // getTimezoneOffset returns minutes difference from UTC
      const sign = offsetMinutes >= 0 ? '+' : '-';
      const absOffset = Math.abs(offsetMinutes);
      const hours = Math.floor(absOffset / 60);
      const minutes = absOffset % 60;
      const expectedOffset = `${sign}${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
      expect(instance.format('Z')).toBe(expectedOffset);
    });

    test('TC079: 测试 Dayjs.utcOffset: 返回 UTC 偏移量', () => {
      const instance = dayjs('2023-01-01');
      // Calculate the expected offset based on the test runner's timezone.
      const expectedOffset = -Math.round(instance.$d.getTimezoneOffset() / 15) * 15;
      expect(instance.utcOffset()).toBe(expectedOffset);
    });

    test('TC080: 测试 Dayjs.diff: 差异年份, float 为 true', () => {
      const instance = dayjs('2024-01-01');
      const input = '2023-01-01';
      expect(instance.diff(input, 'year', true)).toBe(1);
    });

    test('TC081: 测试 Dayjs.diff: 差异月份, float 为 false', () => {
      const instance = dayjs('2023-03-15');
      const input = '2023-01-15';
      expect(instance.diff(input, 'month', false)).toBe(2);
    });

    test('TC082: 测试 Dayjs.diff: 差异季度, float 为 true', () => {
      const instance = dayjs('2023-07-01');
      const input = '2023-01-01';
      expect(instance.diff(input, 'quarter', true)).toBe(2);
    });

    test('TC083: 测试 Dayjs.diff: 差异周, float 为 true', () => {
      const instance = dayjs('2023-01-15'); // Sunday
      const input = '2023-01-01'; // Sunday
      expect(instance.diff(input, 'week', true)).toBe(2);
    });

    test('TC084: 测试 Dayjs.diff: 差异天, float 为 false', () => {
      const instance = dayjs('2023-01-15');
      const input = '2023-01-10';
      expect(instance.diff(input, 'day', false)).toBe(5);
    });

    test('TC085: 测试 Dayjs.diff: 差异小时, float 为 true', () => {
      const instance = dayjs('2023-01-01 10:00:00');
      const input = '2023-01-01 08:00:00';
      expect(instance.diff(input, 'hour', true)).toBe(2);
    });

    test('TC086: 测试 Dayjs.diff: 差异分钟, float 为 false', () => {
      const instance = dayjs('2023-01-01 10:30:00');
      const input = '2023-01-01 10:20:00';
      expect(instance.diff(input, 'minute', false)).toBe(10);
    });

    test('TC087: 测试 Dayjs.diff: 差异秒, float 为 true', () => {
      const instance = dayjs('2023-01-01 10:00:30');
      const input = '2023-01-01 10:00:10';
      expect(instance.diff(input, 'second', true)).toBe(20);
    });

    test('TC088: 测试 Dayjs.diff: 差异毫秒 (默认单位), float 为 false', () => {
      const instance = dayjs('2023-01-01 10:00:00.500');
      const input = '2023-01-01 10:00:00.100';
      expect(instance.diff(input, 'millisecond', false)).toBe(400);
    });

    test('TC089: 测试 Dayjs.daysInMonth: 返回月份天数', () => {
      const instance = dayjs('2023-02-15'); // February 2023 is not a leap year
      expect(instance.daysInMonth()).toBe(28);
    });

    test('TC090: 测试 Dayjs.$locale: 返回当前 locale 对象', () => {
      const instance = dayjs('2023-01-01');
      const locale = instance.$locale();
      expect(locale.name).toBe('en');
      expect(locale.months).toBeDefined();
    });

    test('TC091: 测试 Dayjs.locale: 无 preset (getter)', () => {
      const instance = dayjs('2023-01-01');
      expect(instance.locale()).toBe('en');
    });

    test('TC092: 测试 Dayjs.locale: 设置未加载的 locale (字符串和对象)', () => {
      const instance = dayjs('2023-01-01');
      const newLocale = { name: 'fr', months: ['Janvier'] };
      const result = instance.locale('fr', newLocale);
      expect(result).toBeDayjsInstance({ $L: 'fr' });
      expect(result).not.toBe(instance); // Should return a new instance
      expect(loadedLocales.fr).toEqual(newLocale); // Should be loaded globally
      expect(dayjs.locale()).toBe('en'); // Global locale should not change by instance.locale()
    });

    test('TC093: 测试 Dayjs.locale: 设置已加载的 locale (字符串)', () => {
      dayjs.locale('es', { name: 'es' }); // Load 'es' globally first
      const instance = dayjs('2023-01-01');
      const result = instance.locale('es');
      expect(result).toBeDayjsInstance({ $L: 'es' });
      expect(result).not.toBe(instance);
      expect(dayjs.locale()).toBe('en'); // Global locale should not change
    });

    test('TC094: 测试 Dayjs.locale: 设置未知 locale (无对象), 不应改变 locale', () => {
      const instance = dayjs('2023-01-01');
      const result = instance.locale('unknown', null);
      expect(result).toBeDayjsInstance({ $L: 'en' }); // Locale should remain 'en'
      expect(result).not.toBe(instance);
      expect(loadedLocales.unknown).toBeUndefined();
    });

    test('TC095: 测试 Dayjs.clone: 克隆实例', () => {
      const instance = dayjs('2023-01-01');
      const cloned = instance.clone();
      expect(cloned).toBeDayjsInstance({ $d: 'Date object for 2023-01-01' });
      expect(cloned).not.toBe(instance); // Should be a new instance
    });

    test('TC096: 测试 Dayjs.toDate: 返回原生 Date 对象', () => {
      const instance = dayjs('2023-01-01');
      const date = instance.toDate();
      expect(date).toBeInstanceOf(Date);
      expect(date.getTime()).toBe(createDateFromString('Date object for 2023-01-01').getTime());
    });

    test('TC097: 测试 Dayjs.toJSON: 有效日期', () => {
      const instance = dayjs('2023-01-01T00:00:00.000Z');
      expect(instance.toJSON()).toBe('2023-01-01T00:00:00.000Z');
    });

    test('TC098: 测试 Dayjs.toJSON: 无效日期', () => {
      const instance = dayjs(null);
      expect(instance.toJSON()).toBeNull();
    });

    test('TC099: 测试 Dayjs.toISOString: 返回 ISO 8601 字符串', () => {
      const instance = dayjs('2023-01-01T12:30:45.123Z');
      expect(instance.toISOString()).toBe('2023-01-01T12:30:45.123Z');
    });

    test('TC100: 测试 Dayjs.toString: 返回 UTC 字符串', () => {
      const instance = dayjs('2023-01-01T12:30:45.123Z');
      expect(instance.toString()).toBe('Sun, 01 Jan 2023 12:30:45 GMT');
    });

    test('TC123: 测试 Dayjs.$set with utc: true', () => {
      const instance = dayjs('2023-01-15 00:00:00', { utc: true });
      expect(instance).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 00:00:00.000Z' });
    });

    test('TC124: 测试 Dayjs.$set: 设置 C.H (小时) with utc: true', () => {
      const instance = dayjs('2023-01-15 10:30:45', { utc: true });
      const result = instance.clone().$set('hour', 14);
      expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-15 14:30:45Z' });
    });

    describe('Dayjs getters and setters (via proto loop)', () => {
      test('TC107: 测试 Dayjs.year() getter', () => {
        const instance = dayjs('2023-01-01');
        expect(instance.year()).toBe(2023);
      });

      test('TC108: 测试 Dayjs.year(int) setter', () => {
        const instance = dayjs('2023-01-01');
        const result = instance.year(2024);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2024-01-01' });
      });

      test('TC109: 测试 Dayjs.month() getter', () => {
        const instance = dayjs('2023-01-01');
        expect(instance.month()).toBe(0); // January is 0
      });

      test('TC110: 测试 Dayjs.month(int) setter', () => {
        const instance = dayjs('2023-01-31');
        const result = instance.month(1); // February (0-indexed 1), which has 28 days in 2023
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-02-28' });
      });

      test('TC111: 测试 Dayjs.date() getter', () => {
        const instance = dayjs('2023-01-15');
        expect(instance.date()).toBe(15);
      });

      test('TC112: 测试 Dayjs.date(int) setter', () => {
        const instance = dayjs('2023-01-15');
        const result = instance.date(20);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-20' });
      });

      test('TC113: 测试 Dayjs.day() getter (day of week)', () => {
        const instance = dayjs('2023-01-15'); // Sunday
        expect(instance.day()).toBe(0);
      });

      test('TC114: 测试 Dayjs.day(int) setter (day of week)', () => {
        const instance = dayjs('2023-01-15'); // Sunday (0)
        const result = instance.day(1); // Set to Monday (1)
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-16' });
      });

      test('TC115: 测试 Dayjs.hour() getter', () => {
        const instance = dayjs('2023-01-01 10:00:00');
        expect(instance.hour()).toBe(10);
      });

      test('TC116: 测试 Dayjs.hour(int) setter', () => {
        const instance = dayjs('2023-01-01 10:00:00');
        const result = instance.hour(14);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-01 14:00:00' });
      });

      test('TC117: 测试 Dayjs.minute() getter', () => {
        const instance = dayjs('2023-01-01 10:30:00');
        expect(instance.minute()).toBe(30);
      });

      test('TC118: 测试 Dayjs.minute(int) setter', () => {
        const instance = dayjs('2023-01-01 10:30:00');
        const result = instance.minute(45);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-01 10:45:00' });
      });

      test('TC119: 测试 Dayjs.second() getter', () => {
        const instance = dayjs('2023-01-01 10:30:45');
        expect(instance.second()).toBe(45);
      });

      test('TC120: 测试 Dayjs.second(int) setter', () => {
        const instance = dayjs('2023-01-01 10:30:45');
        const result = instance.second(50);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-01 10:30:50' });
      });

      test('TC121: 测试 Dayjs.millisecond() getter', () => {
        const instance = dayjs('2023-01-01 10:30:45.123');
        expect(instance.millisecond()).toBe(123);
      });

      test('TC122: 测试 Dayjs.millisecond(int) setter', () => {
        const instance = dayjs('2023-01-01 10:30:45.123');
        const result = instance.millisecond(456);
        expect(result).toBeDayjsInstance({ $d: 'Date object for 2023-01-01 10:30:45.456' });
      });
    });
  });

  describe('dayjs.extend', () => {
    test('TC101: 测试 dayjs.extend: 首次安装插件', () => {
      const mockPlugin = jest.fn((option, DayjsClass, dayjsFunc) => {
        DayjsClass.prototype.foo = () => 'bar';
      });
      mockPlugin.$i = false; // Ensure it's not marked as installed initially

      const option = { test: true };
      dayjs.extend(mockPlugin, option);

      expect(mockPlugin).toHaveBeenCalledTimes(1);
      expect(mockPlugin).toHaveBeenCalledWith(option, expect.any(Function), dayjs);
      expect(mockPlugin.$i).toBe(true); // Should be marked as installed

      const instance = dayjs();
      expect(instance.foo()).toBe('bar'); // Check if plugin method is added
    });

    test('TC102: 测试 dayjs.extend: 再次安装已安装的插件 (不应再次调用)', () => {
      const mockPlugin = jest.fn((option, DayjsClass, dayjsFunc) => {
        DayjsClass.prototype.bar = () => 'baz';
      });
      mockPlugin.$i = true; // Mark as already installed

      const option = { test: true };
      dayjs.extend(mockPlugin, option);

      expect(mockPlugin).not.toHaveBeenCalled(); // Should not be called again
      // Verify the method is not added if it wasn't installed
      const instance = dayjs();
      expect(instance.bar).toBeUndefined();
    });
  });

  describe('dayjs.unix', () => {
    test('TC103: 测试 dayjs.unix: 将 Unix 时间戳转换为 Dayjs 实例', () => {
      const timestamp = 0; // Corresponds to 1970-01-01T00:00:00.000Z
      const d = dayjs.unix(timestamp);
      expect(d).toBeDayjsInstance({ $d: 'Date object for 1970-01-01T00:00:00.000Z' });
    });
  });
});