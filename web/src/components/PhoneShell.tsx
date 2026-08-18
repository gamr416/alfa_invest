import { type ReactNode } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { NewsBell } from './NewsBell'
import { TabBar } from './TabBar'

function parentOf(path: string): string | null {
  if (path.startsWith('/instrument') || path.startsWith('/buy')) return '/catalog'
  if (path === '/agent' || path === '/operations' || path === '/analytics') {
    return path === '/agent' ? '/profile' : '/'
  }
  if (/^\/pulse\/.+/.test(path)) return '/pulse'
  if (/^\/learn\/.+/.test(path)) return '/learn'
  return null
}

export function PhoneShell({ children, tabs = true }: { children: ReactNode; tabs?: boolean }) {
  const now = new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  const loc = useLocation()
  const nav = useNavigate()
  const backTo = parentOf(loc.pathname)
  const isChat = loc.pathname === '/agent'

  return (
    <div className="app-stage">
        <div className="phone" id="phone-frame">
        <div className="phone-status">
          <span>{now}</span>
          <span>демо</span>
        </div>
        <header className="brand-bar">
          {backTo ? (
            <button className="brand-back" type="button" aria-label="Назад" onClick={() => nav(backTo)}>
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <path d="M15 5L8 12l7 7" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          ) : null}
          <span className="brand-title">АЛЬФА ИНВЕСТИЦИИ</span>
          <NewsBell />
        </header>
        <div className={`phone-body${tabs ? '' : ' no-tabs'}${isChat ? ' chat-mode' : ''}`}>{children}</div>
        {tabs ? <TabBar /> : null}
      </div>
    </div>
  )
}
