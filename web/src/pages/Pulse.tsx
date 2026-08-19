import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { api, type PulsePost } from '../api'
import { EmptyState } from '../components/EmptyState'
import { Mascot } from '../components/Mascot'

export function PulsePage() {
  const [items, setItems] = useState<PulsePost[]>([])
  const [tag, setTag] = useState('все')
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const load = () =>
      api.pulse().then((r) => {
        setItems(r.items)
        setReady(true)
      })
    load()
    const id = setInterval(load, 60_000)
    return () => clearInterval(id)
  }, [])

  const tags = ['все', ...Array.from(new Set(items.map((i) => i.tag)))]
  const shown = tag === 'все' ? items : items.filter((i) => i.tag === tag)

  return (
    <div className="page">
      <h1 className="page-title">Пульс</h1>
      <p className="page-sub">{items.length} материалов · без торговых сигналов</p>
      <Mascot pose="hello" size={92} text="Это лента обучения. Не призыв покупать." />
      <div className="chip-row">
        {tags.map((t) => (
          <button key={t} className={`chip${tag === t ? ' active' : ''}`} onClick={() => setTag(t)}>
            {t}
          </button>
        ))}
      </div>
      {!ready ? (
        <p className="muted">Загрузка…</p>
      ) : shown.length === 0 ? (
        <EmptyState text="В этой ленте пока тихо. Загляни позже или смени фильтр." />
      ) : (
        <div className="feed-list">
        {shown.map((p) => (
        <Link key={p.id} to={`/pulse/${p.id}`} state={p} className="feed-card">
          <div className="stripe" />
          <div className="body">
            <div
              className="muted"
              style={{
                marginBottom: 6,
                letterSpacing: '0.04em',
                textTransform: 'uppercase',
                fontSize: 11,
                fontWeight: 600,
              }}
            >
              {p.author} · {p.tag}
            </div>
            <div style={{ fontWeight: 700, marginBottom: 6, letterSpacing: '-0.02em' }}>{p.title}</div>
            <div style={{ fontSize: 14, color: 'var(--muted)' }}>{p.body}</div>
          </div>
        </Link>
        ))}
        </div>
      )}
    </div>
  )
}

export function PulsePostPage() {
  const { id } = useParams()
  const loc = useLocation()
  const st = loc.state as PulsePost | null
  const [post, setPost] = useState<PulsePost | null>(st?.title ? st : null)

  useEffect(() => {
    if (post) return
    api.pulse().then((r) => setPost(r.items.find((i) => i.id === id) || r.items[0] || null))
  }, [id, post])

  if (!post) return <div className="page muted">Загрузка…</div>
  return (
    <div className="page page-prose">
      <h1 className="page-title" style={{ fontSize: 22 }}>
        {post.title}
      </h1>
      <p style={{ fontSize: 16, lineHeight: 1.55 }}>{post.body}</p>
      <Link className="btn btn-ghost" style={{ marginTop: 12 }} to="/learn">
        К урокам
      </Link>
    </div>
  )
}
