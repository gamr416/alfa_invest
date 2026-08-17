const DAYS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

export type Candle = { o: number; h: number; l: number; c: number }

function dayLabels(n: number) {
  const now = new Date()
  const out: string[] = []
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date(now)
    d.setDate(now.getDate() - i)
    out.push(String(d.getDate()))
  }
  return out
}

export function PriceChart({ candles, width = 340, height = 240 }: { candles: Candle[]; width?: number; height?: number }) {
  if (candles.length < 2) return null
  const padL = 44
  const padR = 8
  const padT = 12
  const padB = 28
  const w = width - padL - padR
  const h = height - padT - padB
  const min = Math.min(...candles.map((c) => c.l))
  const max = Math.max(...candles.map((c) => c.h))
  const span = max - min || 1
  const y = (v: number) => padT + h - ((v - min) / span) * h
  const slot = w / candles.length
  const bodyW = Math.max(3, slot * 0.55)
  const ticks = 4
  const yTicks = Array.from({ length: ticks + 1 }, (_, i) => min + (span * i) / ticks)
  const labelEvery = Math.max(1, Math.floor((candles.length - 1) / 4))
  const labels = dayLabels(candles.length)
  void DAYS

  return (
    <svg className="price-chart" width="100%" height={height} viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="xMidYMid meet">
      {yTicks.map((t) => {
        const yy = y(t)
        return (
          <g key={t}>
            <line x1={padL} x2={width - padR} y1={yy} y2={yy} stroke="#EAEAEA" />
            <text x={padL - 6} y={yy + 4} textAnchor="end" className="chart-lab">
              {t.toFixed(t < 2 ? 3 : 1)}
            </text>
          </g>
        )
      })}
      {candles.map((c, i) => {
        const cx = padL + slot * i + slot / 2
        const up = c.c >= c.o
        const color = up ? '#1a9e4a' : '#EF3124'
        const yO = y(c.o)
        const yC = y(c.c)
        const top = Math.min(yO, yC)
        const bodyH = Math.max(1.5, Math.abs(yC - yO))
        return (
          <g key={i}>
            <line x1={cx} x2={cx} y1={y(c.h)} y2={y(c.l)} stroke={color} strokeWidth="1" />
            <rect x={cx - bodyW / 2} y={top} width={bodyW} height={bodyH} fill={color} />
          </g>
        )
      })}
      {candles.map((_, i) =>
        i % labelEvery === 0 || i === candles.length - 1 ? (
          <text key={`l${i}`} x={padL + slot * i + slot / 2} y={height - 8} textAnchor="middle" className="chart-lab">
            {labels[i]}
          </text>
        ) : null,
      )}
    </svg>
  )
}
