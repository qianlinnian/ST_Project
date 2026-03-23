const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs', () => {
  // 重置全局locale为en，确保测试独立性
  beforeEach(() => {
    index.locale('en');
  });

  // 基本日期解析测试
  test('should parse date string with empty config', () => {
    const d = index('2023-05-15 14:30:25.123', {});
    expect(d.isValid()).toBe(true);
    // 可选：检查具体日期组件
    expect(d.$y()).toBe(2023);
    expect(d.$M()).toBe(4); // 月份0-indexed，5月为4
    expect(d.$D()).toBe(15);
  });

  test('should parse date string with utc config', () => {
    const d = index('2023-05-15 14:30:25.123', { utc: true });
    expect(d.isValid()).toBe(true);
    // utc模式下，可以使用toISOString验证
    expect(d.toISOString()).toBe('2023-05-15T14:30:25.123Z');
  });

  test('should handle invalid date string', () => {
    const d = index('invalid-date', {});
    expect(d.isValid()).toBe(false);
    expect(d.format('YYYY-MM-DD')).toBe('Invalid Date');
  });

  test('should parse timestamp', () => {
    const d = index(1684123456789, {});
    expect(d.isValid()).toBe(true);
    expect(d.valueOf()).toBe(1684123456789);
  });

  // parseLocale 函数测试
  test('TC009: parseLocale with empty preset should return current global L', () => {
    const result = index.locale('', null, false);
    expect(result).toBe('en');
  });

  test('TC010: parseLocale with existing locale string', () => {
    const result = index.locale('en', null, false);
    expect(result).toBe('en');
    // 验证全局L未改变（仍为'en')
    const currentLocale = index.locale();
    expect(currentLocale).toBe('en');
  });

  test('should add new locale string and set global L', () => {
    const result = index.locale('fr', { name: 'fr' }, false);
    expect(result).toBe('fr');
    const currentLocale = index.locale();
    expect(currentLocale).toBe('fr');
  });

  test('TC012: parseLocale with hyphenated locale string', () => {
    const result = index.locale('zh-CN', null, false);
    expect(result).toBe('en'); // 递归后返回当前全局L 'en'
  });

  test('should parseLocale with locale object', () => {
    const result = index.locale({ name: 'ja' }, null, false);
    expect(result).toBe('ja');
    const currentLocale = index.locale();
    expect(currentLocale).toBe('ja');
  });

  test('TC014: parseLocale with unknown string and isLocal true', () => {
    const result = index.locale('unknown', null, true);
    expect(result).toBe(false);
    // 全局L应保持为'en'（由于beforeEach重置）
    const currentLocale = index.locale();
    expect(currentLocale).toBe('en');
  });

  // startOf 方法测试
  describe('startOf method', () => {
    const baseDate = index('2023-05-15 14:30:25.123'); // 星期一，5月15日

    test('TC021: startOf with month and isStartOf false', () => {
      const result = baseDate.startOf('month', false);
      expect(result.$D()).toBe(31); // 5月最后一天
      expect(result.$H()).toBe(23);
      expect(result.$m()).toBe(59);
      expect(result.$s()).toBe(59);
      expect(result.$ms()).toBe(999);
    });

    test('TC022: startOf with week', () => {
      const result = baseDate.startOf('week');
      expect(result.$D()).toBe(14); // 当周第一天为5月14日（星期日）
      expect(result.$H()).toBe(0);
      expect(result.$m()).toBe(0);
      expect(result.$s()).toBe(0);
      expect(result.$ms()).toBe(0);
    });

    test('TC023: startOf with day', () => {
      const result = baseDate.startOf('day');
      expect(result.$D()).toBe(15);
      expect(result.$H()).toBe(0);
      expect(result.$m()).toBe(0);
      expect(result.$s()).toBe(0);
      expect(result.$ms()).toBe(0);
    });

    test('TC024: startOf with hour', () => {
      const result = baseDate.startOf('hour');
      expect(result.$H()).toBe(14);
      expect(result.$m()).toBe(0);
      expect(result.$s()).toBe(0);
      expect(result.$ms()).toBe(0);
    });

    test('TC025: startOf with minute', () => {
      const result = baseDate.startOf('minute');
      expect(result.$m()).toBe(30);
      expect(result.$s()).toBe(0);
      expect(result.$ms()).toBe(0);
    });

    test('TC026: startOf with second', () => {
      const result = baseDate.startOf('second');
      expect(result.$s()).toBe(25);
      expect(result.$ms()).toBe(0);
    });

    test('TC027: startOf with invalid units returns clone', () => {
      const result = baseDate.startOf('invalid');
      expect(result.valueOf()).toBe(baseDate.valueOf());
    });
  });

  // add 方法测试
  describe('add method', () => {
    const baseDate = index('2023-05-15 14:30:25.123');

    test('TC028: add months', () => {
      const result = baseDate.add(2, 'month');
      expect(result.$M()).toBe(6); // 5月(4) + 2 = 6月(6)
      expect(result.$D()).toBe(15); // 日期不变
      expect(result.$H()).toBe(14);
      expect(result.$m()).toBe(30);
    });

    test('TC029: add years', () => {
      const result = baseDate.add(1, 'year');
      expect(result.$y()).toBe(2024);
      expect(result.$M()).toBe(4);
      expect(result.$D()).toBe(15);
    });

    test('TC030: add days', () => {
      const result = baseDate.add(3, 'day');
      expect(result.$D()).toBe(18); // 5月15日 + 3天 = 5月18日
      expect(result.$H()).toBe(14);
      expect(result.$m()).toBe(30);
    });

    test('TC031: add weeks', () => {
      const result = baseDate.add(2, 'week');
      expect(result.$D()).toBe(29); // 5月15日 + 2周 = 5月29日
      expect(result.$H()).toBe(14);
      expect(result.$m()).toBe(30);
    });

    test('TC032: add hours', () => {
      const result = baseDate.add(5, 'hour');
      expect(result.$H()).toBe(19); // 14 + 5 = 19
      expect(result.$m()).toBe(30);
    });
  });

  // format 方法测试
  describe('format method', () => {
    test('TC033: format with invalid date', () => {
      const d = index('invalid-date');
      const result = d.format('YYYY-MM-DD');
      expect(result).toBe('Invalid Date');
    });

    test('TC035: format with all tokens', () => {
      // 使用utc模式避免时区差异
      const d = index('2023-05-15 14:30:25.123', { utc: true });
      const formatStr = "YYYY-YY-M-MM-MMM-MMMM-D-DD-d-dd-ddd-dddd-H-HH-h-hh-a-A-m-mm-s-ss-SSS-Z";
      const result = d.format(formatStr);
      // 基于UTC时间2023-05-15 14:30:25.123，locale为en
      const expected = "2023-23-5-05-May-May-15-15-1-Mo-Mon-Monday-14-14-2-02-pm-PM-30-30-25-25-123-Z";
      expect(result).toBe(expected);
    });
  });

  // 静态方法测试
  test('TC039: dayjs.unix', () => {
    const timestamp = 1672531200; // 对应2023-01-01 00:00:00 UTC
    const d = index.unix(timestamp);
    expect(d.unix()).toBe(timestamp);
    expect(d.valueOf()).toBe(timestamp * 1000);
  });

  // 原型getter/setter测试
  describe('prototype getters and setters', () => {
    const baseDate = index('2023-05-15 14:30:25.123');

    test('TC040: $D getter', () => {
      expect(baseDate.$D()).toBe(15);
    });

    test('TC041: $M setter', () => {
      const result = baseDate.$M(5);
      expect(result.$M()).toBe(5); // 设置为5，即6月
      // 原对象未改变
      expect(baseDate.$M()).toBe(4); // 原月份为4（5月）
    });
  });

