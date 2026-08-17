"""Stub: market instruments, quotes, order book, sparklines."""

from __future__ import annotations

import hashlib
import math
from typing import Any


INSTRUMENTS: list[dict[str, Any]] = [
    {
        "ticker": "LQDT",
        "name": "Фонд денежного рынка",
        "type": "etf",
        "price": 100.42,
        "change_pct": 0.02,
        "currency": "RUB",
        "conservative": True,
        "sector": "Деньги",
        "desc": "Короткие облигации и депозиты. Низкий риск для первого шага.",
    },
    {
        "ticker": "SBGB",
        "name": "Облигации федерального займа",
        "type": "etf",
        "price": 112.8,
        "change_pct": -0.15,
        "currency": "RUB",
        "conservative": True,
        "sector": "Облигации",
        "desc": "ОФЗ в одном фонде. Подходит под подушку на 1–3 года.",
    },
    {
        "ticker": "SBER",
        "name": "Сбербанк",
        "type": "stock",
        "price": 278.5,
        "change_pct": 1.24,
        "currency": "RUB",
        "conservative": False,
        "sector": "Финансы",
        "desc": "Крупный банк. Цена может сильно меняться день ото дня.",
    },
    {
        "ticker": "GAZP",
        "name": "Газпром",
        "type": "stock",
        "price": 142.1,
        "change_pct": -0.68,
        "currency": "RUB",
        "conservative": False,
        "sector": "Энергетика",
        "desc": "Энергетическая компания. Риск выше, чем у фондов.",
    },
    {
        "ticker": "YDEX",
        "name": "Яндекс",
        "type": "stock",
        "price": 3850.0,
        "change_pct": 2.1,
        "currency": "RUB",
        "conservative": False,
        "sector": "Технологии",
        "desc": "IT-компания. Волатильность высокая.",
    },
    {
        "ticker": "TMOS",
        "name": "Мосбиржа полный рынок",
        "type": "etf",
        "price": 6.12,
        "change_pct": 0.45,
        "currency": "RUB",
        "conservative": False,
        "sector": "Индекс",
        "desc": "Корзина акций рынка. Средний риск.",
    },
    {
        "ticker": "FXRU",
        "name": "Корпоративные облигации",
        "type": "etf",
        "price": 980.0,
        "change_pct": 0.08,
        "currency": "RUB",
        "conservative": True,
        "sector": "Облигации",
        "desc": "Корп. облигации. Чуть выше риска, чем денежный рынок.",
    },
    {
        "ticker": "VTBR",
        "name": "ВТБ",
        "type": "stock",
        "price": 0.0825,
        "change_pct": -1.1,
        "currency": "RUB",
        "conservative": False,
        "sector": "Финансы",
        "desc": "Банк. Низкая цена за штуку, но риск как у акций.",
    },
]


def _seed(ticker: str) -> int:
    return int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)


def list_instruments(q: str | None = None, kind: str | None = None) -> list[dict]:
    items = INSTRUMENTS
    if kind == "conservative":
        items = [i for i in items if i["conservative"]]
    elif kind and kind != "all":
        items = [i for i in items if i["type"] == kind]
    if q:
        ql = q.lower()
        items = [i for i in items if ql in i["ticker"].lower() or ql in i["name"].lower()]
    return items


def get_instrument(ticker: str) -> dict | None:
    for i in INSTRUMENTS:
        if i["ticker"].upper() == ticker.upper():
            return i
    return None


def sparkline(ticker: str, points: int = 24) -> list[float]:
    return [c["c"] for c in candles(ticker, points)]


def candles(ticker: str, n: int = 24) -> list[dict]:
    inst = get_instrument(ticker)
    if not inst:
        return []
    base = float(inst["price"])
    s = _seed(ticker)
    out: list[dict] = []
    close = base * 0.97
    for i in range(n):
        wobble = math.sin((s % 97) / 10 + i / 3) * 0.008
        drift = ((s >> (i % 8)) & 1) * 0.003 - 0.0015
        o = close
        c = round(o * (1 + wobble + drift), 4)
        hi = round(max(o, c) * (1 + 0.004 + (i % 3) * 0.001), 4)
        lo = round(min(o, c) * (1 - 0.004 - ((s + i) % 3) * 0.001), 4)
        out.append({"o": round(o, 4), "h": hi, "l": lo, "c": c})
        close = c
    # last close ≈ current price
    if out:
        out[-1]["c"] = round(base, 4)
        out[-1]["h"] = max(out[-1]["h"], out[-1]["c"], out[-1]["o"])
        out[-1]["l"] = min(out[-1]["l"], out[-1]["c"], out[-1]["o"])
    return out


def order_book(ticker: str) -> dict:
    inst = get_instrument(ticker)
    if not inst:
        return {"bids": [], "asks": []}
    p = float(inst["price"])
    s = _seed(ticker)
    bids = []
    asks = []
    for i in range(8):
        bids.append(
            {
                "price": round(p * (1 - 0.001 * (i + 1)), 4),
                "qty": 10 + ((s + i * 3) % 90),
            }
        )
        asks.append(
            {
                "price": round(p * (1 + 0.001 * (i + 1)), 4),
                "qty": 8 + ((s + i * 5) % 70),
            }
        )
    return {"bids": bids, "asks": asks}


def metrics(ticker: str) -> dict:
    s = _seed(ticker)
    return {
        "pe": round(8 + (s % 200) / 10, 1),
        "ps": round(1 + (s % 50) / 10, 1),
        "debt_equity": round((s % 80) / 100, 2),
        "dividend_yield": round((s % 60) / 10, 1),
        "consensus": ["Покупать", "Держать", "Продавать"][s % 3],
    }


COLLECTIONS = [
    {"id": "first", "title": "Первый шаг", "kind": "conservative"},
    {"id": "up", "title": "Взлёты дня", "kind": "stock"},
    {"id": "pop", "title": "Популярно", "kind": "all"},
]
