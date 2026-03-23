const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 核心功能测试', () => {
  // TC002
  test('测试 dayjs 函数传入 null 日期', () => {
    const result = index(null);
    expect(result.isValid()).toBe(false);
  });

  // TC005
  test('测试 dayjs 函数传入可解析的日期字符串（非UTC）', () => {
    const result = index('2023-05-15 14:30:25.123');
    expect(result.isValid()).toBe(true);
    expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-05-15 14:30:25.123');
  });

  // TC006 (根据 JSON 片段推断)
  test('测试 dayjs 函数传入可解析的日期字符串（UTC）', () => {
    const result = index('2023-05-15 14:30:25.123', { utc: true });
    expect(result.isValid()).toBe(true);
    // 注意：UTC 模式下，toISOString 会返回 UTC 时间
    expect(result.toISOString()).toBe('2023-05-15T14:30:25.123Z');
  });

  // TC007
  test('测试 dayjs 函数传入不可解析的字符串，回退到 new Date(date)', () => {
    const result = index('invalid date string');
    expect(result.isValid()).toBe(false);
  });

  // TC008
  test('测试 dayjs 函数传入数字时间戳', () => {
    const result = index(1672531200000);
    expect(result.isValid()).toBe(true);
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  // TC009
  test('测试 parseLocale 函数传入空 preset，返回全局 locale', () => {
    const result = index.locale(null, null, false);
    expect(result).toBe('en');
  });

  // TC010
  test('测试 parseLocale 函数传入已加载的 locale 字符串（小写）', () => {
    const result = index.locale('en', null, false);
    expect(result).toBe('en');
  });

  // TC011 (根据 JSON 片段推断)
  test('测试 parseLocale 函数传入新 locale 字符串并注册', () => {
    const frLocale = { name: 'fr' };
    const result = index.locale('fr', frLocale, false);
    expect(result).toBe('fr');
    expect(index.Ls.fr).toBe(frLocale);
  });

  // TC012
  test('测试 parseLocale 函数传入带连字符的 locale 字符串，且第一部分未加载', () => {
    const result = index.locale('zh-CN', null, false);
    expect(result).toBe('zh');
  });

  // TC013 (根据 JSON 片段推断)
  test('测试 parseLocale 函数传入 locale 对象', () => {
    const jaLocale = { name: 'ja' };
    const result = index.locale(jaLocale, null, false);
    expect(result).toBe('ja');
    expect(index.Ls.ja).toBe(jaLocale);
  });

  // TC014 (根据 JSON 片段推断)
  test('测试 parseLocale 函数传入 locale 字符串，isLocal 为 true', () => {
    const deLocale = { name: 'de' };
    const result = index.locale('de', deLocale, true);
    expect(result).toBe('de');
    // isLocal 为 true 时，全局 L 不应改变（应为 'en'）
    expect(index.locale()).toBe('en');
  });

  // TC022
  test('测试 $g 方法，input 有值时调用 set 方法', () => {
    const dayjsObj = index('2023-06-15');
    // 注意：$g 是私有方法，但可以通过原型访问
    const result = dayjsObj.$g(20, '$D', 'D');
    expect(result.format('YYYY-MM-DD')).toBe('2023-06-20');
  });

  // TC023
  test('测试 startOf 方法，units 为 "year"，isStartOf 为 true', () => {
    const dayjsObj = index('2023-06-15 14:30:25');
    const result = dayjsObj.startOf('year', true);
    expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-01-01 00:00:00.000');
  });

  // TC024
  test('测试 startOf 方法，units 为 "month"，isStartOf 为 false（即 endOf month）', () => {
    const dayjsObj = index('2023-06-15 14:30:25');
    const result = dayjsObj.startOf('month', false);
    expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-30 23:59:59.999');
  });

  // TC025
  test('测试 startOf 方法，units 为 "week"，且 $W 小于 weekStart', () => {
    const dayjsObj = index('2023-01-01'); // 2023-01-01 是周日 (0)
    const result = dayjsObj.startOf('week', true);
    // 默认 weekStart 为 0（周日），所以一周开始是 2023-01-01
    expect(result.format('YYYY-MM-DD')).toBe('2023-01-01');
  });

  // TC026
  test('测试 startOf 方法，units 为 "day"，使用 instanceFactorySet', () => {
    const dayjsObj = index('2023-06-15 14:30:25');
    const result = dayjsObj.startOf('day', true);
    expect(result.format('YYYY-MM-DD HH:mm:ss.SSS')).toBe('2023-06-15 00:00:00.000');
  });

  // TC027
  test('测试 startOf 方法，units 为无效值，返回克隆对象', () => {
    const dayjsObj = index('2023-06-15');
    const result = dayjsObj.startOf('invalid', true);
    expect(result.format('YYYY-MM-DD')).toBe('2023-06-15');
    expect(result).not.toBe(dayjsObj); // 应该是克隆对象
  });

  // TC028
  test('测试 $set 方法，设置日期 (C.D)', () => {
    const dayjsObj = index('2023-06-15');
    // $set 是私有方法，但可以通过原型访问
    const result = dayjsObj.$set('D', 20);
    expect(result.format('YYYY-MM-DD')).toBe('2023-06-20');
  });

  // TC029
  test('测试 $set 方法，设置月份 (C.M)', () => {
    const dayjsObj = index('2023-01-31');
    const result = dayjsObj.$set('M', 1); // 设置为二月
    expect(result.format('YYYY-MM-DD')).toBe('2023-02-28'); // 自动调整到2月最后一天
  });

  // TC030
  test('测试 add 方法，添加月份', () => {
    const dayjsObj = index('2023-01-31');
    const result = dayjsObj.add(1, 'M');
    expect(result.format('YYYY-MM-DD')).toBe('2023-02-28');
  });

  // TC031
  test('测试 add 方法，添加天数', () => {
    const dayjsObj = index('2023-01-31');
    const result = dayjsObj.add(1, 'D');
    expect(result.format('YYYY-MM-DD')).toBe('2023-02-01');
  });

  // TC032
  test('测试 add 方法，添加分钟', () => {
    const dayjsObj = index('2023-01-01 00:00:00');
    const result = dayjsObj.add(30, 'minute');
    expect(result.format('YYYY-MM-DD HH:mm:ss')).toBe('2023-01-01 00:30:00');
  });
});