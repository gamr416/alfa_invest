import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { money } from '../api'
import { Mascot } from '../components/Mascot'

const YEARS = [1, 3, 5, 10]
const RATES = [8, 12, 16]

function futureValue(principal: number, pmt: number, annualPct: number, years: number) {
  const months = years * 12
  const r = annualPct / 100 / 12
  if (r === 0) return principal + pmt * months
  const growth = Math.pow(1 + r, months)
  return principal * growth + pmt * ((growth - 1) / r)
}

function yearEnds(principal: number, pmt: number, annualPct: number, years: number) {
  const out: { year: number; value: number }[] = []
  for (let y = 1; y <= years; y++) {
    out.push({ year: y, value: futureValue(principal, pmt, annualPct, y) })
  }
  return out
}

export function CompoundPage() {
  const [start, setStart] = useState('1000')
  const [monthly, setMonthly] = useState('500')
  const [years, setYears] = useState(5)
  const [rate, setRate] = useState(12)

  const principal = Math.max(0, Number(start.replace(',', '.')) || 0)
  const pmt = Math.max(0, Number(monthly.replace(',', '.')) || 0)
  const contributed = principal + pmt * years * 12
  const fv = useMemo(() => futureValue(principal, pmt, rate, years), [principal, pmt, rate, years])
  const rows = useMemo(() => yearEnds(principal, pmt, rate, years), [principal, pmt, rate, years])
  const grown = fv - contributed

  return (
    <div className="page">
      <h1 className="page-title">Сложный процент</h1>
      <p className="page-sub">это если ставка не меняется — не прогноз</p>
      <Mascot
        pose="hello"
        size={100}
        text="Регулярный маленький взнос обычно сильнее редкого «всё сразу». Считаем модель, не обещание."
      />
      <div className="field">
        <label className="label">Стартовая сумма</label>
        <input className="input" value={start} onChange={(e) => setStart(e.target.value)} inputMode="decimal" />
      </div>
      <div className="field">
        <label className="label">Каждый месяц</label>
        <input className="input" value={monthly} onChange={(e) => setMonthly(e.target.value)} inputMode="decimal" />
      </div>
      <div className="section-label">Лет</div>
      <div className="chip-row">
        {YEARS.map((y) => (
          <button key={y} className={`chip${years === y ? ' active' : ''}`} onClick={() => setYears(y)}>
            {y}
          </button>
        ))}
      </div>
      <div className="section-label">Ставка % годовых · учебная</div>
      <div className="chip-row">
        {RATES.map((r) => (
          <button key={r} className={`chip${rate === r ? ' active' : ''}`} onClick={() => setRate(r)}>
            {r}%
          </button>
        ))}
      </div>
      <div className="card" style={{ marginTop: 16 }}>
        <div className="row-between">
          <span className="muted">В модели через {years} {years === 1 ? 'год' : years < 5 ? 'года' : 'лет'}</span>
          <strong>{money(fv, 0)}</strong>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
          <span className="muted">Внесено</span>
          <span>{money(contributed, 0)}</span>
        </div>
        <div className="row-between" style={{ marginTop: 8 }}>
          <span className="muted">Приросло в модели</span>
          <span className={grown >= 0 ? 'pnl-up' : 'pnl-down'}>{money(grown, 0)}</span>
        </div>
      </div>
      <div className="section-label">По годам</div>
      <div className="card" style={{ padding: '4px 16px' }}>
        {rows.map((row) => (
          <div key={row.year} className="list-item">
            <div className="muted">{row.year}-й год</div>
            <strong style={{ fontVariantNumeric: 'tabular-nums' }}>{money(row.value, 0)}</strong>
          </div>
        ))}
      </div>
      <p className="muted" style={{ fontSize: 13, marginTop: 14 }}>
        Ставка выдумана для учёбы. Цена фонда может и падать. Это не гарантия дохода.
      </p>
      <Link className="btn btn-primary" to="/instrument/LQDT">
        К спокойному фонду
      </Link>
    </div>
  )
}
