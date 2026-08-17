import { NavLink } from 'react-router-dom'

function Icon({ d }: { d: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d={d} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

const tabs = [
  { to: '/', label: 'Портфель', end: true, d: 'M4 19V5M10 19V9M16 19V3M20 19H3' },
  { to: '/catalog', label: 'Каталог', d: 'M4 6h16M4 12h16M4 18h10' },
  { to: '/pulse', label: 'Пульс', d: 'M4 12h3l2-6 4 12 2-6h5' },
  { to: '/learn', label: 'Учёба', d: 'M4 19V6l8-3 8 3v13M4 10l8 3 8-3' },
  { to: '/profile', label: 'Профиль', d: 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 20a8 8 0 0116 0' },
]

export function TabBar() {
  return (
    <nav className="tabbar">
      {tabs.map((t) => (
        <NavLink key={t.to} to={t.to} end={t.end} className={({ isActive }) => `tab${isActive ? ' active' : ''}`}>
          <Icon d={t.d} />
          {t.label}
        </NavLink>
      ))}
    </nav>
  )
}
