import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { Mascot } from '../components/Mascot'

type Lesson = { id: string; title: string; minutes: number; done: boolean; text: string }

export function AcademyPage() {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [done] = useState<Record<string, boolean>>(() => {
    try {
      return JSON.parse(localStorage.getItem('academy-done') || '{}')
    } catch {
      return {}
    }
  })

  useEffect(() => {
    api.academy().then((r) => setLessons(r.lessons))
  }, [])

  const finished = lessons.filter((l) => done[l.id]).length
  const pctDone = lessons.length ? Math.round((finished / lessons.length) * 100) : 0

  return (
    <div className="page">
      <h1 className="page-title">Учёба</h1>
      <p className="page-sub">Микроуроки без давления</p>
      <Mascot pose="hello" size={110} text="2–3 минуты — и уже понятнее, зачем риск и горизонт." />
      <div className="card">
        <div className="row-between">
          <span>Прогресс курса</span>
          <strong>
            {finished}/{lessons.length} · {pctDone}%
          </strong>
        </div>
        <div className="progress">
          <span style={{ width: `${pctDone}%` }} />
        </div>
      </div>
      <div className="tiles">
        <Link className="tile" to="/agent">
          <span className="muted">Спросить</span>
          <strong>Агент</strong>
        </Link>
        <Link className="tile" to="/pulse">
          <span className="muted">Почитать</span>
          <strong>Пульс</strong>
        </Link>
      </div>
      <div className="section-label">Уроки</div>
      <div className="card" style={{ padding: '4px 16px' }}>
      {lessons.map((l) => (
        <Link key={l.id} to={`/learn/${l.id}`} className="list-item">
          <div className={`ticker-badge${done[l.id] ? ' safe' : ''}`}>{done[l.id] ? 'ок' : l.minutes + 'м'}</div>
          <div>
            <div style={{ fontWeight: 600 }}>{l.title}</div>
            <div className="muted">{done[l.id] ? 'Пройдено' : `${l.minutes} мин · микроурок`}</div>
          </div>
        </Link>
      ))}
      </div>
    </div>
  )
}

export function LessonPage() {
  const { id = '' } = useParams()
  const [lesson, setLesson] = useState<Lesson | null>(null)

  useEffect(() => {
    api.academy().then((r) => setLesson(r.lessons.find((l) => l.id === id) || null))
  }, [id])

  function markDone() {
    const prev = JSON.parse(localStorage.getItem('academy-done') || '{}')
    prev[id] = true
    localStorage.setItem('academy-done', JSON.stringify(prev))
  }

  if (!lesson) return <div className="page muted">Загрузка…</div>

  return (
    <div className="page">
      <Mascot pose="hello" size={100} text={lesson.title} />
      <p style={{ fontSize: 16, lineHeight: 1.55 }}>{lesson.text}</p>
      <Link className="btn btn-primary" to="/learn" onClick={markDone}>
        Понятно
      </Link>
    </div>
  )
}
