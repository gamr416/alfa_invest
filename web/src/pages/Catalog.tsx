import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, money, pct, type Instrument } from '../api'
import { EmptyState } from '../components/EmptyState'

export function CatalogPage() {
  const [items, setItems] = useState<Instrument[]>([])
  const [collections, setCollections] = useState<{ id: string; title: string; kind: string }[]>([])
  const [kind, setKind] = useState('all')
  const [q, setQ] = useState('')

  useEffect(() => {
    api.instruments(q || undefined, kind === 'all' ? undefined : kind).then((r) => {
      setItems(r.items)
      setCollections(r.collections)
    })
  }, [kind, q])

  return (
    <div className="page">
      <h1 className="page-title">Каталог</h1>
      <p className="page-sub">Инструменты. Сначала — спокойные.</p>
      <Link className="banner" to="/instrument/LQDT">
        <img src="/mascot/alfa-buy.png" alt="" />
        <div>
          <strong>Витрина «Первый шаг»</strong>
          <span className="muted">LQDT, SBGB, FXRU — консервативные фонды.</span>
        </div>
      </Link>
      <input
        className="input"
        placeholder="Тикер или название"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        style={{ marginBottom: 14 }}
      />
      <div className="chip-row">
        <button className={`chip${kind === 'all' ? ' active' : ''}`} onClick={() => setKind('all')}>
          Всё
        </button>
        {collections.map((c) => (
          <button
            key={c.id}
            className={`chip${kind === c.kind && c.kind !== 'all' ? ' active' : ''}`}
            onClick={() => setKind(c.kind)}
          >
            {c.title}
          </button>
        ))}
      </div>
      {items.length === 0 ? (
        <EmptyState text="По такому запросу бумаг нет. Попробуй другой тикер." />
      ) : (
      <div className="card" style={{ padding: '4px 16px' }}>
        {items.map((i) => (
          <Link key={i.ticker} to={`/instrument/${i.ticker}`} className="list-item">
            <div className={`ticker-badge${i.conservative ? ' safe' : ''}`}>{i.ticker.slice(0, 4)}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600 }}>{i.name}</div>
              <div className="muted">
                {i.sector}
                {i.conservative ? ' · первый шаг' : ''}
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontWeight: 600, fontVariantNumeric: 'tabular-nums' }}>
                {money(i.price, i.price < 1 ? 4 : 2)}
              </div>
              <div className={i.change_pct >= 0 ? 'pnl-up muted' : 'pnl-down muted'}>{pct(i.change_pct)}</div>
            </div>
          </Link>
        ))}
      </div>
      )}
    </div>
  )
}
