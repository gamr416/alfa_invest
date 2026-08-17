import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, money, type Me } from '../api'

export function ProfilePage() {
  const [me, setMe] = useState<Me | null>(null)
  const [ollama, setOllama] = useState(false)

  useEffect(() => {
    api.me().then(setMe)
    api
      .health()
      .then((h) => setOllama(!!h.ollama?.available))
      .catch(() => setOllama(false))
  }, [])

  if (!me) return <div className="page muted">Загрузка…</div>

  return (
    <div className="page">
      <h1 className="page-title">{me.name}</h1>
      <p className="page-sub">{me.age} лет · когорта 18–24</p>
      <div className="section-label">Счёт и карта</div>
      <div className="card">
        <div className="stat-row row-between">
          <span className="muted">Карта</span>
          <strong style={{ fontVariantNumeric: 'tabular-nums' }}>{money(me.balance)}</strong>
        </div>
        <div className="stat-row row-between">
          <span className="muted">Кэшбэк</span>
          <strong style={{ fontVariantNumeric: 'tabular-nums' }}>{money(me.cashback)}</strong>
        </div>
        <div className="stat-row row-between">
          <span className="muted">Копилка</span>
          <strong style={{ fontVariantNumeric: 'tabular-nums' }}>{money(me.piggy)}</strong>
        </div>
        <div className="stat-row row-between">
          <span className="muted">Инвестсчёт</span>
          <strong>демо · paper</strong>
        </div>
      </div>

      <div className="tiles">
        <Link className="tile" to="/operations">
          <span className="muted">История</span>
          <strong>Операции</strong>
        </Link>
        <Link className="tile" to="/analytics">
          <span className="muted">Доли</span>
          <strong>Аналитика</strong>
        </Link>
      </div>

      <div className="section-label">Ассистент</div>
      <div className="card">
        <div className="row-between">
          <span>bonsai-27b</span>
          <strong style={{ color: ollama ? 'var(--black)' : 'var(--red)' }}>{ollama ? 'онлайн' : 'офлайн'}</strong>
        </div>
        <p className="muted" style={{ marginTop: 8 }}>
          Тариф «Агент»: комиссия за объяснения. Демо-пункт, без списания.
        </p>
        <Link className="btn btn-primary" style={{ marginTop: 14 }} to="/agent">
          Открыть чат
        </Link>
      </div>

      <Link className="btn btn-ghost" style={{ marginTop: 12 }} to="/onboarding">
        Туториал снова
      </Link>
      <div className="section-label">Документы</div>
      <div className="card" style={{ padding: '4px 16px' }}>
        <div className="list-item">
          <div>
            <div style={{ fontWeight: 600 }}>Тариф «Агент»</div>
            <div className="muted">Комиссия за объяснения · демо, 0 ₽</div>
          </div>
        </div>
        <div className="list-item">
          <div>
            <div style={{ fontWeight: 600 }}>Маржа и крипта</div>
            <div className="muted">Выключены. В продукт не входят.</div>
          </div>
        </div>
        <div className="list-item">
          <div>
            <div style={{ fontWeight: 600 }}>Отчёт брокера</div>
            <div className="muted">В MVP нет. Появится на живом API.</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export function AgentPage() {
  const [msgs, setMsgs] = useState<{ role: 'user' | 'assistant'; content: string }[]>([
    {
      role: 'assistant',
      content: 'Привет. Могу объяснить риск, горизонт и зачем новичкам фонд денежного рынка. Спроси что угодно про первый шаг.',
    },
  ])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const logRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: 'smooth' })
  }, [msgs, loading])

  async function send() {
    if (!text.trim() || loading) return
    const next = [...msgs, { role: 'user' as const, content: text.trim() }]
    setMsgs(next)
    setText('')
    setLoading(true)
    const res = await api.chat(next.map((m) => ({ role: m.role, content: m.content })))
    setMsgs([...next, { role: 'assistant', content: res.reply }])
    setLoading(false)
  }

  return (
    <div className="chat-screen">
      <div className="chat-log" ref={logRef}>
        {msgs.map((m, i) => {
          const isBot = m.role !== 'user'
          const showAvatar = isBot && (i === msgs.length - 1 || msgs[i + 1]?.role === 'user') && !loading
          return (
            <div key={i} className={`msg-row ${isBot ? 'bot' : 'user'}`}>
              {isBot ? (
                <img
                  className={`chat-avatar${showAvatar ? '' : ' ghost'}`}
                  src="/mascot/alfa-avatar.webp"
                  alt=""
                />
              ) : null}
              <div className={`msg ${isBot ? 'bot' : 'user'}`}>{m.content}</div>
            </div>
          )
        })}
        {loading ? (
          <div className="msg-row bot">
            <img className="chat-avatar" src="/mascot/alfa-avatar.webp" alt="" />
            <div className="msg bot typing">печатает…</div>
          </div>
        ) : null}
      </div>
      <div className="chat-compose">
        <input
          className="input"
          placeholder="Сообщение"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
        />
        <button className="btn btn-primary" onClick={send} disabled={loading} aria-label="Отправить">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3 11l18-8-8 18-2-7-8-3z" />
          </svg>
        </button>
      </div>
    </div>
  )
}
