const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 测试套件', () => {
  // TC002
  test('测试 dayjs 函数传入 null 日期', () => {
    const result = index(null);
    expect(result.isValid()).toBe(false);
  });

  // TC005
  test('测试 dayjs 函数传入有效的日期字符串（非 Z 结尾）', () => {
    const result = index('2023-01-01 12:00:00');
    expect(result.isValid()).toBe(true);
    expect(result.format('YYYY-MM-DDTHH:mm:ss')).toBe('2023-01-01T12:00:00');
  });

  // TC006
  test('测试 dayjs 函数传入无效的日期字符串', () => {
    const result = index('invalid date');
    expect(result.isValid()).toBe(false);
  });

  // TC007
  test('测试 parseLocale 函数传入空 preset', () => {
    const result = index.locale(null);
    expect(result).toBe('en');
  });

  // TC008
  test('测试 parseLocale 函数传入已存在的 locale 字符串', () => {
    const result = index.locale('en');
    expect(result).toBe('en');
  });

  // TC010
  test('测试 parseLocale 函数传入带连字符的 locale 字符串（如 zh-CN）', () => {
    // 由于 zh-CN 不存在，会递归调用 parseLocale('zh')，而 zh 也不存在，所以会返回当前全局 locale 'en'
    const result = index.locale('zh-CN');
    expect(result).toBe('en');
  });

  // TC012
  test('测试 isValid 方法在有效日期时返回 true', () => {
    const result = index('2023-01-01').isValid();
    expect(result).toBe(true);
  });

  // TC013
  test('测试 isValid 方法在无效日期时返回 false', () => {
    const result = index('invalid').isValid();
    expect(result).toBe(false);
  });

  // TC014
  test('测试 isSame 方法（相同日期）', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-01');
    const result = date1.isSame(date2, 'day');
    expect(result).toBe(true);
  });

  // TC015
  test('测试 isAfter 方法（date1 在 date2 之后）', () => {
    const date1 = index('2023-01-02');
    const date2 = index('2023-01-01');
    const result = date1.isAfter(date2, 'day');
    expect(result).toBe(true);
  });

  // TC016
  test('测试 isBefore 方法（date1 在 date2 之前）', () => {
    const date1 = index('2023-01-01');
    const date2 = index('2023-01-02');
    const result = date1.isBefore(date2, 'day');
    expect(result).toBe(true);
  });

  // TC017
  test('测试 $g 方法不带 input 参数（get 模式）', () => {
    const date = index('2023-01-01');
    // 注意：$g 是私有方法，但可以通过原型访问
    const result = date.$g(undefined, '$y', 'year');
    expect(result).toBe(2023);
  });

  // TC018
  test('测试 $g 方法带 input 参数（set 模式）', () => {
    const date = index('2023-01-01');
    const result = date.$g(2024, '$y', 'year');
    expect(result.format('YYYY')).toBe('2024');
  });

  // TC019
  test('测试 startOf 方法，units 为 "year"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('year');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-01-01T00:00:00.000');
  });

  // TC020
  test('测试 endOf 方法，units 为 "year"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.endOf('year');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-12-31T23:59:59.999');
  });

  // TC021
  test('测试 startOf 方法，units 为 "month"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('month');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-01T00:00:00.000');
  });

  // TC022
  test('测试 startOf 方法，units 为 "week"（假设 weekStart 为 0）', () => {
    const date = index('2023-06-15T12:30:45'); // 2023-06-15 是周四
    const result = date.startOf('week');
    // 如果 weekStart=0（周日），那么周四所在的周从周日（2023-06-11）开始
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-11T00:00:00.000');
  });

  // TC023
  test('测试 startOf 方法，units 为 "day"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('day');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-15T00:00:00.000');
  });

  // TC024
  test('测试 startOf 方法，units 为 "hour"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('hour');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-15T12:00:00.000');
  });

  // TC025
  test('测试 startOf 方法，units 为 "minute"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('minute');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-15T12:30:00.000');
  });

  // TC026
  test('测试 startOf 方法，units 为 "second"', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('second');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-15T12:30:45.000');
  });

  // TC027
  test('测试 startOf 方法，units 为无效值', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.startOf('invalid');
    expect(result.format('YYYY-MM-DDTHH:mm:ss.SSS')).toBe('2023-06-15T12:30:45.000');
  });

  // TC028
  test('测试 $set 方法设置月份', () => {
    const date = index('2023-01-15');
    // $set 是私有方法，但可以通过原型访问
    const result = date.$set('month', 5);
    expect(result.format('YYYY-MM-DD')).toBe('2023-06-15');
  });

  // TC029
  test('测试 $set 方法设置日期（day of month）', () => {
    const date = index('2023-01-15');
    const result = date.$set('date', 20);
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-20');
  });

  // TC030
  test('测试 add 方法添加月份', () => {
    const date = index('2023-01-15');
    const result = date.add(2, 'month');
    expect(result.format('YYYY-MM-DD')).toBe('2023-03-15');
  });

  // TC031
  test('测试 add 方法添加年份', () => {
    const date = index('2023-01-15');
    const result = date.add(1, 'year');
    expect(result.format('YYYY-MM-DD')).toBe('2024-01-15');
  });

  // TC032
  test('测试 add 方法添加天数', () => {
    const date = index('2023-01-15');
    const result = date.add(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-20');
  });

  // TC033
  test('测试 add 方法添加周数', () => {
    const date = index('2023-01-15');
    const result = date.add(2, 'week');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-29');
  });

  // TC034
  test('测试 add 方法添加分钟', () => {
    const date = index('2023-01-15T12:00:00');
    const result = date.add(30, 'minute');
    expect(result.format('YYYY-MM-DDTHH:mm:ss')).toBe('2023-01-15T12:30:00');
  });

  // TC035
  test('测试 subtract 方法减去天数', () => {
    const date = index('2023-01-15');
    const result = date.subtract(5, 'day');
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-10');
  });

  // TC036
  test('测试 format 方法使用默认格式', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.format();
    // 默认格式是 'YYYY-MM-DDTHH:mm:ssZ'，但时区部分可能不同，所以只检查前半部分
    expect(result).toMatch(/^2023-06-15T12:30:45/);
  });

  // TC037
  test('测试 format 方法使用自定义格式（YYYY-MM-DD）', () => {
    const date = index('2023-06-15T12:30:45');
    const result = date.format('YYYY-MM-DD');
    expect(result).toBe('2023-06-15');
  });

  // 最后一个测试用例（JSON 中不完整，推断为测试无效日期的 format）
  test('测试无效日期的 format 方法', () => {
    const date = index('invalid');
    const result = date.format('YYYY-MM-DD');
    // 根据源代码，无效日期返回 locale.invalidDate 或 C.INVALID_DATE_STRING
    // 假设 C.INVALID_DATE_STRING 是 'Invalid Date'
    expect(result).toBe('Invalid Date');
  });
});