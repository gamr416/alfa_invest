export function Sparkline({ points, width = 64, height = 28 }: { points: number[]; width?: number; height?: number }) {
  if (!points.length) return <svg className="spark" width={width} height={height} />
  const min = Math.min(...points)
  const max = Math.max(...points)
  const span = max - min || 1
  const d = points
    .map((v, i) => {
      const x = (i / (points.length - 1)) * width
      const y = height - ((v - min) / span) * (height - 4) - 2
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`
    })
    .join(' ')
  return (
    <svg className="spark" width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <path d={d} fill="none" stroke="#111111" strokeWidth="1.5" />
    </svg>
  )
}
