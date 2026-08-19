import { Link } from 'react-router-dom'
import type { League, LeagueRow } from '../api'

function initial(name: string) {
  return name.trim().slice(0, 1).toUpperCase() || '?'
}

function Row({ row, rank, i }: { row: LeagueRow; rank: number; i: number }) {
  return (
    <li className={`league-row${row.you ? ' you' : ''}`} style={{ ['--i' as string]: i }}>
      <span className="league-rank">{rank}</span>
      <span className="league-ava" aria-hidden>
        {initial(row.name)}
      </span>
      <div className="league-who">
        <div className="league-name">
          {row.name}
          {row.you ? <span className="league-you-tag">ты</span> : null}
        </div>
        <div className="league-hint">{row.hint}</div>
      </div>
      <strong className="league-pts">{row.points}</strong>
    </li>
  )
}

export function LeagueTable({
  data,
  loading,
}: {
  data: League | null
  loading: boolean
}) {
  return (
    <section className="league" aria-label="Таблица лиги">
      <div className="league-cols" aria-hidden>
        <span>#</span>
        <span />
        <span>кто</span>
        <span>очки</span>
      </div>
      {loading && !data ? (
        <ol className="league-table" aria-hidden>
          {[0, 1, 2, 3].map((i) => (
            <li key={i} className="league-row skel" style={{ ['--i' as string]: i }}>
              <span className="league-skel rank" />
              <span className="league-skel ava" />
              <span className="league-skel name" />
              <span className="league-skel pts" />
            </li>
          ))}
        </ol>
      ) : data ? (
        <ol className="league-table">
          {data.rows.map((row, i) => (
            <Row key={row.you ? 'you' : row.name} row={row} rank={i + 1} i={i} />
          ))}
        </ol>
      ) : (
        <p className="muted">Таблица сейчас недоступна. Уроки на экране учёбы на месте.</p>
      )}
    </section>
  )
}

export function LeaguePeek({ data }: { data: League | null }) {
  const place = data ? data.rows.findIndex((r) => r.you) + 1 : 0
  const you = data?.rows.find((r) => r.you)
  return (
    <Link className="league-peek" to="/learn/league">
      <div>
        <div className="section-label" style={{ marginTop: 0 }}>
          Лига практики
        </div>
        <strong>{you ? `${place} место · ${you.points}` : 'Открыть таблицу'}</strong>
        <div className="muted">{data?.metric_label || 'Практика, не доходность'}</div>
      </div>
      <span className="league-peek-go" aria-hidden>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M9 6l6 6-6 6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </span>
    </Link>
  )
}
