const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 白盒测试', () => {
  // 辅助函数：检查是否为 Dayjs 对象
  const isDayjsObject = (obj) => obj && obj.$isDayjsObject === true;

  describe('dayjs 函数', () => {
    test('TC002: 测试dayjs函数传入非对象配置', () => {
      const { date, c } = { date: '2023-01-01', c: 'invalid' };
      const result = index(date, c);
      expect(isDayjsObject(result)).toBe(true);
      expect(result.isValid()).toBe(true);
    });
  });

  describe('parseLocale 函数', () => {
    test('TC003: 测试parseLocale函数传入空preset', () => {
      const { preset, object, isLocal } = { preset: null, object: null, isLocal: false };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('en'); // L 的初始值
    });

    test('TC004: 测试parseLocale函数传入字符串preset且Ls中存在', () => {
      const { preset, object, isLocal } = { preset: 'en', object: null, isLocal: false };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('en');
    });

    test('TC005: 测试parseLocale函数传入字符串preset且Ls中不存在，但有object', () => {
      const { preset, object, isLocal } = { preset: 'fr', object: { name: 'fr' }, isLocal: false };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('fr');
      expect(index.Ls.fr).toEqual({ name: 'fr' });
    });

    test('TC006: 测试parseLocale函数传入字符串preset带连字符且Ls中不存在', () => {
      const { preset, object, isLocal } = { preset: 'en-US', object: null, isLocal: false };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('en');
    });

    test('TC007: 测试parseLocale函数传入对象preset', () => {
      const { preset, object, isLocal } = { preset: { name: 'zh-cn' }, object: null, isLocal: false };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('zh-cn');
      expect(index.Ls['zh-cn']).toEqual({ name: 'zh-cn' });
    });

    test('TC008: 测试parseLocale函数传入字符串preset且Ls中不存在，有object，且isLocal为true', () => {
      const { preset, object, isLocal } = { preset: 'fr', object: { name: 'fr' }, isLocal: true };
      const result = index.locale(preset, object, isLocal);
      expect(result).toBe('fr');
      expect(index.Ls.fr).toEqual({ name: 'fr' });
      expect(index.locale()).toBe('en'); // 全局 L 应仍为 'en'
    });
  });

  describe('parseDate 函数', () => {
    const parseDate = (cfg) => {
      const dayjsInstance = index(cfg.date, cfg);
      return dayjsInstance.$d;
    };

    test('TC009: 测试parseDate函数传入null', () => {
      const { cfg } = { cfg: { date: null, utc: false } };
      const result = parseDate(cfg);
      expect(isNaN(result.getTime())).toBe(true);
    });

    test('TC010: 测试parseDate函数传入有效日期字符串，utc为false', () => {
      const { cfg } = { cfg: { date: '2023-01-01 12:00:00', utc: false } };
      const result = parseDate(cfg);
      expect(result.getFullYear()).toBe(2023);
      expect(result.getMonth()).toBe(0);
      expect(result.getDate()).toBe(1);
      expect(result.getHours()).toBe(12);
    });

    test('TC011: 测试parseDate函数传入有效日期字符串，utc为true', () => {
      const { cfg } = { cfg: { date: '2023-01-01 12:00:00', utc: true } };
      const result = parseDate(cfg);
      expect(result.getUTCFullYear()).toBe(2023);
      expect(result.getUTCMonth()).toBe(0);
      expect(result.getUTCDate()).toBe(1);
      expect(result.getUTCHours()).toBe(12);
    });

    test('TC012: 测试parseDate函数传入无效日期字符串', () => {
      const { cfg } = { cfg: { date: 'invalid', utc: false } };
      const result = parseDate(cfg);
      expect(isNaN(result.getTime())).toBe(true);
    });

    test('TC013: 测试parseDate函数传入带Z的日期字符串', () => {
      const { cfg } = { cfg: { date: '2023-01-01T12:00:00Z', utc: false } };
      const result = parseDate(cfg);
      expect(result.toISOString()).toBe('2023-01-01T12:00:00.000Z');
    });
  });

  describe('Dayjs 构造函数', () => {
    test('TC014: 测试Dayjs构造函数传入locale和x', () => {
      const { locale, date, x } = { locale: 'en', date: '2023-01-01', x: {} };
      const result = index(date, { locale, x });
      expect(result.$L).toBe('en');
      expect(result.$x).toEqual({});
      expect(result.isValid()).toBe(true);
    });
  });

  describe('isValid 方法', () => {
    test('TC017: 测试isValid方法返回true', () => {
      const { date } = { date: '2023-01-01' };
      const result = index(date);
      expect(result.isValid()).toBe(true);
    });

    test('TC018: 测试isValid方法返回false', () => {
      const { date } = { date: 'invalid' };
      const result = index(date);
      expect(result.isValid()).toBe(false);
    });
  });

  describe('isSame 方法', () => {
    test('TC019: 测试isSame方法相同日期', () => {
      const { that, units } = { that: '2023-01-01', units: 'day' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.isSame(that, units);
      expect(result).toBe(true);
    });

    test('TC020: 测试isSame方法不同日期', () => {
      const { that, units } = { that: '2023-01-02', units: 'day' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.isSame(that, units);
      expect(result).toBe(false);
    });
  });

  describe('isAfter 方法', () => {
    test('TC021: 测试isAfter方法', () => {
      const { that, units } = { that: '2023-01-01', units: 'day' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.isAfter(that, units);
      expect(result).toBe(false);
    });
  });

  describe('isBefore 方法', () => {
    test('TC022: 测试isBefore方法', () => {
      const { that, units } = { that: '2023-01-02', units: 'day' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.isBefore(that, units);
      expect(result).toBe(true);
    });
  });

  describe('$g 方法', () => {
    test('TC023: 测试$g方法无input参数', () => {
      const { input, get, set } = { input: undefined, get: '$y', set: 'year' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.$g(input, get, set);
      expect(result).toBe(2023);
    });

    test('TC024: 测试$g方法有input参数', () => {
      const { input, get, set } = { input: 2024, get: '$y', set: 'year' };
      const dayjsInstance = index('2023-01-01');
      const result = dayjsInstance.$g(input, get, set);
      expect(isDayjsObject(result)).toBe(true);
      expect(result.year()).toBe(2024);
    });
  });

  describe('unix 方法', () => {
    test('TC025: 测试unix方法', () => {
      const { date } = { date: '2023-01-01T00:00:00Z' };
      const dayjsInstance = index(date);
      const result = dayjsInstance.unix();
      expect(result).toBe(1672531200);
    });
  });

  describe('startOf 方法', () => {
    const baseDate = index('2023-06-15T14:30:45.123');

    test('TC026: 测试startOf方法units为Y且isStartOf为true', () => {
      const { units, startOf } = { units: 'year', startOf: true };
      const result = baseDate.startOf(units, startOf);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-01-01 00:00:00.000');
    });

    test('TC027: 测试startOf方法units为Y且isStartOf为false', () => {
      const { units, startOf } = { units: 'year', startOf: false };
      const result = baseDate.startOf(units, startOf);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-12-31 23:59:59.999');
    });

    test('TC028: 测试startOf方法units为M', () => {
      const { units } = { units: 'month' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-01 00:00:00.000');
    });

    test('TC029: 测试startOf方法units为W', () => {
      const { units } = { units: 'week' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD')).toBe('2023-06-11'); // 假设周一开始
    });

    test('TC030: 测试startOf方法units为D', () => {
      const { units } = { units: 'day' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-15 00:00:00.000');
    });

    test('TC031: 测试startOf方法units为H', () => {
      const { units } = { units: 'hour' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-15 14:00:00.000');
    });

    test('TC032: 测试startOf方法units为MIN', () => {
      const { units } = { units: 'minute' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-15 14:30:00.000');
    });

    test('TC033: 测试startOf方法units为S', () => {
      const { units } = { units: 'second' };
      const result = baseDate.startOf(units);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-15 14:30:45.000');
    });

    test('TC034: 测试startOf方法units无效', () => {
      const { units } = { units: 'invalid' };
      const result = baseDate.startOf(units);
      expect(result.valueOf()).toBe(baseDate.valueOf());
    });
  });

  describe('endOf 方法', () => {
    test('TC035: 测试endOf方法', () => {
      const { arg } = { arg: 'year' };
      const baseDate = index('2023-06-15');
      const result = baseDate.endOf(arg);
      expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-12-31 23:59:59.999');
    });
  });

  describe('$set 方法', () => {
    const baseDate = index('2023-06-15T14:30:45.123');

    test('TC036: 测试$set方法units为D', () => {
      const { units, int } = { units: 'date', int: 15 };
      const result = baseDate.$set(units, int);
      expect(result.date()).toBe(15);
    });

    test('TC037: 测试$set方法units为M', () => {
      const { units, int } = { units: 'month', int: 5 };
      const result = baseDate.$set(units, int);
      expect(result.month()).toBe(5);
    });

    test('TC038: 测试$set方法units为Y', () => {
      const { units, int } = { units: 'year', int: 2024 };
      const result = baseDate.$set(units, int);
      expect(result.year()).toBe(2024);
    });

    test('TC039: 测试$set方法units无效', () => {
      const { units, int } = { units: 'invalid', int: 1 };
      const result = baseDate.$set(units, int);
      expect(result.valueOf()).toBe(baseDate.valueOf());
    });
  });

  describe('set 方法', () => {
    test('TC040: 测试set方法', () => {
      const { string, int } = { string: 'year', int: 2024 };
      const baseDate = index('2023-01-01');
      const result = baseDate.set(string, int);
      expect(isDayjsObject(result)).toBe(true);
      expect(result.year()).toBe(2024);
      expect(baseDate.year()).toBe(2023); // 原对象不应改变
    });
  });

  describe('get 方法', () => {
    test('TC041: 测试get方法', () => {
      const { unit } = { unit: 'year' };
      const baseDate = index('2023-01-01');
      const result = baseDate.get(unit);
      expect(result).toBe(2023);
    });
  });

  describe('add 方法', () => {
    const baseDate = index('2023-01-01');

    test('TC042: 测试add方法units为M', () => {
      const { number, units } = { number: 1, units: 'month' };
      const result = baseDate.add(number, units);
      expect(result.month()).toBe(1);
    });

    test('TC043: 测试add方法units为Y', () => {
      const { number, units } = { number: 1, units: 'year' };
      const result = baseDate.add(number, units);
      expect(result.year()).toBe(2024);
    });
  });

test('补充: dayjs传入Dayjs实例应返回克隆对象', () => {
    const original = dayjs('2023-01-01');
    const cloned = dayjs(original);
    expect(cloned).not.toBe(original);
    expect(cloned.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  test('补充: parseDate传入null应返回无效Date', () => {
    const cfg = { date: null };
    const result = parseDate(cfg);
    expect(result.getTime()).toBeNaN();
  });

  test('补充: parseDate传入undefined应返回当前日期', () => {
    const cfg = { date: undefined };
    const result = parseDate(cfg);
    expect(result).toBeInstanceOf(Date);
  });

  test('补充: $utils方法应返回Utils对象', () => {
    const instance = dayjs('2023-01-01');
    const utils = instance.$utils();
    expect(utils).toBe(Utils);
  });

  test('补充: add方法处理天(D)单位', () => {
    const instance = dayjs('2023-01-01');
    const result = instance.add(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-06');
  });

  test('补充: add方法处理周(W)单位', () => {
    const instance = dayjs('2023-01-01');
    const result = instance.add(2, 'week');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-15');
  });

  test('补充: add方法处理分钟(MIN)单位', () => {
    const instance = dayjs('2023-01-01T10:00:00');
    const result = instance.add(30, 'minute');
    expect(result.format('HH:mm')).toBe('10:30');
  });

  test('补充: subtract方法应正确减去时间', () => {
    const instance = dayjs('2023-01-10');
    const result = instance.subtract(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-05');
  });

  test('补充: format在无效日期时返回无效字符串', () => {
    const instance = dayjs(new Date(NaN));
    const result = instance.format('YYYY-MM-DD');
    expect(result).toBe('Invalid Date');
  });

  test('补充: format使用自定义格式字符串', () => {
    const instance = dayjs('2023-06-15T14:30:45');
    const result = instance.format('YYYY/MM/DD HH:mm:ss');
    expect(result).toBe('2023/06/15 14:30:45');
  });

  test('补充: format处理12小时制(h)和上午(AM)', () => {
    const instance = dayjs('2023-06-15T09:30:00');
    const result = instance.format('h:mm A');
    expect(result).toBe('9:30 AM');
  });

  test('补充: diff方法计算月份差', () => {
    const instance1 = dayjs('2023-01-15');
    const instance2 = dayjs('2023-06-15');
    const result = instance1.diff(instance2, 'month');
    expect(result).toBe(-5);
  });

  test('补充: locale方法无参数返回当前locale', () => {
    const instance = dayjs('2023-01-01');
    const locale = instance.locale();
    expect(locale).toBeDefined();
  });

  test('补充: toJSON在无效日期时返回null', () => {
    const instance = dayjs(new Date(NaN));
    const result = instance.toJSON();
    expect(result).toBeNull();
  });

  test('补充: dayjs.extend应安装插件', () => {
    let pluginCalled = false;
    const mockPlugin = (option, Dayjs, dayjs) => {
      pluginCalled = true;
    };
    mockPlugin.$i = undefined;
    
    dayjs.extend(mockPlugin, {});
    expect(pluginCalled).toBe(true);
    expect(mockPlugin.$i).toBe(true);
  });

  test('补充: dayjs.unix处理时间戳', () => {
    const timestamp = 1672531200; // 2023-01-01 00:00:00 UTC
    const result = dayjs.unix(timestamp);
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

test('补充: dayjs传入Dayjs实例应返回克隆', () => {
    const original = dayjs('2023-01-01');
    const cloned = dayjs(original);
    expect(cloned).not.toBe(original);
    expect(cloned.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  test('补充: parseDate传入undefined应返回当前日期', () => {
    const cfg = { date: undefined };
    const result = parseDate(cfg);
    expect(result).toBeInstanceOf(Date);
  });

  test('补充: $utils方法应返回Utils对象', () => {
    const instance = dayjs();
    const utils = instance.$utils();
    expect(utils).toBe(Utils);
  });

  test('补充: add方法处理天(D)单位', () => {
    const instance = dayjs('2023-01-01');
    const result = instance.add(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-06');
  });

  test('补充: add方法处理周(W)单位', () => {
    const instance = dayjs('2023-01-01');
    const result = instance.add(2, 'week');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-15');
  });

  test('补充: add方法处理分钟(MIN)单位', () => {
    const instance = dayjs('2023-01-01T00:00:00');
    const result = instance.add(30, 'minute');
    expect(result.format('HH:mm')).toBe('00:30');
  });

  test('补充: add方法处理小时(H)单位', () => {
    const instance = dayjs('2023-01-01T00:00:00');
    const result = instance.add(5, 'hour');
    expect(result.format('HH')).toBe('05');
  });

  test('补充: add方法处理秒(S)单位', () => {
    const instance = dayjs('2023-01-01T00:00:00');
    const result = instance.add(45, 'second');
    expect(result.format('ss')).toBe('45');
  });

  test('补充: subtract方法应调用add', () => {
    const instance = dayjs('2023-01-10');
    const result = instance.subtract(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-05');
  });

  test('补充: format在无效日期时返回无效字符串', () => {
    const instance = dayjs(new Date(NaN));
    const result = instance.format('YYYY-MM-DD');
    expect(result).toBe('Invalid Date');
  });

  test('补充: format使用自定义格式字符串', () => {
    const instance = dayjs('2023-01-01T14:30:45');
    const result = instance.format('YY-M-D ddd hh:mm A');
    expect(result).toBe('23-1-1 Sun 02:30 PM');
  });

  test('补充: diff方法计算年差', () => {
    const d1 = dayjs('2023-01-01');
    const d2 = dayjs('2020-01-01');
    const result = d1.diff(d2, 'year');
    expect(result).toBe(3);
  });

  test('补充: diff方法计算月差', () => {
    const d1 = dayjs('2023-03-01');
    const d2 = dayjs('2023-01-01');
    const result = d1.diff(d2, 'month');
    expect(result).toBe(2);
  });

  test('补充: diff方法计算季度差', () => {
    const d1 = dayjs('2023-10-01');
    const d2 = dayjs('2023-01-01');
    const result = d1.diff(d2, 'quarter');
    expect(result).toBe(3);
  });

  test('补充: locale方法无参数返回当前locale', () => {
    const instance = dayjs();
    const locale = instance.locale();
    expect(locale).toBe('en');
  });

  test('补充: toJSON在无效日期时返回null', () => {
    const instance = dayjs(new Date(NaN));
    const result = instance.toJSON();
    expect(result).toBeNull();
  });

  test('补充: toJSON在有效日期时返回ISO字符串', () => {
    const instance = dayjs('2023-01-01');
    const result = instance.toJSON();
    expect(result).toBe('2023-01-01T00:00:00.000Z');
  });

  test('补充: dayjs.unix转换时间戳', () => {
    const timestamp = 1672531200; // 2023-01-01 00:00:00 UTC
    const result = dayjs.unix(timestamp);
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  test('补充: dayjs.extend安装插件', () => {
    let pluginCalled = false;
    const mockPlugin = (option, Dayjs, dayjs) => {
      pluginCalled = true;
    };
    mockPlugin.$i = false;
    dayjs.extend(mockPlugin);
    expect(pluginCalled).toBe(true);
    expect(mockPlugin.$i).toBe(true);
  });
});