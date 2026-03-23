const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('Dayjs 单元测试', () => {
  // TC002
  test('测试 dayjs 函数传入 null 日期', () => {
    const result = index(null);
    expect(result.isValid()).toBe(false);
  });

  // TC005
  test('测试 dayjs 函数传入有效的 ISO 字符串（不含 Z）', () => {
    const result = index('2023-01-01 12:00:00');
    expect(result.isValid()).toBe(true);
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0); // 0-based month
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(12);
  });

  // TC006
  test('测试 dayjs 函数传入无效的字符串', () => {
    const result = index('invalid date');
    expect(result.isValid()).toBe(false);
  });

  // TC007
  test('测试 parseLocale 传入空 preset', () => {
    const result = index.locale(null);
    expect(result).toBe('en');
  });

  // TC008
  test('测试 parseLocale 传入已存在的 locale 字符串', () => {
    const result = index.locale('en');
    expect(result).toBe('en');
  });

  // TC009 (从 JSON 片段推断)
  test('测试 parseLocale 传入新 locale 字符串和对象', () => {
    const localeObj = { name: 'fr', weekStart: 1 };
    const result = index.locale('fr', localeObj);
    expect(result).toBe('fr');
  });

  // TC010
  test('测试 parseLocale 传入带连字符的 locale 字符串', () => {
    const result = index.locale('zh-CN');
    expect(result).toBe('zh');
  });

  // TC011 (从 JSON 片段推断)
  test('测试 parseLocale 传入对象 preset', () => {
    const localeObj = { name: 'ja' };
    const result = index.locale(localeObj);
    expect(result).toBe('ja');
  });

  // TC012
  test('测试 isValid 方法对有效日期返回 true', () => {
    const dayjsObj = index('2023-01-01');
    expect(dayjsObj.isValid()).toBe(true);
  });

  // TC013
  test('测试 isSame 方法相同日期', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.isSame('2023-01-01', 'day');
    expect(result).toBe(true);
  });

  // TC014
  test('测试 isAfter 方法', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.isAfter('2023-01-01', 'day');
    expect(result).toBe(false);
  });

  // TC015
  test('测试 isBefore 方法', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.isBefore('2023-01-02', 'day');
    expect(result).toBe(true);
  });

  // TC017
  test('测试 $g 方法带 input', () => {
    const dayjsObj = index('2023-01-01');
    // 通过公开的 setter 方法测试 $g 逻辑
    const result = dayjsObj.date(15);
    expect(result.date()).toBe(15);
    expect(result).not.toBe(dayjsObj); // 应该是新对象
  });

  // TC018
  test('测试 startOf 方法 units 为 Y（年）', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.startOf('year');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC019
  test('测试 startOf 方法 units 为 M（月）', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.startOf('month');
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(5); // June is 5 (0-based)
    expect(result.date()).toBe(1);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC020
  test('测试 startOf 方法 units 为 W（周）', () => {
    const dayjsObj = index('2023-06-15'); // Thursday
    const result = dayjsObj.startOf('week');
    // Assuming week starts on Sunday (en locale default)
    expect(result.date()).toBe(11); // June 11, 2023 is Sunday
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC021
  test('测试 startOf 方法 units 为 D（日）', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.startOf('day');
    expect(result.date()).toBe(15);
    expect(result.hour()).toBe(0);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC022
  test('测试 startOf 方法 units 为 H（小时）', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.startOf('hour');
    expect(result.hour()).toBe(14);
    expect(result.minute()).toBe(0);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC023
  test('测试 startOf 方法 units 为 MIN（分钟）', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.startOf('minute');
    expect(result.minute()).toBe(30);
    expect(result.second()).toBe(0);
    expect(result.millisecond()).toBe(0);
  });

  // TC024
  test('测试 startOf 方法 units 为 S（秒）', () => {
    const dayjsObj = index('2023-06-15 14:30:45.123');
    const result = dayjsObj.startOf('second');
    expect(result.second()).toBe(45);
    expect(result.millisecond()).toBe(0);
  });

  // TC025
  test('测试 startOf 方法 units 无效', () => {
    const dayjsObj = index('2023-06-15');
    const result = dayjsObj.startOf('invalid');
    // Should return a clone
    expect(result.valueOf()).toBe(dayjsObj.valueOf());
    expect(result).not.toBe(dayjsObj);
  });

  // TC026
  test('测试 endOf 方法', () => {
    const dayjsObj = index('2023-06-15');
    const result = dayjsObj.endOf('month');
    expect(result.month()).toBe(5); // June
    expect(result.date()).toBe(30); // June has 30 days
    expect(result.hour()).toBe(23);
    expect(result.minute()).toBe(59);
    expect(result.second()).toBe(59);
    expect(result.millisecond()).toBe(999);
  });

  // TC027
  test('测试 $set 方法设置月份', () => {
    const dayjsObj = index('2023-01-15');
    const result = dayjsObj.set('month', 5);
    expect(result.month()).toBe(5); // June
    expect(result.date()).toBe(15);
  });

  // TC028
  test('测试 $set 方法设置日期', () => {
    const dayjsObj = index('2023-06-01');
    const result = dayjsObj.set('date', 15);
    expect(result.date()).toBe(15);
  });

  // TC029
  test('测试 add 方法添加月份', () => {
    const dayjsObj = index('2023-01-15');
    const result = dayjsObj.add(2, 'month');
    expect(result.month()).toBe(3); // March (0-based)
  });

  // TC030
  test('测试 add 方法添加天数', () => {
    const dayjsObj = index('2023-01-15');
    const result = dayjsObj.add(3, 'day');
    expect(result.date()).toBe(18);
  });

  // TC031
  test('测试 add 方法添加小时', () => {
    const dayjsObj = index('2023-01-15 10:00:00');
    const result = dayjsObj.add(5, 'hour');
    expect(result.hour()).toBe(15);
  });

  // TC032
  test('测试 subtract 方法', () => {
    const dayjsObj = index('2023-01-15');
    const result = dayjsObj.subtract(1, 'day');
    expect(result.date()).toBe(14);
  });

  // TC033
  test('测试 format 方法无效日期', () => {
    const invalidDayjs = index(null);
    const result = invalidDayjs.format('YYYY-MM-DD');
    expect(result).toBe('Invalid Date');
  });

  // TC034
  test('测试 format 方法多种格式符', () => {
    const dayjsObj = index('2023-06-15 14:30:45');
    const result = dayjsObj.format('YYYY-MM-DD HH:mm:ss');
    expect(result).toBe('2023-06-15 14:30:45');
  });

  // TC035
  test('测试 diff 方法计算月份差', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.diff('2023-06-01', 'month');
    expect(result).toBe(-5); // January to June is 5 months
  });

  // TC036
  test('测试 diff 方法计算天数差（带 float）', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.diff('2023-01-02', 'day', true);
    expect(result).toBe(-1);
  });

  // TC037
  test('测试 locale 方法不带 preset', () => {
    const dayjsObj = index('2023-01-01');
    const result = dayjsObj.locale();
    expect(result).toBe('en');
  });

  // TC038
  test('测试 clone 方法', () => {
    const dayjsObj = index('2023-01-01');
    const clone = dayjsObj.clone();
    expect(clone.valueOf()).toBe(dayjsObj.valueOf());
    expect(clone).not.toBe(dayjsObj);
  });

  // TC039
  test('测试 toJSON 方法无效日期', () => {
    const invalidDayjs = index(null);
    const result = invalidDayjs.toJSON();
    expect(result).toBeNull();
  });

  // TC040
  test('测试 dayjs.unix 方法', () => {
    const result = index.unix(1672531200);
    expect(result.isValid()).toBe(true);
    // 1672531200 = 2023-01-01 00:00:00 UTC
    expect(result.year()).toBe(2023);
    expect(result.month()).toBe(0);
    expect(result.date()).toBe(1);
  });

test('补充: parseDate 当 date 为 undefined 时返回当前日期', () => {
    const result = dayjs(undefined);
    expect(result.isValid()).toBe(true);
  });

  test('补充: parseDate 处理 UTC 日期字符串', () => {
    const result = dayjs('2023-01-01 12:00:00.123', { utc: true });
    expect(result.isValid()).toBe(true);
  });

  test('补充: $utils 方法返回 Utils 对象', () => {
    const result = dayjs().$utils();
    expect(result).toBe(Utils);
  });

  test('补充: unix 方法返回时间戳秒数', () => {
    const date = dayjs('2023-01-01 00:00:00');
    const result = date.unix();
    expect(result).toBe(1672531200);
  });

  test('补充: get 方法获取年份', () => {
    const date = dayjs('2023-06-15');
    const result = date.get('year');
    expect(result).toBe(2023);
  });

  test('补充: add 方法添加年份', () => {
    const date = dayjs('2023-01-01');
    const result = date.add(1, 'year');
    expect(result.year()).toBe(2024);
  });

  test('补充: add 方法添加周数', () => {
    const date = dayjs('2023-01-01');
    const result = date.add(2, 'week');
    expect(result.date()).toBe(15);
  });

  test('补充: format 方法使用 YY 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('YY');
    expect(result).toBe('23');
  });

  test('补充: format 方法使用 M 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('M');
    expect(result).toBe('1');
  });

  test('补充: format 方法使用 MMM 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('MMM');
    expect(result).toBe('Jan');
  });

  test('补充: format 方法使用 MMMM 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('MMMM');
    expect(result).toBe('January');
  });

  test('补充: format 方法使用 D 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('D');
    expect(result).toBe('1');
  });

  test('补充: format 方法使用 d 格式', () => {
    const date = dayjs('2023-01-01'); // 周日
    const result = date.format('d');
    expect(result).toBe('0');
  });

  test('补充: format 方法使用 dd 格式', () => {
    const date = dayjs('2023-01-01'); // 周日
    const result = date.format('dd');
    expect(result).toBe('Su');
  });

  test('补充: format 方法使用 ddd 格式', () => {
    const date = dayjs('2023-01-01'); // 周日
    const result = date.format('ddd');
    expect(result).toBe('Sun');
  });

  test('补充: format 方法使用 dddd 格式', () => {
    const date = dayjs('2023-01-01'); // 周日
    const result = date.format('dddd');
    expect(result).toBe('Sunday');
  });

  test('补充: format 方法使用 H 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('H');
    expect(result).toBe('14');
  });

  test('补充: format 方法使用 h 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('h');
    expect(result).toBe('2');
  });

  test('补充: format 方法使用 hh 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('hh');
    expect(result).toBe('02');
  });

  test('补充: format 方法使用 a 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('a');
    expect(result).toBe('pm');
  });

  test('补充: format 方法使用 A 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('A');
    expect(result).toBe('PM');
  });

  test('补充: format 方法使用 m 格式', () => {
    const date = dayjs('2023-01-01 14:05:00');
    const result = date.format('m');
    expect(result).toBe('5');
  });

  test('补充: format 方法使用 s 格式', () => {
    const date = dayjs('2023-01-01 14:30:05');
    const result = date.format('s');
    expect(result).toBe('5');
  });

  test('补充: format 方法使用 SSS 格式', () => {
    const date = dayjs('2023-01-01 14:30:00.123');
    const result = date.format('SSS');
    expect(result).toBe('123');
  });

  test('补充: format 方法使用 Z 格式', () => {
    const date = dayjs('2023-01-01T14:30:00Z');
    const result = date.format('Z');
    expect(result).toMatch(/^[+-]\d{2}:\d{2}$/);
  });

  test('补充: diff 方法使用年单位', () => {
    const date1 = dayjs('2023-01-01');
    const date2 = dayjs('2024-01-01');
    const result = date1.diff(date2, 'year', true);
    expect(result).toBe(-1);
  });

  test('补充: diff 方法使用季度单位', () => {
    const date1 = dayjs('2023-01-01');
    const date2 = dayjs('2023-04-01');
    const result = date1.diff(date2, 'quarter', true);
    expect(result).toBe(-1);
  });

  test('补充: diff 方法使用周单位', () => {
    const date1 = dayjs('2023-01-01');
    const date2 = dayjs('2023-01-08');
    const result = date1.diff(date2, 'week', true);
    expect(result).toBe(-1);
  });

  test('补充: diff 方法使用小时单位', () => {
    const date1 = dayjs('2023-01-01 00:00:00');
    const date2 = dayjs('2023-01-01 02:00:00');
    const result = date1.diff(date2, 'hour', true);
    expect(result).toBe(-2);
  });

  test('补充: diff 方法使用分钟单位', () => {
    const date1 = dayjs('2023-01-01 00:00:00');
    const date2 = dayjs('2023-01-01 00:30:00');
    const result = date1.diff(date2, 'minute', true);
    expect(result).toBe(-30);
  });

  test('补充: diff 方法使用秒单位', () => {
    const date1 = dayjs('2023-01-01 00:00:00');
    const date2 = dayjs('2023-01-01 00:00:30');
    const result = date1.diff(date2, 'second', true);
    expect(result).toBe(-30);
  });

  test('补充: diff 方法使用默认单位（毫秒）', () => {
    const date1 = dayjs('2023-01-01 00:00:00');
    const date2 = dayjs('2023-01-01 00:00:00.500');
    const result = date1.diff(date2);
    expect(result).toBe(-500);
  });

  test('补充: locale 方法设置新区域', () => {
    const date = dayjs('2023-01-01');
    const result = date.locale('zh-cn');
    expect(result.$L).toBe('zh-cn');
  });

  test('补充: toISOString 方法返回 ISO 字符串', () => {
    const date = dayjs('2023-01-01T00:00:00Z');
    const result = date.toISOString();
    expect(result).toBe('2023-01-01T00:00:00.000Z');
  });

  test('补充: toString 方法返回 UTC 字符串', () => {
    const date = dayjs('2023-01-01T00:00:00Z');
    const result = date.toString();
    expect(result).toBe('Sun, 01 Jan 2023 00:00:00 GMT');
  });

  test('补充: extend 方法安装插件', () => {
    const plugin = (option, Dayjs, dayjs) => {
      Dayjs.prototype.testMethod = () => 'test';
    };
    const result = dayjs.extend(plugin);
    expect(result).toBe(dayjs);
  });

