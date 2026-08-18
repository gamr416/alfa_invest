import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type PulsePost } from '../api'

const SEEN_KEY = 'alfa-news-seen'

export function NewsBell() {
  const [items, setItems] = useState<PulsePost[]>([])
  const [open, setOpen] = useState(false)
  const [seen, setSeen] = useState<string[]>(() => {
    try {
      const raw = localStorage.getItem(SEEN_KEY)
      return raw ? (JSON.parse(raw) as string[]) : []
    } catch {
      return []
    }
  })
  const wrap = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const load = () =>
      api.pulse().then((r) => setItems(r.items.filter((p) => p.tag === 'рынок')))
    load()
    const id = setInterval(load, 60_000)
    return () => clearInterval(id)
  }, [])

  useEffect(() => {
    if (!open) return
    const onDoc = (e: MouseEvent) => {
      if (!wrap.current?.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', onDoc)
    return () => document.removeEventListener('mousedown', onDoc)
  }, [open])

  const unread = items.filter((p) => !seen.includes(p.id)).length

  const toggle = () => {
    setOpen((v) => !v)
    if (!open) {
      const ids = items.map((p) => p.id)
      setSeen(ids)
      localStorage.setItem(SEEN_KEY, JSON.stringify(ids))
    }
  }

  return (
    <div className="news-bell" ref={wrap}>
      <button type="button" className="news-bell-btn" aria-label="Уведомления" onClick={toggle}>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M13.73 21a2 2 0 01-3.46 0" strokeLinecap="round" />
        </svg>
        {unread > 0 ? <span className="news-bell-dot">{unread > 9 ? '9+' : unread}</span> : null}
      </button>
      {open ? (
        <div className="news-bell-panel">
          {items.length === 0 ? (
            <p className="muted" style={{ margin: 0, fontSize: 13 }}>
              Пока тихо. Демо-новость появится не каждую минуту.
            </p>
          ) : (
            items.map((p) => (
              <Link
                key={p.id}
                to={`/pulse/${p.id}`}
                state={p}
                className="news-bell-item"
                onClick={() => setOpen(false)}
              >
                <strong>{p.title}</strong>
                <span>{p.tickers?.join(', ')}</span>
              </Link>
            ))
          )}
        </div>
      ) : null}
    </div>
  )
}
