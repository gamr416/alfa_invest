import { type ReactNode } from 'react'

export function EmptyState({
  title = 'Ничего нет, но всё ещё впереди',
  text,
  action,
}: {
  title?: string
  text?: string
  action?: ReactNode
}) {
  return (
    <div className="empty-state">
      <img src="/mascot/alfa-crying.png" alt="" />
      <h2>{title}</h2>
      {text ? <p>{text}</p> : null}
      {action}
    </div>
  )
}
