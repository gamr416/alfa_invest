import { useEffect, useState } from 'react'
import { api, money, type Portfolio } from '../api'
import { EmptyState } from '../components/EmptyState'
import { Link } from 'react-router-dom'

export function OperationsPage() {
  const [items, setItems] = useState<{ id: string; kind: string; title: string; amount: number; ts: number }[]>([])

  useEffect(() => {
    api.operations().then((r) => setItems(r.items))
  }, [])

  return (
    <div className="page">
      <h1 className="page-title" style={{ fontSize: 24 }}>
        Операции
      </h1>
      {items.length === 0 ? (
        <EmptyState text="Сделок ещё не было. Первый взнос — и лента оживёт." action={<Link className="btn btn-primary" to="/catalog">В каталог</Link>} />
      ) : (
        items.map((o) => (
          <div key={o.id} className="list-item">
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600 }}>{o.title}</div>
              <div className="muted">{new Date(o.ts * 1000).toLocaleString('ru-RU')}</div>
            </div>
            <strong className={o.amount >= 0 ? 'pnl-up' : 'pnl-down'}>{money(o.amount)}</strong>
          </div>
        ))
      )}
    </div>
  )
}

export function AnalyticsPage() {
  const [p, setP] = useState<Portfolio | null>(null)
  const [ops, setOps] = useState<{ kind: string; amount: number }[]>([])

  useEffect(() => {
    api.portfolio().then(setP)
    api.operations().then((r) => setOps(r.items))
  }, [])

  if (!p) return <div className="page muted">Загрузка…</div>

  const invested = p.positions.reduce((s, x) => s + x.value, 0)
  const costBasis = p.positions.reduce((s, x) => s + x.avg * x.qty, 0)
  const gained = p.positions.filter((x) => x.pnl > 0).reduce((s, x) => s + x.pnl, 0)
  const lost = p.positions.filter((x) => x.pnl < 0).reduce((s, x) => s + x.pnl, 0)
  const net = gained + lost
  const fees = ops.filter((o) => o.kind === 'commission').reduce((s, o) => s + o.amount, 0)
  const bought = ops.filter((o) => o.kind === 'trade' && o.amount < 0).reduce((s, o) => s + o.amount, 0)
  const sold = ops.filter((o) => o.kind === 'trade' && o.amount > 0).reduce((s, o) => s + o.amount, 0)

  const colors: Record<string, string> = { cash: '#111111', stock: '#EF3124', etf: '#1a9e4a' }
  const labels: Record<string, string> = { cash: 'Свободные', stock: 'Акции', etf: 'Фонды' }
  const byType: Record<string, number> = { cash: p.cash }
  for (const pos of p.positions) byType[pos.type] = (byType[pos.type] || 0) + pos.value
  const parts = Object.entries(byType)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => ({ key: k, label: labels[k] || k, value: v, color: colors[k] || '#888' }))
  const total = parts.reduce((s, x) => s + x.value, 0) || 1
  let acc = 0
  const gradient = parts
    .map((x) => {
      const a = (acc / total) * 100
      acc += x.value
      return `${x.color} ${a}% ${(acc / total) * 100}%`
    })
    .join(', ')

  const hasAssets = p.positions.length > 0
  const maxAbs = Math.max(...p.positions.map((x) => Math.abs(x.value)), 1)

  return (
    <div className="page">
      <h1 className="page-title" style={{ fontSize: 24 }}>
        Аналитика
      </h1>
      <p className="page-sub">Как лежат деньги и что уже случилось с ними</p>

      {!hasAssets ? (
        <EmptyState
          text="Когда появятся бумаги, здесь будет разбивка и результат."
          action={
            <Link className="btn btn-primary" to="/catalog">
              Купить первый пай
            </Link>
          }
        />
      ) : (
        <>
          <div className="hero">
            <p className="muted" style={{ marginBottom: 4 }}>
              Нереализованный результат
            </p>
            <p className="big-num" style={{ fontSize: 32, color: net >= 0 ? '#1a9e4a' : 'var(--red)' }}>
              {net >= 0 ? '+' : ''}
              {money(net)}
            </p>
            <p className="muted">К цене покупки. Пока бумаги не проданы — это на бумаге.</p>
          </div>

          <div className="stats-3">
            <div className="stat-box">
              <div className="k">Портфель</div>
              <div className="v">{money(p.total, 0)}</div>
            </div>
            <div className="stat-box">
              <div className="k">В бумагах</div>
              <div className="v">{money(invested, 0)}</div>
            </div>
            <div className="stat-box">
              <div className="k">Кэш</div>
              <div className="v">{money(p.cash, 0)}</div>
            </div>
          </div>

          <div className="pnl-split">
            <div className="pnl-card up">
              <span className="muted">Выросло</span>
              <strong>+{money(gained)}</strong>
              <span className="muted">позиции в плюсе</span>
            </div>
            <div className="pnl-card down">
              <span className="muted">Просело</span>
              <strong>{money(lost)}</strong>
              <span className="muted">позиции в минусе</span>
            </div>
          </div>

          <div className="section-label">Движение денег</div>
          <div className="card">
            <div className="stat-row row-between">
              <span className="muted">Потрачено на покупки</span>
              <strong>{money(bought)}</strong>
            </div>
            <div className="stat-row row-between">
              <span className="muted">Пришло с продаж</span>
              <strong>{money(sold)}</strong>
            </div>
            <div className="stat-row row-between">
              <span className="muted">Комиссии</span>
              <strong className="pnl-down">{money(fees)}</strong>
            </div>
            <div className="stat-row row-between">
              <span className="muted">Цена входа в бумаги</span>
              <strong>{money(costBasis)}</strong>
            </div>
            <div className="stat-row row-between">
              <span className="muted">Сейчас стоят</span>
              <strong>{money(invested)}</strong>
            </div>
          </div>

          <div className="section-label">Состав</div>
          <div className="card mix-row">
            <div className="pie" style={{ background: `conic-gradient(${gradient || '#EAEAEA'})` }} />
            <div className="legend">
              {parts.map((x) => (
                <div key={x.key} className="legend-item">
                  <span className="dot" style={{ background: x.color }} />
                  <span style={{ flex: 1 }}>{x.label}</span>
                  <span className="muted">{money(x.value, 0)}</span>
                  <strong>{Math.round((x.value / total) * 100)}%</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="section-label">По бумагам</div>
          <div className="card" style={{ padding: '12px 16px' }}>
            {p.positions.map((pos) => (
              <div key={pos.ticker} className="pos-bar">
                <div className="row-between">
                  <strong>{pos.ticker}</strong>
                  <span className={pos.pnl >= 0 ? 'gain' : 'pnl-down'}>
                    {pos.pnl >= 0 ? '+' : ''}
                    {money(pos.pnl)}
                  </span>
                </div>
                <div className="muted" style={{ margin: '2px 0 6px' }}>
                  {pos.name} · {pos.qty} шт · вход {money(pos.avg, pos.avg < 1 ? 4 : 2)}
                </div>
                <div className="hbar">
                  <span style={{ width: `${(pos.value / maxAbs) * 100}%` }} />
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