test('补充: parseDate 当 date 为 undefined 时返回当前日期', () => {
    const result = dayjs(undefined);
    expect(result.isValid()).toBe(true);
  });

  test('补充: parseDate 处理 UTC 日期字符串', () => {
    const result = dayjs('2023-01-01', { utc: true });
    expect(result.isValid()).toBe(true);
  });

  test('补充: $utils 方法返回 Utils 对象', () => {
    const result = dayjs().$utils();
    expect(result).toBe(Utils);
  });

  test('补充: unix 方法返回时间戳秒数', () => {
    const date = dayjs('2023-01-01 00:00:00');
    const result = date.unix();
    expect(result).toBe(1672531200);
  });

  test('补充: get 方法获取年份', () => {
    const date = dayjs('2023-06-15');
    const result = date.get('year');
    expect(result).toBe(2023);
  });

  test('补充: add 方法添加年份', () => {
    const date = dayjs('2023-01-01');
    const result = date.add(1, 'year');
    expect(result.year()).toBe(2024);
  });

  test('补充: add 方法添加周数', () => {
    const date = dayjs('2023-01-01');
    const result = date.add(2, 'week');
    expect(result.date()).toBe(15);
  });

  test('补充: format 方法处理 YY 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('YY');
    expect(result).toBe('23');
  });

  test('补充: format 方法处理 M 格式', () => {
    const date = dayjs('2023-06-15');
    const result = date.format('M');
    expect(result).toBe('6');
  });

  test('补充: format 方法处理 MMM 格式', () => {
    const date = dayjs('2023-01-01');
    const result = date.format('MMM');
    expect(result).toBe('Jan');
  });

  test('补充: format 方法处理 D 格式', () => {
    const date = dayjs('2023-01-15');
    const result = date.format('D');
    expect(result).toBe('15');
  });

  test('补充: format 方法处理 d 格式', () => {
    const date = dayjs('2023-01-01'); // 周日
    const result = date.format('d');
    expect(result).toBe('0');
  });

  test('补充: format 方法处理 h 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('h');
    expect(result).toBe('2');
  });

  test('补充: format 方法处理 a 格式', () => {
    const date = dayjs('2023-01-01 14:30:00');
    const result = date.format('a');
    expect(result).toBe('pm');
  });

  test('补充: diff 方法计算年份差', () => {
    const date1 = dayjs('2023-01-01');
    const date2 = dayjs('2025-01-01');
    const result = date1.diff(date2, 'year', true);
    expect(result).toBe(-2);
  });

  test('补充: locale 方法设置新区域', () => {
    const date = dayjs('2023-01-01');
    const result = date.locale('zh-cn');
    expect(result.$L).toBe('zh-cn');
  });

  test('补充: toISOString 方法返回 ISO 字符串', () => {
    const date = dayjs('2023-01-01T00:00:00Z');
    const result = date.toISOString();
    expect(result).toBe('2023-01-01T00:00:00.000Z');
  });

  test('补充: toString 方法返回 UTC 字符串', () => {
    const date = dayjs('2023-01-01T00:00:00Z');
    const result = date.toString();
    expect(result).toBe('Sun, 01 Jan 2023 00:00:00 GMT');
  });

  test('补充: extend 方法安装插件', () => {
    const plugin = (option, Dayjs, dayjs) => {
      Dayjs.prototype.testMethod = () => 'test';
    };
    const result = dayjs.extend(plugin);
    expect(result).toBe(dayjs);
  });
});