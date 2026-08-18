export type Me = {
  id: string
  name: string
  age: number
  balance: number
  cashback: number
  piggy: number
  has_invest_account: boolean
}

export type Position = {
  ticker: string
  name: string
  type: string
  qty: number
  avg: number
  price: number
  value: number
  pnl: number
  pnl_pct: number
  sparkline: number[]
}

export type Portfolio = {
  cash: number
  total: number
  day_pnl: number
  day_pnl_pct: number
  positions: Position[]
  onboarded: boolean
  goal: string | null
}

export type PulsePost = {
  id: string
  author: string
  title: string
  body: string
  tag: string
  tickers?: string[]
}

export type Instrument = {
  ticker: string
  name: string
  type: string
  price: number
  change_pct: number
  currency: string
  conservative: boolean
  sector: string
  desc: string
  sparkline?: number[]
  candles?: { o: number; h: number; l: number; c: number }[]
  book?: { bids: { price: number; qty: number }[]; asks: { price: number; qty: number }[] }
  metrics?: Record<string, string | number>
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
    ...init,
  })
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }))
    throw new Error(typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail || err))
  }
  return r.json()
}

export const api = {
  me: () => req<Me>('/api/me'),
  portfolio: () => req<Portfolio>('/api/portfolio'),
  operations: () => req<{ items: { id: string; kind: string; title: string; amount: number; ts: number }[] }>('/api/operations'),
  onboard: (goal?: string) =>
    req<Portfolio>('/api/onboard', { method: 'POST', body: JSON.stringify({ goal }) }),
  instruments: (q?: string, kind?: string) => {
    const p = new URLSearchParams()
    if (q) p.set('q', q)
    if (kind) p.set('kind', kind)
    const qs = p.toString()
    return req<{ items: Instrument[]; collections: { id: string; title: string; kind: string }[] }>(
      `/api/instruments${qs ? `?${qs}` : ''}`,
    )
  },
  instrument: (ticker: string) => req<Instrument>(`/api/instruments/${ticker}`),
  order: (body: { ticker: string; side: 'buy' | 'sell'; qty: number; order_type?: string }) =>
    req<{ order: unknown; portfolio: Portfolio }>('/api/orders', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  pulse: () => req<{ items: PulsePost[] }>('/api/pulse'),
  academy: () =>
    req<{ lessons: { id: string; title: string; minutes: number; done: boolean; text: string }[] }>(
      '/api/academy',
    ),
  chat: (messages: { role: string; content: string }[], context?: string) =>
    req<{ ok: boolean; reply: string; error?: string }>('/api/agent/chat', {
      method: 'POST',
      body: JSON.stringify({ messages, context }),
    }),
  health: () => req<{ api: string; ollama: { available: boolean; model: string } }>('/api/health'),
}

export function money(n: number, digits = 2) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: digits,
  }).format(n)
}

export function pct(n: number) {
  const sign = n > 0 ? '+' : ''
  return `${sign}${n.toFixed(2)}%`
}
