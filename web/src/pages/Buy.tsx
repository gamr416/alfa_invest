import { useEffect, useState } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { api, money, type Instrument } from '../api'
import { Mascot } from '../components/Mascot'

export function BuyPage() {
  const { ticker = '' } = useParams()
  const [params] = useSearchParams()
  const nav = useNavigate()
  const [inst, setInst] = useState<Instrument | null>(null)
  const [qty, setQty] = useState('1')
  const [side, setSide] = useState<'buy' | 'sell'>(params.get('side') === 'sell' ? 'sell' : 'buy')
  const [orderType, setOrderType] = useState('market')
  const [confirm, setConfirm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')
  const [cash, setCash] = useState(0)

  useEffect(() => {
    api.instrument(ticker).then(setInst)
    api.portfolio().then((p) => setCash(p.cash))
  }, [ticker])

  if (!inst) return <div className="page muted">Загрузка…</div>

  const n = Number(qty) || 0
  const cost = n * inst.price
  const commission = Math.max(cost * 0.0005, 1)

  async function submit() {
    setLoading(true)
    setErr('')
    try {
      await api.order({ ticker, side, qty: n, order_type: orderType })
      setConfirm(false)
      nav('/', { replace: true })
    } catch (e) {
      setErr(e instanceof Error ? e.message : 'Ошибка')
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <Mascot pose="type" size={100} text={`Заявка по ${inst.ticker}. Проверь сумму перед отправкой.`} />
      <div className="seg">
        <button className={side === 'buy' ? 'active' : ''} onClick={() => setSide('buy')} style={{ gridColumn: 'span 1' }}>
          Покупка
        </button>
        <button className={side === 'sell' ? 'active' : ''} onClick={() => setSide('sell')}>
          Продажа
        </button>
        <button className={orderType === 'market' ? 'active' : ''} onClick={() => setOrderType('market')}>
          Рыночная
        </button>
      </div>
      <div className="field">
        <label className="label">Количество</label>
        <input className="input" value={qty} onChange={(e) => setQty(e.target.value)} inputMode="decimal" />
      </div>
      <div className="card">
        <div className="row-between">
          <span className="muted">Цена</span>
          <span>{money(inst.price, inst.price < 1 ? 4 : 2)}</span>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
          <span className="muted">Сумма</span>
          <strong>{money(cost)}</strong>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
          <span className="muted">Комиссия ≈</span>
          <span>{money(commission)}</span>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
          <span className="muted">Доступно</span>
          <span>{money(cash)}</span>
        </div>
      </div>
      {err ? <p style={{ color: 'var(--red)' }}>{err}</p> : null}
      <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setConfirm(true)}>
        {side === 'sell' ? 'Продать' : 'Купить'}
      </button>

      {confirm && (
        <div className="sheet-backdrop" onClick={() => setConfirm(false)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <div className="sheet-handle" />
            <Mascot
              pose="buy"
              size={110}
              text={`${side === 'buy' ? 'Покупка' : 'Продажа'} ${n} × ${inst.ticker} за ${money(cost)}. Подтверди.`}
            />
            <button className="btn btn-primary" disabled={loading} onClick={submit}>
              {loading ? 'Отправляю…' : 'Подтвердить'}
            </button>
            <button className="btn btn-ghost" style={{ marginTop: 8 }} onClick={() => setConfirm(false)}>
              Отмена
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
