const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 白盒测试', () => {
  // TC002
  test('测试dayjs函数传入null日期', () => {
    const result = index(null);
    expect(result.isValid()).toBe(false);
  });

  // TC005
  test('测试dayjs函数传入有效日期字符串（非UTC）', () => {
    const result = index('2023-01-01 12:30:45.123');
    expect(result.isValid()).toBe(true);
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0); // 0-based month
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(30);
    expect(result.second()).toBe(45);
    expect(result.millisecond()).toBe(123);
  });

  // TC006
  test('测试dayjs函数传入UTC日期字符串', () => {
    const result = index('2023-01-01T12:30:45Z');
    expect(result.isValid()).toBe(true);
  });

  // TC007
  test('测试dayjs函数传入无效日期字符串', () => {
    const result = index('invalid-date');
    expect(result.isValid()).toBe(false);
  });

  // TC008
  test('测试parseLocale传入空preset', () => {
    const result = index.locale(null);
    expect(result).toBe('en');
  });

  // TC009
  test('测试parseLocale传入已存在的locale字符串', () => {
    const result = index.locale('en');
    expect(result).toBe('en');
  });

  // TC010 (从JSON片段推断)
  test('测试parseLocale传入新locale字符串和对象', () => {
    const localeObj = { name: 'zh-cn', weekStart: 1 };
    const result = index.locale('zh-cn', localeObj);
    expect(result).toBe('zh-cn');
  });

  // TC011
  test('测试parseLocale传入带连字符的locale字符串（无对应locale）', () => {
    const result = index.locale('zh-CN');
    // 由于zh不存在，会返回当前全局locale 'en'
    expect(result).toBe('en');
  });

  // TC012 (从JSON片段推断)
  test('测试parseLocale传入locale对象', () => {
    const localeObj = { name: 'fr' };
    const result = index.locale(localeObj);
    expect(result).toBe('fr');
  });

  // TC013
  test('测试isValid方法对有效日期返回true', () => {
    const result = index('2023-01-01');
    expect(result.isValid()).toBe(true);
  });

  // TC014
  test('测试isValid方法对无效日期返回false', () => {
    const result = index('invalid');
    expect(result.isValid()).toBe(false);
  });

  // TC015
  test('测试isSame方法相同日期相同单位', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-01');
    expect(date1.isSame(date2, 'day')).toBe(true);
  });

  // TC016
  test('测试isSame方法不同日期', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-02');
    expect(date1.isSame(date2, 'day')).toBe(false);
  });

  // TC017
  test('测试isAfter方法', () => {
    const date1 = index('2023-01-02');
    const date2 = index('2023-01-01');
    expect(date1.isAfter(date2, 'day')).toBe(true);
  });

  // TC018
  test('测试isBefore方法', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-02');
    expect(date1.isBefore(date2, 'day')).toBe(true);
  });

  // TC019
  test('测试$g方法不带input参数', () => {
    const date = index('2023-01-01');
    // 注意：$g是私有方法，通过原型链访问
    expect(date.$g(undefined, '$y', 'year')).toBe(2023);
  });

  // TC020
  test('测试$g方法带input参数', () => {
    const date = index('2023-01-01');
    const result = date.$g(2024, '$y', 'year');
    expect(result.year()).toBe(2024);
  });

  // TC021
  test('测试startOf方法Y单位', () => {
    const date = index('2023-06-15');
    const result = date.startOf('year');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC022
  test('测试endOf方法Y单位', () => {
    const date = index('2023-06-15');
    const result = date.endOf('year');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(11);
    expect(result.date()).toBe(31);
    expect(result.hour()).toBe(23);
    expect(result.minute()).toBe(59);
    expect(result.second()).toBe(59);
    expect(result.millisecond()).toBe(999);
  });

  // TC023
  test('测试startOf方法M单位', () => {
    const date = index('2023-06-15');
    const result = date.startOf('month');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC024
  test('测试startOf方法W单位', () => {
    const date = index('2023-06-15'); // 周四
    const result = date.startOf('week');
    // 假设周开始是周日 (weekStart = 0)
    expect(result.date()).toBe(11); // 2023-06-11 周日
  });

  // TC025
  test('测试startOf方法D单位', () => {
    const date = index('2023-06-15 12:30:45');
    const result = date.startOf('day');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC026
  test('测试startOf方法H单位', () => {
    const date = index('2023-06-15 12:30:45');
    const result = date.startOf('hour');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC027
  test('测试startOf方法MIN单位', () => {
    const date = index('2023-06-15 12:30:45');
    const result = date.startOf('minute');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(30);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC028
  test('测试startOf方法S单位', () => {
    const date = index('2023-06-15 12:30:45.123');
    const result = date.startOf('second');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(30);
    expect(result.second()).toBe(45);
    expect(result.millisecond()).toBe(0);
  });

  // TC029
  test('测试startOf方法无效单位', () => {
    const date = index('2023-06-15');
    const result = date.startOf('invalid');
    // 应该返回克隆对象
    expect(result.valueOf()).toBe(date.valueOf());
    expect(result).not.toBe(date); // 确保是克隆
  });

  // TC030
  test('测试$set方法设置月份', () => {
    const date = index('2023-01-15');
    // $set是私有方法
    const result = date.$set('month', 5);
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5);
    expect(result.date()).toBe(15);
  });

  // TC031
  test('测试$set方法设置日期', () => {
    const date = index('2023-01-15');
    const result = date.$set('date', 20);
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(20);
  });

  // TC032
  test('测试add方法添加月份', () => {
    const date = index('2023-01-15');
    const result = date.add(2, 'month');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(2);
    expect(result.date()).toBe(15);
  });

  // TC033
  test('测试add方法添加年份', () => {
    const date = index('2023-01-15');
    const result = date.add(1, 'year');
    expect(result.year()).toBe(2024);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(15);
  });

  // TC034
  test('测试add方法添加天数', () => {
    const date = index('2023-01-15');
    const result = date.add(5, 'day');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(20);
  });

  // TC035
  test('测试add方法添加周数', () => {
    const date = index('2023-01-15');
    const result = date.add(2, 'week');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(29);
  });

  // TC036
  test('测试add方法添加分钟', () => {
    const date = index('2023-01-15 12:00:00');
    const result = date.add(30, 'minute');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(12);
    expect(result.minute()).toBe(30);
  });

  // TC037
  test('测试subtract方法', () => {
    const date = index('2023-01-15');
    const result = date.subtract(5, 'day');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(10);
  });

  // TC038
  test('测试format方法无效日期', () => {
    const date = index('invalid');
    const result = date.format('YYYY-MM-DD');
    expect(result).toBe('Invalid Date');
  });

  // TC039
  test('测试format方法默认格式', () => {
    const date = index('2023-06-15 12:30:45');
    const result = date.format();
    // 默认格式应该是类似 'YYYY-MM-DDTHH:mm:ssZ' 的格式
    expect(typeof result).toBe('string');
    expect(result.length).toBeGreaterThan(0);
  });

  // TC040
  test('测试format方法YYYY-MM-DD格式', () => {
    const date = index('2023-06-15');
    const result = date.format('YYYY-MM-DD');
    expect(result).toBe('2023-06-15');
  });

  // TC041 (从JSON片段推断)
  test('测试format方法hh:mm A格式', () => {
    const date = index('2023-06-15 14:30:00');
    const result = date.format('hh:mm A');
    // 14:30 应该是 02:30 PM
    expect(result).toBe('02:30 PM');
  });
});