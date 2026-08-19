import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, money, pct, type Instrument, type PulsePost } from '../api'
import { PriceChart } from '../components/PriceChart'

export function InstrumentPage() {
  const { ticker = '' } = useParams()
  const [inst, setInst] = useState<Instrument | null>(null)
  const [news, setNews] = useState<PulsePost | null>(null)
  const [tab, setTab] = useState<'chart' | 'book' | 'metrics'>('chart')
  const [range, setRange] = useState<'7' | '14' | '24'>('14')
  const [err, setErr] = useState('')

  useEffect(() => {
    const load = () => {
      api
        .instrument(ticker)
        .then(setInst)
        .catch((e) => setErr(e.message))
      api.pulse().then((r) => {
        const hit = r.items.find((p) => p.tickers?.some((t) => t.toUpperCase() === ticker.toUpperCase()))
        setNews(hit || null)
      })
    }
    load()
    const id = setInterval(load, 60_000)
    return () => clearInterval(id)
  }, [ticker])

  if (err)
    return (
      <div className="page">
        <p style={{ color: 'var(--red)' }}>{err}</p>
      </div>
    )
  if (!inst) return <div className="page muted">Загрузка…</div>

  return (
    <div className="page page-instrument">
      <div className="inst-head">
        <div className="row-between">
          <div>
            <h1 className="page-title" style={{ fontSize: 24 }}>
              {inst.ticker}
            </h1>
            <p className="page-sub" style={{ marginBottom: 8 }}>
              {inst.name}
            </p>
          </div>
          <div className="ticker-badge">{inst.type === 'etf' ? 'ETF' : 'Акц'}</div>
        </div>
        <p className="big-num" style={{ fontSize: 32 }}>
          {money(inst.price, inst.price < 1 ? 4 : 2)}
        </p>
        <p className={inst.change_pct >= 0 ? 'pnl-up muted' : 'pnl-down muted'}>{pct(inst.change_pct)} за день</p>
        {news ? (
          <Link to={`/pulse/${news.id}`} state={news} className="muted" style={{ display: 'block', marginTop: 8, fontSize: 13 }}>
            {news.title}
          </Link>
        ) : null}
        <p className="inst-desc">{inst.desc}</p>
      </div>

      <div className="inst-chart">
      <div className="seg">
        <button className={tab === 'chart' ? 'active' : ''} onClick={() => setTab('chart')}>
          График
        </button>
        <button className={tab === 'book' ? 'active' : ''} onClick={() => setTab('book')}>
          Стакан
        </button>
        <button className={tab === 'metrics' ? 'active' : ''} onClick={() => setTab('metrics')}>
          Показатели
        </button>
      </div>

      {tab === 'chart' && (
        <div className="card chart-card">
          <div className="chart-range">
            {(['7', '14', '24'] as const).map((n) => (
              <button key={n} className={range === n ? 'active' : ''} onClick={() => setRange(n)}>
                {n === '24' ? '24 мин' : `${n} мин`}
              </button>
            ))}
          </div>
          <PriceChart candles={(inst.candles || []).slice(-Number(range))} height={240} />
          <p className="chart-caption">
            Свечи по минутам. Зелёная — минута закрылась выше открытия, красная — ниже. Фитиль — максимум и минимум.
          </p>
        </div>
      )}

      {tab === 'book' && inst.book && (
        <div className="card">
          <p className="book-lead">
            Стакан — кто сколько хочет купить или продать <strong>прямо сейчас</strong>. Это не твой портфель.
          </p>
          <div className="book-grid">
            <div className="book-col">
              <div className="h">Покупка</div>
              <p className="book-hint">Люди готовы купить по этой цене. Справа — лоты (сколько штук).</p>
              <div className="book-head">
                <span>Цена, ₽</span>
                <span>Лоты</span>
              </div>
              {inst.book.bids.map((b) => {
                const maxQ = Math.max(...inst.book!.bids.map((x) => x.qty), 1)
                return (
                  <div key={b.price} className="book-row">
                    <span className="book-bar" style={{ width: `${(b.qty / maxQ) * 100}%` }} />
                    <span>{b.price}</span>
                    <span className="muted">{b.qty}</span>
                  </div>
                )
              })}
            </div>
            <div className="book-col">
              <div className="h sell">Продажа</div>
              <p className="book-hint">Люди готовы продать. Чем выше цена — тем дальше от рынка. Число справа — объём в лотах.</p>
              <div className="book-head">
                <span>Цена, ₽</span>
                <span>Лоты</span>
              </div>
              {inst.book.asks.map((a) => {
                const maxQ = Math.max(...inst.book!.asks.map((x) => x.qty), 1)
                return (
                  <div key={a.price} className="book-row sell">
                    <span className="book-bar sell" style={{ width: `${(a.qty / maxQ) * 100}%` }} />
                    <span className="sell-px">{a.price}</span>
                    <span className="muted">{a.qty}</span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {tab === 'metrics' && inst.metrics && (
        <div className="card">
          {[
            ['pe', 'P/E — цена к прибыли'],
            ['ps', 'P/S — цена к выручке'],
            ['debt_equity', 'Долг / капитал'],
            ['dividend_yield', 'Дивиденды, %'],
            ['consensus', 'Консенсус аналитиков'],
          ].map(([k, label]) => (
            <div key={k} className="row-between" style={{ padding: '8px 0', borderBottom: '1px solid var(--line)' }}>
              <span className="muted">{label}</span>
              <strong>{String(inst.metrics![k])}</strong>
            </div>
          ))}
        </div>
      )}
      </div>

      <aside className="inst-side">
        <div className="action-pair">
          <Link className="btn btn-primary" to={`/buy/${inst.ticker}`}>
            Купить
          </Link>
          <Link className="btn btn-ghost" to={`/buy/${inst.ticker}?side=sell`}>
            Продать
          </Link>
        </div>
      </aside>
    </div>
  )
}
