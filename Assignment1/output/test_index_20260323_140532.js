const _indexModule = require('../targets/index.js');
const index = _indexModule.default || _indexModule;

describe('dayjs library tests', () => {
  test('TC001: 测试 parseLocale 函数，传入 null 作为 preset', () => {
    const result = index.l(null, null, false);
    expect(result).toBe('en');
  });

  test('TC002: 测试 parseLocale 函数，传入字符串 preset，且在 Ls 中存在', () => {
    const result = index.l('en', null, false);
    expect(result).toBe('en');
  });

  test('TC003: 测试 parseLocale 函数，传入字符串 preset，且在 Ls 中不存在', () => {
    const result = index.l('fr', null, false);
    expect(result).toBe('en');
  });

  test('TC004: 测试 dayjs 函数，传入有效日期字符串', () => {
    const result = index('2023-10-01').$d;
    expect(result.toISOString()).toBe('2023-10-01T00:00:00.000Z');
  });

  test('TC005: 测试 dayjs 函数，传入 null 作为日期', () => {
    const result = index({ date: null, utc: false });
    expect(result.isValid()).toBe(false);
  });

  test('TC006: 测试 dayjs 函数，传入无效日期字符串', () => {
    const result = index({ date: 'invalid-date', locale: 'en' });
    expect(result.isValid()).toBe(false);
  });

  test('TC007: 测试 dayjs 函数，传入有效日期字符串并检查格式化', () => {
    const result = index('2023-10-01').format('YYYY-MM-DD');
    expect(result).toBe('2023-10-01');
  });

  test('TC008: 测试 dayjs 函数，传入有效日期字符串并检查日期对象', () => {
    const result = index('2023-10-01').toDate();
    expect(result).toEqual(new Date('2023-10-01T00:00:00.000Z'));
  });

  test('TC009: 测试 dayjs 函数，传入有效日期字符串并检查 unix 时间戳', () => {
    const result = index('2023-10-01').unix();
    expect(result).toBe(1696118400);
  });

  test('TC010: 测试 dayjs 函数，传入有效日期字符串并检查是否有效', () => {
    const result = index('2023-10-01');
    expect(result.isValid()).toBe(true);
  });

test('补充: 测试 parseLocale 处理字符串类型的 preset', () => {
    const result = parseLocale('en-US', null, false);
    expect(result).toBe('en-us');
  });

  test('补充: 测试 parseLocale 处理字符串类型的 preset 并传入 object', () => {
    const result = parseLocale('en-US', { greeting: 'Hello' }, false);
    expect(result).toBe('en-us');
    expect(Ls['en-us']).toEqual({ greeting: 'Hello' });
  });

  test('补充: 测试 parseLocale 处理没有 l 的情况', () => {
    const result = parseLocale('en-US-GB', null, false);
    expect(result).toBe('en');
  });

  test('补充: 测试 parseLocale 处理 null preset', () => {
    const result = parseLocale(null, null, false);
    expect(result).toBe(L);
  });

  test('补充: 测试 dayjs 处理 Dayjs 实例', () => {
    const date = dayjs();
    const result = dayjs(date);
    expect(result).toEqual(date.clone());
  });

  test('补充: 测试 parseDate 处理 null 日期', () => {
    const result = parseDate({ date: null });
    expect(result).toEqual(new Date(NaN));
  });

  test('补充: 测试 parseDate 处理字符串日期', () => {
    const result = parseDate({ date: '2023-01-01' });
    expect(result).toEqual(new Date('2023-01-01T00:00:00Z'));
  });

  test('补充: 测试 isSame 方法', () => {
    const date1 = dayjs('2023-01-01');
    const date2 = dayjs('2023-01-01');
    const result = date1.isSame(date2, 'day');
    expect(result).toBe(true);
  });

  test('补充: 测试 startOf 方法', () => {
    const date = dayjs('2023-01-01');
    const result = date.startOf('month');
    expect(result.date()).toBe(1);
  });

  test('补充: 测试 endOf 方法', () => {
    const date = dayjs('2023-01-01');
    const result = date.endOf('month');
    expect(result.date()).toBe(31);
  });

  test('补充: 测试 format 方法处理无效日期', () => {
    const date = dayjs(NaN);
    const result = date.format();
    expect(result).toBe(C.INVALID_DATE_STRING);
  });

  test('补充: 测试 locale 方法设置 locale', () => {
    const instance = dayjs();
    const result = instance.locale('fr');
    expect(result.$L).toBe('fr');
  });

  test('补充: 测试 clone 方法', () => {
    const date = dayjs('2023-01-01');
    const result = date.clone();
    expect(result).toEqual(date);
  });

  test('补充: 测试 toISOString 方法', () => {
    const date = dayjs('2023-01-01');
    const result = date.toISOString();
    expect(result).toBe(date.$d.toISOString());
  });

  test('补充: 测试 add 方法', () => {
    const date = dayjs('2023-01-01');
    const result = date.add(1, 'day');
    expect(result.date()).toBe(2);
  });

  test('补充: 测试 subtract 方法', () => {
    const date = dayjs('2023-01-02');
    const result = date.subtract(1, 'day');
    expect(result.date()).toBe(1);
  });

test('补充: 测试 parseLocale 函数，传入字符串 preset', () => {
    const result = parseLocale('en-US', null, false);
    expect(result).toBe('en-us');
  });

  test('补充: 测试 parseLocale 函数，传入字符串 preset 和 object', () => {
    const result = parseLocale('en-US', { key: 'value' }, false);
    expect(result).toBe('en-us');
    expect(Ls['en-us']).toEqual({ key: 'value' });
  });

  test('补充: 测试 parseLocale 函数，传入无效字符串 preset', () => {
    const result = parseLocale('invalid-locale', null, false);
    expect(result).toBeUndefined();
  });

  test('补充: 测试 parseLocale 函数，传入带有连字符的字符串 preset', () => {
    const result = parseLocale('fr-FR', null, false);
    expect(result).toBe('fr-fr');
  });

  test('补充: 测试 parseLocale 函数，传入空 preset', () => {
    const result = parseLocale(null, null, false);
    expect(result).toBe(L);
  });

  test('补充: 测试 dayjs 函数，传入有效日期', () => {
    const result = dayjs(new Date());
    expect(result).toBeInstanceOf(Object);
  });

  test('补充: 测试 parseDate 函数，传入 null', () => {
    const result = parseDate({ date: null });
    expect(result).toEqual(new Date(NaN));
  });

  test('补充: 测试 parseDate 函数，传入有效日期字符串', () => {
    const result = parseDate({ date: '2023-01-01' });
    expect(result).toEqual(new Date('2023-01-01T00:00:00.000Z'));
  });

  test('补充: 测试 isSame 函数，传入相同日期', () => {
    const result = dayjs().isSame(dayjs(), 'day');
    expect(result).toBe(true);
  });

  test('补充: 测试 isAfter 函数，传入未来日期', () => {
    const result = dayjs().isAfter(dayjs().add(1, 'day'), 'day');
    expect(result).toBe(true);
  });

  test('补充: 测试 isBefore 函数，传入过去日期', () => {
    const result = dayjs().isBefore(dayjs().subtract(1, 'day'), 'day');
    expect(result).toBe(true);
  });

  test('补充: 测试 $set 函数，设置日期', () => {
    const instance = dayjs();
    const result = instance.$set('date', 15);
    expect(result.$D).toBe(15);
  });

  test('补充: 测试 format 函数，传入无效日期', () => {
    const instance = dayjs(NaN);
    const result = instance.format();
    expect(result).toBe(C.INVALID_DATE_STRING);
  });

  test('补充: 测试 locale 函数，传入有效 preset', () => {
    const instance = dayjs();
    const result = instance.locale('en');
    expect(result.$L).toBe('en');
  });

  test('补充: 测试 clone 函数', () => {
    const instance = dayjs();
    const result = instance.clone();
    expect(result).not.toBe(instance);
    expect(result).toEqual(instance);
  });
});