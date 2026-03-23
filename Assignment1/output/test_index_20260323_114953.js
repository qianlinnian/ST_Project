```javascript
const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 测试套件', () => {
  // 辅助函数：获取日期字符串（用于比较）
  const getDateString = (dayjsObj) => dayjsObj.toISOString();

  describe('dayjs 函数', () => {
    test('TC002: 测试dayjs函数传入非对象配置参数', () => {
      const result = index('2023-01-01', null);
      expect(result).toBeDefined();
      expect(result[IS_DAYJS]).toBe(true);
    });
  });

  describe('parseLocale 函数', () => {
    test('TC003: 测试parseLocale函数传入空preset', () => {
      const result = index.parseLocale(null, null, false);
      expect(result).toBe('en'); // 默认全局locale是'en'
    });

    test('TC004: 测试parseLocale函数传入字符串preset且Ls中存在', () => {
      const result = index.parseLocale('en', null, false);
      expect(result).toBe('en');
    });

    test('TC005: 测试parseLocale函数传入字符串preset且Ls中不存在，但有object参数', () => {
      const localeObj = { name: 'fr' };
      const result = index.parseLocale('fr', localeObj, false);
      expect(result).toBe('fr');
      expect(index.Ls.fr).toBe(localeObj);
    });

    test('TC006: 测试parseLocale函数传入字符串preset带连字符且无对应locale', () => {
      const result = index.parseLocale('zh-CN', null, false);
      expect(result).toBe('zh'); // 递归调用parseLocale('zh')
    });

    test('TC007: 测试parseLocale函数传入对象preset', () => {
      const localeObj = { name: 'ja' };
      const result = index.parseLocale(localeObj, null, false);
      expect(result).toBe('ja');
      expect(index.Ls.ja).toBe(localeObj);
    });

    test('TC008: 测试parseLocale函数isLocal为true', () => {
      const localeObj = { name: 'de' };
      const result = index.parseLocale('de', localeObj, true);
      expect(result).toBe('de');
      // isLocal为true，全局L不应改变
      expect(index.L).toBe('en');
    });
  });

  describe('parseDate 函数', () => {
    test('TC009: 测试parseDate函数date为null', () => {
      const cfg = { date: null, utc: false };
      const result = parseDate(cfg);
      expect(result.toString()).toBe('Invalid Date');
    });

    test('TC010: 测试parseDate函数date为有效字符串且utc为false', () => {
      const cfg = { date: '2023-01-01 12:00:00.123', utc: false };
      const result = parseDate(cfg);
      expect(result.getFullYear()).toBe(2023);
      expect(result.getMonth()).toBe(0); // 0-based
      expect(result.getDate()).toBe(1);
    });

    test('TC011: 测试parseDate函数date为有效字符串且utc为true', () => {
      const cfg = { date: '2023-01-01 12:00:00.123', utc: true };
      const result = parseDate(cfg);
      expect(result.getUTCFullYear()).toBe(2023);
      expect(result.getUTCMonth()).toBe(0);
      expect(result.getUTCDate()).toBe(1);
    });

    test('TC012: 测试parseDate函数date为无效字符串', () => {
      const cfg = { date: 'invalid', utc: false };
      const result = parseDate(cfg);
      expect(result.toString()).toBe('Invalid Date');
    });

    test('TC013: 测试parseDate函数date以Z结尾', () => {
      const cfg = { date: '2023-01-01T12:00:00Z', utc: false };
      const result = parseDate(cfg);
      // 直接通过new Date(date)解析
      expect(result.toISOString()).toBe('2023-01-01T12:00:00.000Z');
    });

    test('TC_SUP_002: 测试 parseDate 函数中 utc 为 true 且日期字符串包含时区信息的情况', () => {
      const cfg = { date: '2023-01-15T10:30:00Z', utc: true };
      const result = parseDate(cfg);
      // 注意：以Z结尾的字符串不会匹配REGEX_PARSE，会走最后的new Date(date)
      expect(result.toISOString()).toBe('2023-01-15T10:30:00.000Z');
    });

    test('TC_SUP_023: 测试 parseDate() 中 UTC 日期解析的分支条件', () => {
      const cfg = { date: '2023-01-01T00:00:00', utc: true };
      const result = parseDate(cfg);
      // 字符串不含Z，会匹配REGEX_PARSE
      expect(result.getUTCFullYear()).toBe(2023);
      expect(result.getUTCMonth()).toBe(0);
    });
  });

  describe('Dayjs 构造函数', () => {
    test('TC014: 测试Dayjs构造函数', () => {
      const cfg = { locale: 'en', date: '2023-01-01', x: {} };
      const dayjsObj = new Dayjs(cfg);
      expect(dayjsObj.$L).toBe('en');
      expect(dayjsObj.$x).toEqual({});
      expect(dayjsObj[IS_DAYJS]).toBe(true);
    });
  });

  describe('isValid 方法', () => {
    test('TC017: 测试isValid方法返回true', () => {
      const dayjsObj = index('2023-01-01');
      expect(dayjsObj.isValid()).toBe(true);
    });

    test('TC018: 测试isValid方法返回false', () => {
      const dayjsObj = index('invalid');
      expect(dayjsObj.isValid()).toBe(false);
    });
  });

  describe('isSame/isAfter/isBefore 方法', () => {
    test('TC019: 测试isSame方法相同日期', () => {
      const dayjsObj = index('2023-01-01');
      expect(dayjsObj.isSame('2023-01-01', 'day')).toBe(true);
    });

    test('TC020: 测试isAfter方法', () => {
      const dayjsObj = index('2023-01-01');
      expect(dayjsObj.isAfter('2023-01-01', 'day')).toBe(false);
    });

    test('TC021: 测试isBefore方法', () => {
      const dayjsObj = index('2023-01-01');
      expect(dayjsObj.isBefore('2023-01-01', 'day')).toBe(false);
    });
  });

  describe('$g 方法', () => {
    test('TC022: 测试$g方法无input参数', () => {
      const dayjsObj = index('2023-01-01');
      const result = dayjsObj.$g(undefined, '$y', 'year');
      expect(result).toBe(2023);
    });

    test('TC023: 测试$g方法有input参数', () => {
      const dayjsObj = index('2023-01-01');
      const result = dayjsObj.$g(2024, '$y', 'year');
      expect(result.$y).toBe(2024);
    });
  });

  describe('startOf/endOf 方法', () => {
    const baseDate = index('2023-06-15T14:30:45.123'); // 2023年6月15日 星期四

    test('TC024: 测试startOf方法Y单位', () => {
      const result = baseDate.startOf('year');
      expect(result.toISOString()).toBe('2023-01-01T00:00:00.000Z');
    });

    test('TC025: 测试startOf方法Y单位endOf模式', () => {
      const result = baseDate.endOf('year');
      expect(result.toISOString()).toBe('2023-12-31T23:59:59.999Z');
    });

    test('TC026: 测试startOf方法M单位', () => {
      const result = baseDate.startOf('month');
      expect(result.toISOString()).toBe('2023-06-01T00:00:00.000Z');
    });

    test('TC027: 测试startOf方法W单位', () => {
      const result = baseDate.startOf('week');
      // 2023-06-15是星期四，假设周一开始（默认）
      expect(result.toISOString()).toBe('2023-06-12T00:00:00.000Z');
    });

    test('TC028: 测试startOf方法D单位', () => {
      const result = baseDate.startOf('day');
      expect(result.toISOString()).toBe('2023-06-15T00:00:00.000Z');
    });

    test('TC029: 测试startOf方法H单位', () => {
      const result = baseDate.startOf('hour');
      expect(result.toISOString()).toBe('2023-06-15T14:00:00.000Z');
    });

    test('TC030: 测试startOf方法MIN单位', () => {
      const result = baseDate.startOf('minute');
      expect(result.toISOString()).toBe('2023-06-15T14:30:00.000Z');
    });

    test('TC031: 测试startOf方法S单位', () => {
      const result = baseDate.startOf('second');
      expect(result.toISOString()).toBe('2023-06-15T14:30:45.000Z');
    });

    test('TC032: 测试startOf方法无效单位', () => {
      const result = baseDate.startOf('invalid');
      expect(result.toISOString()).toBe(baseDate.toISOString());
    });

    test('TC_SUP_024: 测试 startOf() 中 weekStart 逻辑（$W < weekStart）', () => {
      // 模拟locale的weekStart为1（周一）
      const originalLocale = index.Ls.en;
      index.Ls.en = { ...originalLocale, weekStart: 1 };
      const dayjsObj = index('2023-01-01'); // 2023-01-01是周日(0)
      const result = dayjsObj.startOf('week');
      // 周日(0) < 周一(1)，所以gap = (0+7)-1 = 6，$D - gap = 1-6 = -5，即前一周的周一
      expect(result.toISOString()).toBe('2022-12-26T00:00:00.000Z');
      index.Ls.en = originalLocale; // 恢复
    });
  });

  describe('$set/set 方法', () => {
    test('TC033: 测试$set方法D单位', () => {
      const dayjsObj = index('2023-01-01');
      dayjsObj.$set('date', 15);
      expect(dayjsObj.$D).toBe(15);
    });

    test('TC034: 测试$set方法M单位', () => {
      const dayjsObj = index('2023-01-31');
      dayjsObj.$set('month', 5); // 设置为6月（0-based）
      expect(dayjsObj.$M).toBe(5);
      // 1月31日设置为6月，因为6月只有30天，日期会调整为30
      expect(dayjsObj.$D).toBe(30);
    });

    test('TC035: 测试$set方法Y单位', () => {
      const dayjsObj = index('2023-01-31');
      dayjsObj.$set('year', 2024);
      expect(dayjsObj.$y).toBe(2024);
    });

    test('TC_SUP_025: 测试 $set() 中月份设置的特殊逻辑', () => {
      const dayjsObj = index('2023-01-31');
      dayjsObj.$set('month', 1); // 设置为2月
      // 2023年2月只有28天
      expect(dayjsObj.toISOString()).toBe('2023-02-28T00:00:00.000Z');
    });
  });

  describe('add/subtract 方法', () => {
    test('TC036: 测试add方法M单位', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.add(1, 'month');
      expect(result.$M).toBe(1); // 2月
    });

    test('TC037: 测试add方法Y单位', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.add(1, 'year');
      expect(result.$y).toBe(2024);
    });

    test('TC038: 测试add方法D单位', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.add(1, 'day');
      expect(result.$D).toBe(16);
    });

    test('TC039: 测试add方法W单位', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.add(1, 'week');
      expect(result.$D).toBe(22);
    });

    test('TC040: 测试add方法MIN单位', () => {
      const dayjsObj = index('2023-01-15T10:00:00');
      const result = dayjsObj.add(30, 'minute');
      expect(result.$H).toBe(10);
      expect(result.$m).toBe(30);
    });

    test('TC041: 测试add方法无效单位', () => {
      const dayjsObj = index('2023-01-15T10:00:00.000');
      const result = dayjsObj.add(1, 'invalid');
      // 默认step=1毫秒
      expect(result.valueOf() - dayjsObj.valueOf()).toBe(1);
    });

    test('TC_SUP_006: 测试 subtract 方法', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.subtract(5, 'day');
      expect(result.format('YYYY-MM-DD')).toBe('2023-01-10');
    });
  });

  describe('format 方法', () => {
    test('TC042: 测试format方法默认格式', () => {
      const dayjsObj = index('2023-01-15T10:30:45.123');
      const result = dayjsObj.format();
      expect(result).toBe('2023-01-15T10:30:45+00:00');
    });

    test('TC_SUP_007: 测试 format 方法中无效日期的情况', () => {
      const dayjsObj = index('invalid date');
      const result = dayjsObj.format('YYYY-MM-DD');
      expect(result).toBe('Invalid Date');
    });

    test('TC_SUP_008: 测试 format 方法中 getShort 函数的 arr 参数为 null 的情况', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.format('MMM');
      expect(result).toBe('Jan');
    });

    test('TC_SUP_009: 测试 format 方法中 get$H 函数', () => {
      const dayjsObj = index('2023-01-15T00:30:00');
      const result = dayjsObj.format('h');
      expect(result).toBe('12');
    });

    test('TC_SUP_010: 测试 format 方法中 meridiem 函数的小时小于12的情况', () => {
      const dayjsObj = index('2023-01-15T10:30:00');
      const result = dayjsObj.format('a');
      expect(result).toBe('am');
    });

    test('TC_SUP_011: 测试 format 方法中各种格式符', () => {
      const dayjsObj = index('2023-01-15T10:30:45.123');
      const result = dayjsObj.format('YY YYYY M MM MMM MMMM D DD d dd ddd dddd H HH h hh a A m mm s ss SSS Z');
      // 注意时区可能不同，这里只检查部分
      expect(result).toContain('23 2023 1 01 Jan January 15 15 0 Su Sun Sunday 10 10 10 10 am AM 30 30 45 45 123');
    });

    test('TC_SUP_001: 测试 format("MMMM") 月份全称格式化', () => {
      const dayjsObj = index('2023-01-15');
      const result = dayjsObj.format('MMMM');
      expect(result).toBe('January');
    });

    test('TC_SUP_002: 测试 format("D") 日期格式化（无前导零）', () => {
      const dayjsObj = index('2023-01-05');
      const result = dayjsObj.format('D');
      expect(result).toBe('5');
    });

    test('TC_SUP_003: 测试 format("d") 星期几格式化（数字）', () => {
      const dayjsObj = index('2023-01-01');
      const result = dayjsObj.format('d');
      expect(result).toBe('0');
    });

    test('TC_SUP_004: 测试 format("dd") 星期几缩写格式化', () => {
      const dayjsObj = index('2023-01-01');
      const result = dayjsObj.format('dd');
      expect(result).toBe('Su');
    });

    test('TC_SUP_005: 测试 format("ddd") 星期几短名称格式化', () => {
      const dayjsObj = index('2023-01-01');
      const result = dayjsObj.format('ddd');
      expect(result).toBe('Sun');
    });

    test('TC_SUP_006: 测试 format("dddd") 星期几全称格式化', () => {
      const