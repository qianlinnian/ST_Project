const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 白盒测试', () => {
  test('TC002: 测试dayjs函数传入null日期', () => {
    const result = index(null);
    expect(result.isValid()).toBe(false);
    expect(result.$d.toString()).toBe('Invalid Date');
  });

  test('TC005: 测试dayjs函数传入有效日期字符串（非UTC）', () => {
    const result = index('2023-01-01 12:00:00');
    expect(result.isValid()).toBe(true);
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0); // 0-based
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
  });

  test('TC006: 测试dayjs函数传入有效日期字符串（UTC）', () => {
    const result = index('2023-01-01 12:00:00', { utc: true });
    expect(result.isValid()).toBe(true);
    expect(result.$u).toBe(true);
  });

  test('TC007: 测试dayjs函数传入无效日期字符串', () => {
    const result = index('invalid-date');
    expect(result.isValid()).toBe(false);
  });

  test('TC008: 测试parseLocale传入空preset', () => {
    const result = index.locale(null);
    expect(result).toBe('en');
  });

  test('TC009: 测试parseLocale传入已加载的locale字符串', () => {
    const result = index.locale('en');
    expect(result).toBe('en');
  });

  test('TC010: 测试parseLocale传入新locale字符串和对象', () => {
    const localeObj = { name: 'fr' };
    const result = index.locale('fr', localeObj);
    expect(result).toBe('fr');
    expect(index.Ls.fr).toBe(localeObj);
  });

  test('TC011: 测试parseLocale传入带连字符的locale字符串', () => {
    const result = index.locale('en-US');
    expect(result).toBe('en');
  });

  test('TC012: 测试parseLocale传入locale对象', () => {
    const localeObj = { name: 'zh-cn' };
    const result = index.locale(localeObj);
    expect(result).toBe('zh-cn');
    expect(index.Ls['zh-cn']).toBe(localeObj);
  });

  test('TC013: 测试isValid方法对有效日期返回true', () => {
    const result = index('2023-01-01');
    expect(result.isValid()).toBe(true);
  });

  test('TC014: 测试isValid方法对无效日期返回false', () => {
    const result = index('invalid');
    expect(result.isValid()).toBe(false);
  });

  test('TC015: 测试isSame方法相同日期', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-01');
    expect(date1.isSame(date2, 'day')).toBe(true);
  });

  test('TC016: 测试isAfter方法日期在前', () => {
    const date1 = index('2023-01-02');
    const date2 = index('2023-01-01');
    expect(date1.isAfter(date2, 'day')).toBe(true);
  });

  test('TC017: 测试isBefore方法日期在后', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-02');
    expect(date1.isBefore(date2, 'day')).toBe(true);
  });

  test('TC018: 测试startOf方法对年单位', () => {
    const date = index('2023-06-15');
    const startOfYear = date.startOf('year');
    expect(startOfYear.year()).toBe(2023);
    expect(startOfYear.month()).toBe(0);
    expect(startOfYear.date()).toBe(1);
    expect(startOfYear.hour()).toBe(0);
    expect(startOfYear.minute()).toBe(0);
    expect(startOfYear.second()).toBe(0);
    expect(startOfYear.millisecond()).toBe(0);
  });

  test('TC019: 测试endOf方法对年单位', () => {
    const date = index('2023-06-15');
    const endOfYear = date.endOf('year');
    expect(endOfYear.year()).toBe(2023);
    expect(endOfYear.month()).toBe(11);
    expect(endOfYear.date()).toBe(31);
    expect(endOfYear.hour()).toBe(23);
    expect(endOfYear.minute()).toBe(59);
    expect(endOfYear.second()).toBe(59);
    expect(endOfYear.millisecond()).toBe(999);
  });

  test('TC020: 测试startOf方法对周单位（自定义周起始）', () => {
    const date = index('2023-01-05'); // 周四
    const startOfWeek = date.startOf('week');
    expect(startOfWeek.isValid()).toBe(true);
  });

  test('TC021: 测试$set方法设置月份', () => {
    const date = index('2023-01-15');
    const newDate = date.set('month', 5);
    expect(newDate.year()).toBe(2023);
    expect(newDate.month()).toBe(5);
    expect(newDate.date()).toBe(15);
  });

  test('TC022: 测试add方法添加月份', () => {
    const date = index('2023-01-31');
    const newDate = date.add(1, 'month');
    expect(newDate.year()).toBe(2023);
    expect(newDate.month()).toBe(1);
    expect(newDate.date()).toBe(28);
  });

  test('TC023: 测试add方法添加天数', () => {
    const date = index('2023-01-31');
    const newDate = date.add(1, 'day');
    expect(newDate.year()).toBe(2023);
    expect(newDate.month()).toBe(1);
    expect(newDate.date()).toBe(1);
  });

  test('TC024: 测试format方法格式化日期', () => {
    const date = index('2023-01-01 14:30:45');
    const formatted = date.format('YYYY-MM-DD HH:mm:ss');
    expect(formatted).toBe('2023-01-01 14:30:45');
  });

  test('TC025: 测试format方法无效日期', () => {
    const date = index('invalid');
    const formatted = date.format('YYYY-MM-DD');
    expect(formatted).toBe('Invalid Date');
  });

  test('TC026: 测试diff方法计算月份差', () => {
    const date1 = index('2023-06-01');
    const date2 = index('2023-01-01');
    const diff = date1.diff(date2, 'month');
    expect(diff).toBe(5);
  });

  test('TC027: 测试diff方法带float参数', () => {
    const date1 = index('2023-06-15');
    const date2 = index('2023-01-01');
    const diff = date1.diff(date2, 'month', true);
    expect(diff).toBeCloseTo(5.5, 1);
  });

  test('TC028: 测试locale方法切换locale', () => {
    const localeObj = { name: 'fr' };
    index.locale('fr', localeObj);
    const date = index('2023-01-01');
    const newDate = date.locale('fr');
    expect(newDate.$L).toBe('fr');
  });

  test('TC029: 测试clone方法', () => {
    const date = index('2023-01-01');
    const cloned = date.clone();
    expect(cloned.isValid()).toBe(true);
    expect(cloned.valueOf()).toBe(date.valueOf());
    expect(cloned).not.toBe(date);
  });

  test('TC030: 测试unix方法', () => {
    const timestamp = 1672531200;
    const date = index.unix(timestamp);
    expect(date.unix()).toBe(timestamp);
  });

  test('TC031: 测试$g方法不带input参数', () => {
    const date = index('2023-01-01');
    const year = date.year();
    expect(year).toBe(2023);
  });

  test('TC032: 测试$g方法带input参数', () => {
    const date = index('2023-01-01');
    const newDate = date.year(2024);
    expect(newDate.year()).toBe(2024);
  });

  test('TC033: 测试startOf方法默认单位', () => {
    const date = index('2023-01-01');
    const result = date.startOf();
    expect(result.valueOf()).toBe(date.valueOf());
  });

  test('TC034: 测试add方法添加分钟', () => {
    const date = index('2023-01-01 00:00:00');
    const newDate = date.add(30, 'minute');
    expect(newDate.hour()).toBe(0);
    expect(newDate.minute()).toBe(30);
  });

  test('TC035: 测试parseLocale的isLocal参数为true', () => {
    const localeObj = { name: 'fr' };
    const result = index.locale('fr', localeObj, true);
    expect(result).toBe('fr');
  });
});