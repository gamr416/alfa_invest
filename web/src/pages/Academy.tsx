import { Fragment, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { Link, Navigate, useParams } from 'react-router-dom'
import {
  LOCAL_ACADEMY,
  type Glossary,
  type Quiz,
  isUnlocked,
  markDone,
  pathRows,
  readDone,
  syncStreakOnVisit,
} from '../academyProgress'

export function AcademyPage() {
  const nodes = LOCAL_ACADEMY.nodes
  const done = readDone()
  const streak = syncStreakOnVisit()

  const rows = useMemo(() => pathRows(nodes), [nodes])
  const open = nodes.filter((n) => !n.locked)
  const finished = open.filter((n) => done[n.id]).length
  const currentId = open.find((n) => isUnlocked(n, done) && !done[n.id])?.id
  const flameOn = streak.count > 0

  return (
    <div className="page">
      <div className="academy-head">
        <h1 className="page-title">Учёба</h1>
        <div className={`streak${flameOn ? '' : ' dead'}`}>
          <Flame on={flameOn} />
          <span>{streak.count}</span>
        </div>
      </div>
      <p className="page-sub">
        Сначала предыдущий урок. На развилке хватит одной ветки.
        {open.length ? ` ${finished}/${open.length}` : ''}
      </p>
      <div className="path">
        {rows.map((row, ri) => (
          <Fragment key={ri}>
            {ri > 0 && <div className={`path-stem${row.some((n) => isUnlocked(n, done) || done[n.id]) ? ' on' : ''}`} />}
            <div className={row.length > 1 ? 'path-fork' : 'path-row'}>
              {row.map((n) => {
                const openNode = isUnlocked(n, done)
                const cls = [
                  'path-node',
                  done[n.id] ? 'done' : '',
                  n.id === currentId ? 'current' : '',
                  n.locked || !openNode ? 'locked' : '',
                ]
                  .filter(Boolean)
                  .join(' ')
                const inner = (
                  <>
                    <div className="path-dot" />
                    <div className="path-node-title">{n.title}</div>
                    <div className="muted">
                      {n.locked ? 'позже' : done[n.id] ? 'пройдено' : `${n.minutes} мин`}
                    </div>
                  </>
                )
                if (n.locked || !openNode) {
                  return (
                    <div key={n.id} className={cls}>
                      {inner}
                    </div>
                  )
                }
                return (
                  <Link key={n.id} className={cls} to={`/learn/${n.id}`}>
                    {inner}
                  </Link>
                )
              })}
            </div>
          </Fragment>
        ))}
      </div>
    </div>
  )
}

function Flame({ on }: { on: boolean }) {
  return (
    <svg width="18" height="22" viewBox="0 0 18 22" aria-hidden>
      <path
        d="M9 1c1.2 3.2-1.2 5-1.2 7.2 0 1.4 1 2.4 2.2 2.4 2.6 0 4.8-2.6 4.8-6.2 2.2 2.4 3.2 4.8 3.2 7.4 0 5-3.6 9-9 9s-9-4-9-9C0 7.4 4.2 3.2 9 1z"
        fill={on ? 'var(--red)' : '#cfcfcf'}
      />
    </svg>
  )
}

export function LessonPage() {
  const { id = '' } = useParams()
  const [term, setTerm] = useState<string | null>(null)
  const [pick, setPick] = useState<number | null>(null)
  const done = readDone()
  const node = LOCAL_ACADEMY.nodes.find((n) => n.id === id) || null
  const glossary = LOCAL_ACADEMY.glossary
  const frame = document.getElementById('app-shell')

  if (!node) return <div className="page muted">Нет такого урока</div>
  if (node.locked || !isUnlocked(node, done)) return <Navigate to="/learn" replace />

  const g = term ? glossary[term] : null
  const quizOk = !node.quiz || pick === node.quiz.correct || !!done[id]
  const paras = node.text.split(/\n\n/)

  return (
    <div className="page page-prose">
      <p className="muted">{node.minutes} мин</p>
      <h1 className="page-title" style={{ fontSize: 22 }}>
        {node.title}
      </h1>
      {paras.map((p, i) => (
        <p key={i} className="lesson-text">
          <LessonBody text={p} glossary={glossary} onTerm={setTerm} />
        </p>
      ))}
      {node.quiz ? <LessonQuiz quiz={node.quiz} pick={pick} onPick={setPick} /> : null}
      {node.href ? (
        <Link
          className="btn btn-primary"
          to={quizOk ? node.href : '#'}
          onClick={(e) => {
            if (!quizOk) e.preventDefault()
            else markDone(id)
          }}
        >
          К калькулятору
        </Link>
      ) : (
        <Link
          className="btn btn-primary"
          to="/learn"
          onClick={(e) => {
            if (!quizOk) e.preventDefault()
            else markDone(id)
          }}
        >
          {quizOk ? 'Понятно' : 'Сначала задание'}
        </Link>
      )}
      {g && frame
        ? createPortal(
            <div className="term-sheet" onClick={() => setTerm(null)} role="presentation">
              <div className="term-card" onClick={(e) => e.stopPropagation()}>
                <strong>{g.term}</strong>
                <p className="muted" style={{ margin: '8px 0 0' }}>
                  {g.def}
                </p>
                <button type="button" className="btn btn-ghost" style={{ marginTop: 12 }} onClick={() => setTerm(null)}>
                  Закрыть
                </button>
              </div>
            </div>,
            frame,
          )
        : null}
    </div>
  )
}

function LessonQuiz({
  quiz,
  pick,
  onPick,
}: {
  quiz: Quiz
  pick: number | null
  onPick: (i: number) => void
}) {
  return (
    <div className="quiz">
      <p className="quiz-q">{quiz.q}</p>
      {quiz.options.map((opt, i) => {
        let cls = 'quiz-opt'
        if (pick !== null) {
          if (i === quiz.correct) cls += ' ok'
          else if (i === pick) cls += ' bad'
        }
        return (
          <button key={i} type="button" className={cls} onClick={() => onPick(i)}>
            {opt}
          </button>
        )
      })}
      {pick !== null ? <p className="muted" style={{ margin: '10px 0 0' }}>{quiz.why}</p> : null}
    </div>
  )
}

function LessonBody({
  text,
  glossary,
  onTerm,
}: {
  text: string
  glossary: Glossary
  onTerm: (id: string) => void
}) {
  const parts = text.split(/(\[\[[^\]]+\]\])/g)
  return (
    <>
      {parts.map((p, i) => {
        const m = p.match(/^\[\[([^\]]+)\]\]$/)
        if (!m) return <Fragment key={i}>{p}</Fragment>
        const id = m[1]
        const label = glossary[id]?.term || id
        return (
          <button key={i} type="button" className="term" onClick={() => onTerm(id)}>
            {label}
          </button>
        )
      })}
    </>
  )
}
