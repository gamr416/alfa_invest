type Pose = 'hello' | 'buy' | 'type'

const SRC: Record<Pose, string> = {
  hello: '/mascot/alfa-hello.png',
  buy: '/mascot/alfa-buy.png',
  type: '/mascot/alfa-sit-in-front-of-computer.png',
}

export function Mascot({
  pose,
  text,
  size = 120,
  stack = false,
}: {
  pose: Pose
  text?: string
  size?: number
  stack?: boolean
}) {
  return (
    <div className={`mascot-block${stack ? ' stack' : ''}`}>
      <img src={SRC[pose]} alt="" width={size} height={size} style={{ width: size }} />
      {text ? <div className="bubble">{text}</div> : null}
    </div>
  )
}
