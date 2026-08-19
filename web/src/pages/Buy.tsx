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
  const [confirm, setConfirm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')
  const [cash, setCash] = useState(0)
  const [held, setHeld] = useState(0)

  useEffect(() => {
    api.instrument(ticker).then(setInst)
    api.portfolio().then((p) => {
      setCash(p.cash)
      const pos = p.positions.find((x) => x.ticker.toUpperCase() === ticker.toUpperCase())
      setHeld(pos?.qty ?? 0)
    })
  }, [ticker])

  if (!inst) return <div className="page muted">Загрузка…</div>

  const n = Number(qty)
  const qtyOk = Number.isFinite(n) && n > 0
  const cost = (qtyOk ? n : 0) * inst.price
  const commission = Math.max(cost * 0.0005, 1)
  const needCash = cost + commission
  const blocked =
    !qtyOk
      ? 'Укажи количество больше 0.'
      : side === 'buy' && needCash > cash
        ? 'Недостаточно средств.'
        : side === 'sell' && n > held
          ? 'Нет столько акций.'
          : ''

  async function submit() {
    if (!qtyOk) return
    setLoading(true)
    setErr('')
    try {
      await api.order({ ticker, side, qty: n, order_type: 'market' })
      setConfirm(false)
      nav('/', { replace: true })
    } catch (e) {
      setErr(e instanceof Error ? e.message : 'Ошибка')
      setLoading(false)
    }
  }

  return (
    <div className="page page-narrow">
      <Mascot pose="type" size={100} text={`Заявка по ${inst.ticker}. Проверь сумму перед отправкой.`} />
      <div className="seg two">
        <button className={side === 'buy' ? 'active' : ''} onClick={() => setSide('buy')}>
          Покупка
        </button>
        <button className={side === 'sell' ? 'active' : ''} onClick={() => setSide('sell')}>
          Продажа
        </button>
      </div>
      <div className="field">
        <label className="label">Количество</label>
        <input
          className="input"
          type="number"
          min="0.01"
          step="any"
          inputMode="decimal"
          value={qty}
          onChange={(e) => {
            const v = e.target.value
            if (v === '' || /^\d*[.,]?\d*$/.test(v)) setQty(v.replace(',', '.'))
          }}
        />
      </div>
      <div className="card">
        <div className="row-between">
          <span className="muted">Тип заявки</span>
          <span>Рыночная</span>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
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
        {side === 'sell' ? (
          <div className="row-between" style={{ marginTop: 8 }}>
            <span className="muted">В портфеле</span>
            <span>{held}</span>
          </div>
        ) : null}
      </div>
      {err ? <p style={{ color: 'var(--red)' }}>{err}</p> : null}
      {blocked ? <p style={{ color: 'var(--red)', marginTop: 12 }}>{blocked}</p> : null}
      <button className="btn btn-primary" style={{ marginTop: 16 }} disabled={Boolean(blocked)} onClick={() => setConfirm(true)}>
        {side === 'sell' ? 'Продать' : 'Купить'}
      </button>

      {confirm && (
        <div className="sheet-backdrop" onClick={() => setConfirm(false)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <div className="sheet-handle" />
            <Mascot
              pose={blocked ? 'cry' : 'buy'}
              size={110}
              text={
                blocked ||
                `${side === 'buy' ? 'Покупка' : 'Продажа'} ${n} × ${inst.ticker} за ${money(cost)}. Подтверди.`
              }
            />
            <button className="btn btn-primary" disabled={loading || Boolean(blocked)} onClick={submit}>
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
