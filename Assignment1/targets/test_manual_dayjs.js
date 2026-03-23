import dayjs, { parseDate, parseLocale, defaultLocale as L, loadedLocales as Ls } from './index.js'

describe('1. parseDate(cfg)', () => {
  test('TC1 null → Path1', () => {
    const d = parseDate({ date: null })
    expect(isNaN(d.getTime())).toBe(true)
  })

  test('TC2 undefined → Path2', () => {
    const d = parseDate({ date: undefined })
    expect(d).toBeInstanceOf(Date)
    expect(Math.abs(d.getTime() - Date.now())).toBeLessThan(100)
  })

  test('TC3 Date 对象 → Path3', () => {
    const orig = new Date()
    const d = parseDate({ date: orig })
    expect(d.getTime()).toBe(orig.getTime())
  })

  test('TC4 字符串 + utc=true → Path4', () => {
    const d = parseDate({ date: '2024-01-01', utc: true })
    expect(d.toISOString()).toBe('2024-01-01T00:00:00.000Z')
  })

  test('TC5 字符串 + utc=false → Path5', () => {
    const d = parseDate({ date: '2024-01-01', utc: false })
    expect(d.getFullYear()).toBe(2024)
  })

  test('TC6 非法字符串 → Path6', () => {
    const d = parseDate({ date: 'invalid-date' })
    expect(isNaN(d.getTime())).toBe(true)
  })

  test('TC7 时间戳 → Path7', () => {
    const d = parseDate({ date: 1700000000000 })
    expect(d.getTime()).toBe(1700000000000)
  })
})

describe('2. parseLocale(preset, object, isLocal)', () => {
  let originalL
  beforeEach(() => { originalL = L })

  test('TC1 null → Path1', () => {
    expect(parseLocale(null)).toBe(L)
  })

  test('TC2 "en" → Path2', () => {
    const res = parseLocale('en')
    expect(res).toBe('en')
    expect(L).toBe('en')
  })

  test('TC3 "abc" → Path3', () => {
    expect(parseLocale('abc')).toBe(L) // 返回默认
  })

  test('TC4 "fr" + object → Path4', () => {
    const obj = { name: 'fr' }
    const res = parseLocale('fr', obj)
    expect(res).toBe('fr')
    expect(Ls.fr).toEqual(obj)
  })

  test('TC5 "en-US" fallback → Path5', () => {
    const res = parseLocale('en-US')
    expect(res).toBe('en')
  })

  test('TC6 对象形式 → Path6', () => {
    const obj = { name: 'jp' }
    const res = parseLocale(obj)
    expect(res).toBe('jp')
  })

  test('TC7 isLocal=true → Path7', () => {
    const res = parseLocale('en', null, true)
    expect(res).toBe('en')
    expect(L).toBe(originalL) // 不修改全局
  })
})

describe('3. Dayjs.prototype.diff', () => {
  const base = dayjs('2024-06-01T12:00:00')

  test('TC1 year float → Path1', () => {
    expect(base.diff('2023-06-01', 'year', true)).toBe(1)
  })

  test('TC2 month float → Path2', () => {
    expect(base.diff('2024-04-15', 'month', true)).toBe(1.5)
  })

  test('TC3 quarter float → Path3', () => {
    expect(base.diff('2023-12-01', 'quarter', true)).toBe(2)
  })

  test('TC4 week float → Path4', () => {
    expect(base.diff('2024-05-18', 'week', true)).toBe(2)
  })

  test('TC5 day float → Path5', () => {
    expect(base.diff('2024-05-30', 'day', true)).toBe(2)
  })

  test('TC6 hour float → Path6', () => {
    expect(base.diff('2024-06-01T09:30:00', 'hour', true)).toBe(2.5)
  })

  test('TC7 minute float → Path7', () => {
    expect(base.diff('2024-06-01T11:45:00', 'minute', true)).toBe(15)
  })

  test('TC8 second float → Path8', () => {
    expect(base.diff('2024-06-01T11:59:30', 'second', true)).toBe(30)
  })

  test('TC9 ms float → Path9', () => {
    expect(base.diff('2024-06-01T11:59:59.500', 'ms', true)).toBe(500)
  })

  test('TC10 month integer → Path10', () => {
    expect(base.diff('2024-04-15', 'month', false)).toBe(1)
  })

  test('TC11 month round验证 → Path10', () => {
    expect(base.diff('2024-03-01', 'month', false)).toBe(2)
  })

  test('TC12 month float对照 → Path10', () => {
    expect(base.diff('2024-03-01', 'month', true)).toBeCloseTo(1.548, 3)
  })

  test('TC13 边界值 → Path10', () => {
    expect(base.diff('2024-02-01', 'month', false)).toBe(1)
  })
})