import { useEffect, useState } from 'react'
import { api, money } from '../api'
import { Mascot } from '../components/Mascot'
import { PhoneShell } from '../components/PhoneShell'

const GOALS = [
  { id: 'pillow', title: 'Подушка', sub: 'На чёрный день, спокойно' },
  { id: 'inflate', title: 'Инфляция', sub: 'Чтобы кэш на карте не таял' },
  { id: 'gadget', title: 'Гаджет', sub: 'Телефон или ноут через год' },
  { id: 'trip', title: 'Поездка', sub: 'Отложить на отпуск' },
]

const QUIZ = [
  {
    q: 'Когда могут понадобиться эти деньги?',
    opts: ['До 3 месяцев', 'Около года', 'Через несколько лет'],
  },
  {
    q: 'Что важнее сейчас?',
    opts: ['Не потерять', 'Небольшой рост без скачков', 'Максимум роста'],
  },
  {
    q: 'Сколько готов вложить сначала?',
    opts: ['100–500 ₽', 'До 2000 ₽', 'Больше'],
  },
]

export function Onboarding() {
  const [step, setStep] = useState(0)
  const [goal, setGoal] = useState('pillow')
  const [answers, setAnswers] = useState<number[]>([])
  const [why, setWhy] = useState('')
  const [loading, setLoading] = useState(false)
  const [name, setName] = useState('друг')
  const [cashback, setCashback] = useState(0)
  const [amount, setAmount] = useState('100')
  const [err, setErr] = useState('')

  useEffect(() => {
    api.me().then((m) => {
      setName(m.name)
      setCashback(m.cashback)
      if (m.cashback >= 100) setAmount(String(Math.min(500, Math.round(m.cashback))))
    })
  }, [])

  async function loadWhy() {
    setLoading(true)
    setErr('')
    const goalTitle = GOALS.find((g) => g.id === goal)?.title || goal
    const res = await api.chat(
      [
        {
          role: 'user',
          content: `Клиент выбрал цель «${goalTitle}». Ответы квиза: ${answers.join(',')}. Объясни, почему для первого шага подходит фонд денежного рынка LQDT, а не акции. Коротко.`,
        },
      ],
      'Продукт: LQDT — фонд денежного рынка, консервативный.',
    )
    setWhy(res.reply)
    setLoading(false)
    setStep(3)
  }

  async function finish() {
    setLoading(true)
    setErr('')
    try {
      await api.onboard(goal)
      const qty = Math.max(1, Math.floor(Number(amount) / 100.42))
      await api.order({ ticker: 'LQDT', side: 'buy', qty: Math.max(1, qty) })
      localStorage.setItem('alfa-onboarded', '1')
      window.location.href = '/'
    } catch (e) {
      setErr(e instanceof Error ? e.message : 'Ошибка')
      setLoading(false)
    }
  }

  async function skip() {
    await api.onboard(goal)
    localStorage.setItem('alfa-onboarded', '1')
    window.location.href = '/'
  }

  return (
    <PhoneShell tabs={false}>
      <div className="page">
        <div className="steps">
          {[0, 1, 2, 3, 4].map((i) => (
            <i key={i} className={i <= step ? 'on' : ''} />
          ))}
        </div>

        {step === 0 && (
          <>
            <Mascot
              pose="hello"
              size={148}
              stack
              text={`Привет, ${name}. Акции и риск ты уже знаешь. Не хватает первого шага — без страха и без обещаний заработка.`}
            />
            <p className="muted" style={{ marginBottom: 16 }}>
              На карте кэшбэк {money(cashback, 0)}. Хватит, чтобы начать от 100 ₽.
            </p>
            <button className="btn btn-primary" onClick={() => setStep(1)}>
              Начать
            </button>
          </>
        )}

        {step === 1 && (
          <>
            <Mascot pose="type" size={108} text="Зачем деньги? При дырявом доходе цель важнее витрины акций." />
            <div className="goal-grid">
              {GOALS.map((g) => (
                <button
                  key={g.id}
                  className={`goal-opt${goal === g.id ? ' active' : ''}`}
                  onClick={() => setGoal(g.id)}
                >
                  <strong>{g.title}</strong>
                  <span className="muted">{g.sub}</span>
                </button>
              ))}
            </div>
            <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setStep(2)}>
              Дальше
            </button>
          </>
        )}

        {step === 2 && (
          <>
            <Mascot pose="type" size={96} text="Три коротких вопроса — про горизонт, не про IQ." />
            <p className="muted">Учебные вопросы, не официальный тест Банка России.</p>
            {QUIZ.map((item, qi) => (
              <div key={item.q} className="card" style={{ marginTop: 10 }}>
                <div style={{ fontWeight: 600, marginBottom: 10, fontSize: 15 }}>{item.q}</div>
                <div className="goal-grid">
                  {item.opts.map((o, oi) => (
                    <button
                      key={o}
                      className={`goal-opt${answers[qi] === oi ? ' active' : ''}`}
                      onClick={() => {
                        const next = [...answers]
                        next[qi] = oi
                        setAnswers(next)
                      }}
                    >
                      {o}
                    </button>
                  ))}
                </div>
              </div>
            ))}
            <button
              className="btn btn-primary"
              style={{ marginTop: 16 }}
              disabled={answers.length < 3 || answers.some((a) => a === undefined)}
              onClick={loadWhy}
            >
              {loading ? 'Думаю…' : 'Показать, почему LQDT'}
            </button>
          </>
        )}

        {step === 3 && (
          <>
            <Mascot pose="hello" size={108} text={why || 'Фонд денежного рынка — спокойный первый шаг.'} />
            <div className="card">
              <div className="row-between">
                <div>
                  <div style={{ fontWeight: 700 }}>LQDT</div>
                  <div className="muted">Фонд денежного рынка</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontWeight: 600 }}>100,42 ₽</div>
                  <div className="muted">консервативно</div>
                </div>
              </div>
            </div>
            <div className="section-label">Не это, а рядом</div>
            <div className="card" style={{ padding: '4px 16px' }}>
              <div className="list-item">
                <div className="ticker-badge">SBGB</div>
                <div>
                  <div style={{ fontWeight: 600 }}>ОФЗ фонд</div>
                  <div className="muted">Чуть длиннее горизонт</div>
                </div>
              </div>
              <div className="list-item">
                <div className="ticker-badge">FXRU</div>
                <div>
                  <div style={{ fontWeight: 600 }}>Корп. облигации</div>
                  <div className="muted">Риск чуть выше</div>
                </div>
              </div>
            </div>
            <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setStep(4)}>
              К взносу
            </button>
          </>
        )}

        {step === 4 && (
          <>
            <Mascot pose="buy" size={140} stack text="Первый взнос. Можно с кэшбэка — без дыры в бюджете." />
            <div className="field">
              <label className="label">Сумма, ₽</label>
              <input className="input" value={amount} onChange={(e) => setAmount(e.target.value)} inputMode="numeric" />
            </div>
            {err ? <p style={{ color: 'var(--red)' }}>{err}</p> : null}
            <button className="btn btn-primary" disabled={loading} onClick={finish}>
              {loading ? 'Оформляю…' : 'Купить LQDT'}
            </button>
            <button className="btn btn-ghost" style={{ marginTop: 8 }} onClick={skip}>
              Пропустить в приложение
            </button>
          </>
        )}
      </div>
    </PhoneShell>
  )
}
