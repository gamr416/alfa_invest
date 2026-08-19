import data from './academy.json'
import { api } from './api'

export type Quiz = {
  q: string
  options: string[]
  correct: number
  why: string
}

export type AcademyNode = {
  id: string
  title: string
  minutes: number
  lane: 'center' | 'left' | 'right'
  locked: boolean
  requires: string[]
  requires_any: string[]
  text: string
  href?: string
  quiz?: Quiz
}

export type Glossary = Record<string, { term: string; def: string }>

const DONE_KEY = 'academy-done'
const STREAK_KEY = 'academy-streak'

export function readDone(): Record<string, boolean> {
  try {
    return JSON.parse(localStorage.getItem(DONE_KEY) || '{}')
  } catch {
    return {}
  }
}

export function markDone(id: string) {
  const prev = readDone()
  prev[id] = true
  localStorage.setItem(DONE_KEY, JSON.stringify(prev))
  bumpStreak()
  void syncProgress()
}

export function syncProgress() {
  const map = readDone()
  const done = Object.keys(map).filter((id) => map[id])
  const streak = readStreak()
  return api.academyProgress({ done, streak: streak.count }).catch(() => null)
}

function pad(n: number) {
  return String(n).padStart(2, '0')
}

export function localDay(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

function addDays(iso: string, delta: number) {
  const [y, m, day] = iso.split('-').map(Number)
  const dt = new Date(y, m - 1, day)
  dt.setDate(dt.getDate() + delta)
  return localDay(dt)
}

export type Streak = { count: number; lastDone: string }

export function readStreak(): Streak {
  try {
    const raw = JSON.parse(localStorage.getItem(STREAK_KEY) || '{"count":0,"lastDone":""}')
    return { count: Number(raw.count) || 0, lastDone: String(raw.lastDone || '') }
  } catch {
    return { count: 0, lastDone: '' }
  }
}

function writeStreak(s: Streak) {
  localStorage.setItem(STREAK_KEY, JSON.stringify(s))
}

/** If last lesson was before yesterday, flame dies. */
export function syncStreakOnVisit(): Streak {
  const s = readStreak()
  const today = localDay()
  const yday = addDays(today, -1)
  if (!s.lastDone || s.lastDone === today || s.lastDone === yday) return s
  const dead = { count: 0, lastDone: s.lastDone }
  writeStreak(dead)
  return dead
}

export function bumpStreak(): Streak {
  const s = readStreak()
  const today = localDay()
  const yday = addDays(today, -1)
  let next: Streak
  if (s.lastDone === today) next = s
  else if (s.lastDone === yday) next = { count: s.count + 1, lastDone: today }
  else next = { count: 1, lastDone: today }
  writeStreak(next)
  return next
}

export function isUnlocked(node: AcademyNode, done: Record<string, boolean>) {
  if (node.locked) return false
  const req = node.requires || []
  const any = node.requires_any || []
  const reqOk = req.every((id) => done[id])
  const anyOk = !any.length || any.some((id) => done[id])
  return reqOk && anyOk
}

export const LOCAL_ACADEMY: { nodes: AcademyNode[]; glossary: Glossary } = {
  nodes: data.nodes as AcademyNode[],
  glossary: data.glossary as Glossary,
}

export function pathRows(nodes: AcademyNode[] | undefined): AcademyNode[][] {
  const rows: AcademyNode[][] = []
  if (!nodes?.length) return rows
  let i = 0
  while (i < nodes.length) {
    const n = nodes[i]
    const next = nodes[i + 1]
    if (n.lane === 'left' && next?.lane === 'right') {
      rows.push([n, next])
      i += 2
    } else {
      rows.push([n])
      i += 1
    }
  }
  return rows
}
