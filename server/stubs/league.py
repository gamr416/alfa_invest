"""Practice league: 3 seeded friends + Anya's score. Not PnL."""

from __future__ import annotations

from . import portfolio

STREAK_CAP = 7
LESSON_PTS = 10
STREAK_PTS = 5
FIRST_CONSERVATIVE_PTS = 50
REPEAT_CONSERVATIVE_PTS = 20

FRIENDS: list[dict] = [
    {
        "name": "Кира",
        "points": 55,
        "hint": "21 · первый взнос · стрик 1",
    },
    {
        "name": "Лев",
        "points": 35,
        "hint": "24 · 2 урока · стрик 3",
    },
    {
        "name": "Марат",
        "points": 15,
        "hint": "19 · 1 урок · стрик 1",
    },
]

_progress: dict[str, dict] = {}


def save_progress(user_id: str, done: list[str], streak: int) -> dict:
    ids: list[str] = []
    seen: set[str] = set()
    for raw in done[:40]:
        item = str(raw).strip()[:48]
        if not item or item in seen:
            continue
        seen.add(item)
        ids.append(item)
    rec = {"done": ids, "streak": max(0, min(int(streak), 365))}
    _progress[user_id] = rec
    return rec


def get_progress(user_id: str) -> dict:
    rec = _progress.get(user_id)
    if rec:
        return rec
    return {"done": [], "streak": 0}


def score_anya(done: list[str], streak: int, first: bool, repeat: bool) -> int:
    lessons = len(done) * LESSON_PTS
    streak_part = min(max(streak, 0), STREAK_CAP) * STREAK_PTS
    first_part = FIRST_CONSERVATIVE_PTS if first else 0
    repeat_part = REPEAT_CONSERVATIVE_PTS if repeat else 0
    return lessons + streak_part + first_part + repeat_part


def _ru_lessons(n: int) -> str:
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        word = "урок"
    elif 2 <= n10 <= 4 and not (12 <= n100 <= 14):
        word = "урока"
    else:
        word = "уроков"
    return f"{n} {word}"


def anya_hint(done: list[str], streak: int, first: bool, repeat: bool) -> str:
    bits: list[str] = []
    if done:
        bits.append(_ru_lessons(len(done)))
    if streak:
        bits.append(f"стрик {streak}")
    if first:
        bits.append("первый взнос")
    if repeat:
        bits.append("повторный взнос")
    return " · ".join(bits) if bits else "ещё не начинала"


def table(user_id: str) -> dict:
    prog = get_progress(user_id)
    done = list(prog["done"])
    streak = int(prog["streak"])
    flags = portfolio.conservative_practice()
    pts = score_anya(done, streak, flags["first"], flags["repeat"])
    rows: list[dict] = [
        {
            "name": "Аня",
            "you": True,
            "points": pts,
            "hint": anya_hint(done, streak, flags["first"], flags["repeat"]),
        }
    ]
    for friend in FRIENDS:
        rows.append(
            {
                "name": friend["name"],
                "you": False,
                "points": friend["points"],
                "hint": friend["hint"],
            }
        )
    rows.sort(key=lambda r: (-int(r["points"]), 0 if r["you"] else 1, r["name"]))
    return {
        "metric_label": "Практика, не доходность",
        "rows": rows,
    }
