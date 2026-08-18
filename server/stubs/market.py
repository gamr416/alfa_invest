"""Stub: market instruments, quotes, order book, sparklines."""

from __future__ import annotations

import hashlib
import time
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

NEWS: list[dict[str, Any]] = [
    {
        "id": "n1",
        "direction": "up",
        "tickers": ["SBER"],
        "title": "Демо: отчёт лучше ожиданий — банки в плюсе",
        "body": "Учебный заголовок, не факт. В демо цена Сбера сегодня выше открытия. Отчёт не обязан быть причиной — так рынок иногда совпадает с новостью.",
    },
    {
        "id": "n2",
        "direction": "down",
        "tickers": ["GAZP"],
        "title": "Демо: спот слабее — экспортёры под давлением",
        "body": "Учебный сценарий. Газпром в минусе за день. Не торговый сигнал и не новость агентства.",
    },
    {
        "id": "n3",
        "direction": "up",
        "tickers": ["YDEX"],
        "title": "Демо: рекламный сезон — IT тянут индекс",
        "body": "Яндекс в плюсе в этой минутной модели. Для первого взноса это не повод гнаться за бумагой.",
    },
    {
        "id": "n4",
        "direction": "down",
        "tickers": ["VTBR"],
        "title": "Демо: слух про размытие — бумага дешевеет",
        "body": "ВТБ ниже открытия дня. Слух выдуман для демо. Низкая цена за штуку не значит «дёшево».",
    },
    {
        "id": "n5",
        "direction": "up",
        "tickers": ["SBGB", "FXRU"],
        "title": "Демо: ставка без сюрприза — облигации чуть выше",
        "body": "ОФЗ и корп. фонды чуть в плюсе. Движение крошечное — так и задумано для спокойных фондов.",
    },
    {
        "id": "n6",
        "direction": "down",
        "tickers": ["YDEX", "TMOS"],
        "title": "Демо: фиксация в росте — технологии отдают",
        "body": "IT и широкий рынок ниже открытия. День вниз не равен «всё потерял».",
    },
    {
        "id": "n7",
        "direction": "up",
        "tickers": ["TMOS", "SBER"],
        "title": "Демо: оборот на Мосбирже выше среднего",
        "body": "Индекс и Сбер в плюсе в стабе. Оборот выдуман. Не сигнал к покупке.",
    },
    {
        "id": "n8",
        "direction": "up",
        "tickers": ["LQDT"],
        "title": "Демо: overnight чуть выше — денежный рынок копейки",
        "body": "LQDT почти не скачет. Если цифра шевелится — это копейки, не «взлёт дня».",
    },
]


def _seed(ticker: str) -> int:
    return int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)


def _base(ticker: str) -> dict | None:
    for i in INSTRUMENTS:
        if i["ticker"].upper() == ticker.upper():
            return i
    return None


def _vol(inst: dict) -> float:
    if inst.get("conservative"):
        return 0.0003
    if inst["ticker"] == "TMOS":
        return 0.0015
    return 0.004


def _u01(key: str) -> float:
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


def _minute_return(inst: dict, minute: int) -> float:
    u = _u01(f"{inst['ticker']}:{minute}")
    return (u * 2 - 1) * _vol(inst)


def _round_price(p: float) -> float:
    if p < 1:
        return round(p, 6)
    if p < 20:
        return round(p, 4)
    return round(p, 2)


def _day_start_minute(minute: int) -> int:
    return (minute * 60 // 86400) * 1440


def _price_at(inst: dict, minute: int) -> float:
    p = float(inst["price"])
    for m in range(_day_start_minute(minute), minute + 1):
        p *= 1 + _minute_return(inst, m)
    return p


def quote(ticker: str, ts: float | None = None) -> dict | None:
    inst = _base(ticker)
    if not inst:
        return None
    minute = int(ts if ts is not None else time.time()) // 60
    live = _price_at(inst, minute)
    open_p = float(inst["price"])
    change_pct = round((live / open_p - 1) * 100, 2) if open_p else 0.0
    out = dict(inst)
    out["price"] = _round_price(live)
    out["change_pct"] = change_pct
    return out


def list_instruments(q: str | None = None, kind: str | None = None) -> list[dict]:
    items = [quote(i["ticker"]) for i in INSTRUMENTS]
    items = [i for i in items if i]
    if kind == "conservative":
        items = [i for i in items if i["conservative"]]
    elif kind and kind != "all":
        items = [i for i in items if i["type"] == kind]
    if q:
        ql = q.lower()
        items = [i for i in items if ql in i["ticker"].lower() or ql in i["name"].lower()]
    return items


def get_instrument(ticker: str) -> dict | None:
    return quote(ticker)


def sparkline(ticker: str, points: int = 24) -> list[float]:
    return [c["c"] for c in candles(ticker, points)]


def candles(ticker: str, n: int = 24) -> list[dict]:
    inst = _base(ticker)
    if not inst:
        return []
    minute = int(time.time()) // 60
    out: list[dict] = []
    for i in range(n):
        m = minute - (n - 1) + i
        o = _round_price(_price_at(inst, m - 1))
        c = _round_price(_price_at(inst, m))
        hi = _round_price(max(o, c) * (1 + 0.0008))
        lo = _round_price(min(o, c) * (1 - 0.0008))
        out.append({"o": o, "h": hi, "l": lo, "c": c})
    return out


def order_book(ticker: str) -> dict:
    inst = quote(ticker)
    if not inst:
        return {"bids": [], "asks": []}
    p = float(inst["price"])
    s = _seed(ticker)
    bids = []
    asks = []
    for i in range(8):
        bids.append(
            {
                "price": _round_price(p * (1 - 0.001 * (i + 1))),
                "qty": 10 + ((s + i * 3) % 90),
            }
        )
        asks.append(
            {
                "price": _round_price(p * (1 + 0.001 * (i + 1))),
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


def live_news(ts: float | None = None) -> dict | None:
    minute = int(ts if ts is not None else time.time()) // 60
    h = int(hashlib.md5(f"news:{minute}".encode()).hexdigest()[:8], 16)
    if h % 3 != 0:
        return None
    candidates: list[dict] = []
    for n in NEWS:
        lead = n["tickers"][0]
        q = quote(lead, ts=float(minute * 60))
        if not q:
            continue
        up = q["change_pct"] >= 0
        if n["direction"] == "up" and up:
            candidates.append(n)
        elif n["direction"] == "down" and not up:
            candidates.append(n)
    if not candidates:
        return None
    n = candidates[h % len(candidates)]
    return {
        "id": f"{n['id']}-{minute}",
        "author": "Рынок",
        "title": n["title"],
        "body": n["body"],
        "tag": "рынок",
        "tickers": n["tickers"],
    }


def recent_news(limit: int = 5, ts: float | None = None) -> list[dict]:
    minute = int(ts if ts is not None else time.time()) // 60
    out: list[dict] = []
    m = minute
    while len(out) < limit and m > minute - 180:
        item = live_news(float(m * 60))
        if item:
            out.append(item)
        m -= 1
    return out


COLLECTIONS = [
    {"id": "first", "title": "Первый шаг", "kind": "conservative"},
    {"id": "up", "title": "Взлёты дня", "kind": "stock"},
]
