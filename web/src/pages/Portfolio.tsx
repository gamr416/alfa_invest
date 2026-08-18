import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, money, pct, type Instrument, type Portfolio } from '../api'
import { Sparkline } from '../components/Sparkline'
import { EmptyState } from '../components/EmptyState'

export function PortfolioPage() {
  const [data, setData] = useState<Portfolio | null>(null)
  const [movers, setMovers] = useState<Instrument[]>([])
  const [err, setErr] = useState('')

  useEffect(() => {
    const load = () => {
      api
        .portfolio()
        .then(setData)
        .catch((e) => setErr(e.message))
      api.instruments().then((r) => {
        const sorted = [...r.items].sort((a, b) => Math.abs(b.change_pct) - Math.abs(a.change_pct))
        setMovers(sorted.slice(0, 6))
      })
    }
    load()
    const id = setInterval(load, 60_000)
    return () => clearInterval(id)
  }, [])

  if (err)
    return (
      <div className="page">
        <p style={{ color: 'var(--red)' }}>{err}</p>
      </div>
    )
  if (!data) return <div className="page muted">Загрузка…</div>

  const invested = data.total - data.cash
  const pnlClass = data.day_pnl >= 0 ? 'pnl-up' : 'pnl-down'

  return (
    <div className="page">
      <p className="page-sub" style={{ marginBottom: 4 }}>
        Брокерский счёт · бумага
      </p>
      <h1 className="page-title">Портфель</h1>
      <div className="hero">
        <p className="big-num">{money(data.total)}</p>
        <p className={`muted ${pnlClass}`} style={{ marginTop: 6 }}>
          за день {data.day_pnl >= 0 ? '+' : ''}
          {money(data.day_pnl)} · {pct(data.day_pnl_pct)}
        </p>
      </div>

      <div className="stats-3">
        <div className="stat-box">
          <div className="k">Кэш</div>
          <div className="v">{money(data.cash, 0)}</div>
        </div>
        <div className="stat-box">
          <div className="k">В бумагах</div>
          <div className="v">{money(invested, 0)}</div>
        </div>
        <div className="stat-box">
          <div className="k">Позиций</div>
          <div className="v">{data.positions.length}</div>
        </div>
      </div>

      <Link className="banner" to="/catalog">
        <img src="/mascot/alfa-hello.png" alt="" />
        <div>
          <strong>Первый шаг от 100 ₽</strong>
          <span className="muted">Фонд денежного рынка LQDT. Без обещания доходности.</span>
        </div>
      </Link>

      <div className="tiles">
        <Link className="tile" to="/analytics">
          <span className="muted">Состав</span>
          <strong>Аналитика</strong>
        </Link>
        <Link className="tile" to="/operations">
          <span className="muted">Лента</span>
          <strong>Операции</strong>
        </Link>
        <Link className="tile" to="/buy/LQDT">
          <span className="muted">Консервативно</span>
          <strong>Купить LQDT</strong>
        </Link>
        <Link className="tile" to="/agent">
          <span className="muted">Спросить</span>
          <strong>Агент</strong>
        </Link>
      </div>

      <div className="section-label">Активы</div>
      {data.positions.length === 0 ? (
        <EmptyState
          text="Портфель ждёт первый пай. Можно с кэшбэка, от 100 ₽."
          action={
            <Link className="btn btn-primary" to="/catalog">
              В каталог
            </Link>
          }
        />
      ) : (
        <div className="card" style={{ padding: '4px 16px' }}>
          {data.positions.map((p) => (
            <Link key={p.ticker} to={`/instrument/${p.ticker}`} className="list-item">
              <div className="ticker-badge safe">{p.ticker.slice(0, 4)}</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 600 }}>{p.name}</div>
                <div className="muted">
                  {p.qty} шт · {money(p.value)}
                </div>
              </div>
              <Sparkline points={p.sparkline} />
              <div style={{ textAlign: 'right', minWidth: 68 }}>
                <div style={{ fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>
                  {money(p.price, p.price < 1 ? 4 : 2)}
                </div>
                <div className={p.pnl >= 0 ? 'pnl-up muted' : 'pnl-down muted'}>{pct(p.pnl_pct)}</div>
              </div>
            </Link>
          ))}
        </div>
      )}

      <div className="section-label">Движение рынка</div>
      <div className="h-scroll">
        {movers.map((m) => (
          <Link key={m.ticker} className="mini-card" to={`/instrument/${m.ticker}`}>
            <div className="t">{m.ticker}</div>
            <div className="muted" style={{ fontSize: 11, margin: '4px 0 8px' }}>
              {m.name}
            </div>
            <div style={{ fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}>
              {money(m.price, m.price < 1 ? 4 : 2)}
            </div>
            <div className={m.change_pct >= 0 ? 'pnl-up muted' : 'pnl-down muted'}>{pct(m.change_pct)}</div>
          </Link>
        ))}
      </div>

      <div className="section-label">Сегодня</div>
      <div className="card" style={{ padding: '4px 16px' }}>
        <Link className="list-item" to="/learn">
          <div className="ticker-badge">2м</div>
          <div>
            <div style={{ fontWeight: 600 }}>Урок: что такое риск</div>
            <div className="muted">Академия · без теста на гения</div>
          </div>
        </Link>
        <Link className="list-item" to="/pulse">
          <div className="ticker-badge">П</div>
          <div>
            <div style={{ fontWeight: 600 }}>Три коротких поста</div>
            <div className="muted">Пульс · без сигналов к покупке</div>
          </div>
        </Link>
      </div>
    </div>
  )
}
