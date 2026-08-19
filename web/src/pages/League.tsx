import { useEffect, useState } from 'react'
import { api, type League } from '../api'
import { LeagueTable } from '../components/LeagueTable'
import { syncProgress } from '../academyProgress'

export function LeaguePage() {
  const [league, setLeague] = useState<League | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    syncProgress()
      .then(() => api.league())
      .then((data) => {
        if (alive) setLeague(data)
      })
      .catch(() => {
        if (alive) setLeague(null)
      })
      .finally(() => {
        if (alive) setLoading(false)
      })
    return () => {
      alive = false
    }
  }, [])

  return (
    <div className="page page-narrow">
      <h1 className="page-title">Лига практики</h1>
      <p className="page-sub">{league?.metric_label || 'Практика, не доходность'}</p>
      <LeagueTable data={league} loading={loading} />
      <p className="league-rules">
        Урок +10. Стрик +5 за день, максимум 7 дней. Первый взнос в conservative +50, повторный +20
        один раз. Не за доходность и не за оборот.
      </p>
    </div>
  )
}