test('补充: parseDate 应处理 null 输入', () => {
    const result = index(null).$d;
    expect(result.toString()).toBe('Invalid Date');
  });

  test('补充: parseDate 应处理 undefined 输入', () => {
    const result = index().isValid();
    expect(result).toBe(true);
  });

  test('补充: parseDate 应处理带 Z 结尾的字符串', () => {
    const dateStr = '2023-01-01T00:00:00Z';
    const result = index(dateStr).isValid();
    expect(result).toBe(true);
  });

  test('补充: $utils 方法应返回 Utils 对象', () => {
    const utils = index('2023-01-01').$utils();
    expect(typeof utils.u).toBe('function');
  });

  test('补充: isSame 方法应正确处理不同单位的时间比较', () => {
    const d1 = index('2023-01-01 10:30:00');
    const d2 = index('2023-01-01 10:30:59');
    const result = d1.isSame(d2, 'hour');
    expect(result).toBe(true);
  });

  test('补充: isAfter 方法应返回 true 当时间在比较对象之后', () => {
    const d1 = index('2023-01-02');
    const d2 = index('2023-01-01');
    const result = d1.isAfter(d2, 'day');
    expect(result).toBe(true);
  });

  test('补充: isBefore 方法应返回 true 当时间在比较对象之前', () => {
    const d1 = index('2023-01-01');
    const d2 = index('2023-01-02');
    const result = d1.isBefore(d2, 'day');
    expect(result).toBe(true);
  });

  test('补充: get 方法应通过 Utils.p 获取属性值', () => {
    const result = index('2023-06-15').get('month');
    expect(result).toBe(5);
  });

  test('补充: subtract 方法应正确减去时间', () => {
    const d1 = index('2023-01-02');
    const d2 = d1.subtract(1, 'day');
    expect(d2.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  test('补充: format 方法应处理未知匹配符并返回 null', () => {
    // 假设 'X' 是未定义的格式符，应触发 default 分支并返回 null，最终被原样输出
    const formatted = index('2023-01-01').format('YYYY-MM-DD [X]');
    expect(formatted).toContain('X');
  });

  test('补充: diff 方法应计算年、月、季度差，不取整', () => {
    const d1 = index('2023-06-15');
    const d2 = index('2022-02-10');
    const yearDiff = d1.diff(d2, 'year', true);
    expect(yearDiff).toBeGreaterThan(1);
    const monthDiff = d1.diff(d2, 'month', true);
    expect(monthDiff).toBeGreaterThan(16);
    const quarterDiff = d1.diff(d2, 'quarter', true);
    expect(quarterDiff).toBeGreaterThan(5);
  });

  test('补充: diff 方法应计算周、日、时、分、秒差', () => {
    const d1 = index('2023-01-08');
    const d2 = index('2023-01-01');
    const weekDiff = d1.diff(d2, 'week');
    expect(weekDiff).toBe(1);
    const dayDiff = d1.diff(d2, 'day');
    expect(dayDiff).toBe(7);
    const hourDiff = d1.diff(index('2023-01-01 00:00:00'), 'hour');
    expect(hourDiff).toBe(24 * 7);
    const minuteDiff = d1.diff(d2, 'minute');
    expect(minuteDiff).toBe(7 * 24 * 60);
    const secondDiff = d1.diff(d2, 'second');
    expect(secondDiff).toBe(7 * 24 * 60 * 60);
  });

  test('补充: diff 方法默认返回毫秒差且可浮点', () => {
    const d1 = index('2023-01-01 00:00:00.500');
    const d2 = index('2023-01-01 00:00:00.000');
    const msDiffFloat = d1.diff(d2, null, true);
    expect(msDiffFloat).toBe(500);
    const msDiffInt = d1.diff(d2);
    expect(msDiffInt).toBe(500);
  });

  test('补充: locale 方法不传参应返回当前语言', () => {
    const d = index('2023-01-01');
    const locale = d.locale();
    expect(locale).toBeDefined();
  });

  test('补充: locale 方法传参应更新语言并返回新实例', () => {
    const d1 = index('2023-01-01');
    const d2 = d1.locale('zh-cn');
    expect(d2.$L).toBe('zh-cn');
    expect(d2).not.toBe(d1);
  });

  test('补充: toJSON 方法对无效日期应返回 null', () => {
    const d = index(new Date(NaN));
    const json = d.toJSON();
    expect(json).toBeNull();
  });

  test('补充: toString 应返回 UTC 字符串', () => {
    const d = index('2023-01-01');
    const str = d.toString();
    expect(str).toMatch(/GMT$/);
  });

  test('补充: dayjs.extend 应安装插件且仅一次', () => {
    let installCount = 0;
    const mockPlugin = (option, Dayjs, dayjsFn) => {
      installCount += 1;
    };
    mockPlugin.$i = undefined;
    dayjs.extend(mockPlugin);
    expect(installCount).toBe(1);
    expect(mockPlugin.$i).toBe(true);
    dayjs.extend(mockPlugin);
    expect(installCount).toBe(1);
  });
});