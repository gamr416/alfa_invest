import { useEffect, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { api } from './api'
import { PhoneShell } from './components/PhoneShell'
import { AcademyPage, LessonPage } from './pages/Academy'
import { CompoundPage } from './pages/Compound'
import { BuyPage } from './pages/Buy'
import { CatalogPage } from './pages/Catalog'
import { InstrumentPage } from './pages/Instrument'
import { Onboarding } from './pages/Onboarding'
import { AnalyticsPage, OperationsPage } from './pages/Operations'
import { PortfolioPage } from './pages/Portfolio'
import { AgentPage, ProfilePage } from './pages/Profile'
import { PulsePage, PulsePostPage } from './pages/Pulse'

function ShellRoutes() {
  const loc = useLocation()
  const noTabs =
    loc.pathname.startsWith('/buy') ||
    loc.pathname.startsWith('/instrument') ||
    loc.pathname.startsWith('/agent') ||
    loc.pathname.startsWith('/operations') ||
    loc.pathname.startsWith('/analytics') ||
    /^\/pulse\/.+/.test(loc.pathname) ||
    /^\/learn\/.+/.test(loc.pathname)
  return (
    <PhoneShell tabs={!noTabs}>
      <Routes>
        <Route path="/" element={<PortfolioPage />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/instrument/:ticker" element={<InstrumentPage />} />
        <Route path="/buy/:ticker" element={<BuyPage />} />
        <Route path="/pulse" element={<PulsePage />} />
        <Route path="/pulse/:id" element={<PulsePostPage />} />
        <Route path="/learn" element={<AcademyPage />} />
        <Route path="/learn/compound" element={<CompoundPage />} />
        <Route path="/learn/:id" element={<LessonPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/agent" element={<AgentPage />} />
        <Route path="/operations" element={<OperationsPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </PhoneShell>
  )
}

function AgeBlocked() {
  return (
    <div className="app-stage">
      <div className="phone-shell">
        <div className="page">
          <h1 className="page-title">Пока нельзя</h1>
          <p className="page-sub">Демо для 18+. Младше 18 сюда не пускаем.</p>
        </div>
      </div>
    </div>
  )
}

function Gate() {
  const [ready, setReady] = useState(false)
  const [needOnboard, setNeedOnboard] = useState(true)
  const [blocked, setBlocked] = useState(false)

  useEffect(() => {
    const local = localStorage.getItem('alfa-onboarded') === '1'
    Promise.all([
      api.me().catch(() => null),
      api.portfolio().catch(() => null),
    ]).then(([me, p]) => {
      if (me && me.age < 18) {
        setBlocked(true)
        setReady(true)
        return
      }
      setNeedOnboard(!(p?.onboarded || local))
      setReady(true)
    })
  }, [])

  if (!ready) {
    return (
      <div className="app-stage">
        <div className="muted">Загрузка…</div>
      </div>
    )
  }

  if (blocked) return <AgeBlocked />

  return (
    <Routes>
      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/*" element={needOnboard ? <Navigate to="/onboarding" replace /> : <ShellRoutes />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Gate />
    </BrowserRouter>
  )
}
