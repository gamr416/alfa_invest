"""In-memory paper portfolio and orders."""

from __future__ import annotations

import time
import uuid
from typing import Any

from . import market

_state: dict[str, Any] = {
    "cash": 1_000_000_000.0,
    "positions": {},  # ticker -> {qty, avg}
    "orders": [],
    "ops": [],
    "onboarded": False,
    "goal": None,
}


def snapshot() -> dict:
    positions = []
    total = float(_state["cash"])
    for ticker, pos in _state["positions"].items():
        inst = market.get_instrument(ticker)
        if not inst:
            continue
        price = float(inst["price"])
        value = price * pos["qty"]
        total += value
        pnl = (price - pos["avg"]) * pos["qty"]
        positions.append(
            {
                "ticker": ticker,
                "name": inst["name"],
                "type": inst["type"],
                "qty": pos["qty"],
                "avg": pos["avg"],
                "price": price,
                "value": round(value, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": round((price / pos["avg"] - 1) * 100, 2) if pos["avg"] else 0,
                "sparkline": market.sparkline(ticker, 16),
            }
        )
    day_pnl = sum(p["pnl"] for p in positions)
    return {
        "cash": round(_state["cash"], 2),
        "total": round(total, 2),
        "day_pnl": round(day_pnl, 2),
        "day_pnl_pct": round(day_pnl / total * 100, 2) if total else 0,
        "positions": positions,
        "onboarded": _state["onboarded"],
        "goal": _state["goal"],
    }


def operations() -> list[dict]:
    return list(reversed(_state["ops"]))


def set_onboarded(goal: str | None = None) -> dict:
    _state["onboarded"] = True
    if goal:
        _state["goal"] = goal
    return snapshot()


def place_order(
    ticker: str,
    side: str,
    qty: float,
    order_type: str = "market",
    limit_price: float | None = None,
) -> dict:
    inst = market.get_instrument(ticker)
    if not inst:
        raise ValueError("Инструмент не найден")
    if qty <= 0:
        raise ValueError("Количество должно быть больше 0")
    price = float(limit_price) if order_type == "limit" and limit_price else float(inst["price"])
    cost = price * qty
    commission = round(max(cost * 0.0005, 1.0), 2)

    if side == "buy":
        if cost + commission > _state["cash"]:
            raise ValueError("Недостаточно средств")
        _state["cash"] -= cost + commission
        pos = _state["positions"].get(ticker, {"qty": 0.0, "avg": 0.0})
        new_qty = pos["qty"] + qty
        pos["avg"] = ((pos["avg"] * pos["qty"]) + cost) / new_qty if new_qty else price
        pos["qty"] = new_qty
        _state["positions"][ticker] = pos
    elif side == "sell":
        pos = _state["positions"].get(ticker)
        if not pos or pos["qty"] < qty:
            raise ValueError("Недостаточно бумаг")
        _state["cash"] += cost - commission
        pos["qty"] -= qty
        if pos["qty"] <= 1e-9:
            del _state["positions"][ticker]
        else:
            _state["positions"][ticker] = pos
    else:
        raise ValueError("side: buy|sell")

    order = {
        "id": str(uuid.uuid4())[:8],
        "ticker": ticker.upper(),
        "side": side,
        "qty": qty,
        "price": price,
        "commission": commission,
        "type": order_type,
        "status": "filled",
        "ts": int(time.time()),
    }
    _state["orders"].append(order)
    _state["ops"].append(
        {
            "id": order["id"],
            "kind": "trade",
            "title": f"{'Покупка' if side == 'buy' else 'Продажа'} {ticker.upper()}",
            "amount": -cost - commission if side == "buy" else cost - commission,
            "ts": order["ts"],
        }
    )
    _state["ops"].append(
        {
            "id": order["id"] + "c",
            "kind": "commission",
            "title": "Комиссия брокера",
            "amount": -commission,
            "ts": order["ts"],
        }
    )
    return {"order": order, "portfolio": snapshot()}


def conservative_practice() -> dict[str, bool]:
    """First and repeat paper buys into conservative instruments (not PnL)."""
    buys = 0
    for order in _state["orders"]:
        if order.get("side") != "buy":
            continue
        inst = market.get_instrument(order["ticker"])
        if inst and inst.get("conservative"):
            buys += 1
    return {"first": buys >= 1, "repeat": buys >= 2}
