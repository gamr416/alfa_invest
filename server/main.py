"""Alfa Invest MVP API — stubs + Ollama agent."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from academy_curriculum import payload as academy_payload
from ollama_client import chat as ollama_chat
from ollama_client import health as ollama_health
from stubs import alfa, market, portfolio

app = FastAPI(title="Alfa Invest MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class OrderIn(BaseModel):
    ticker: str
    side: str = Field(pattern="^(buy|sell)$")
    qty: float = Field(gt=0)
    order_type: str = "market"
    limit_price: float | None = None


class OnboardIn(BaseModel):
    goal: str | None = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatIn(BaseModel):
    messages: list[ChatMessage]
    context: str | None = None


@app.get("/api/health")
async def health():
    o = await ollama_health()
    return {"api": "ok", "ollama": o}


@app.get("/api/me")
def me():
    return alfa.get_me()


@app.get("/api/portfolio")
def get_portfolio():
    return portfolio.snapshot()


@app.get("/api/operations")
def get_operations():
    return {"items": portfolio.operations()}


@app.post("/api/onboard")
def onboard(body: OnboardIn):
    return portfolio.set_onboarded(body.goal)


@app.get("/api/instruments")
def instruments(
    q: str | None = None,
    kind: str | None = Query(None, description="all|stock|etf|conservative"),
):
    return {"items": market.list_instruments(q, kind), "collections": market.COLLECTIONS}


@app.get("/api/instruments/{ticker}")
def instrument(ticker: str):
    inst = market.get_instrument(ticker)
    if not inst:
        raise HTTPException(404, "not found")
    return {
        **inst,
        "sparkline": market.sparkline(ticker),
        "candles": market.candles(ticker),
        "book": market.order_book(ticker),
        "metrics": market.metrics(ticker),
    }


@app.post("/api/orders")
def orders(body: OrderIn):
    try:
        return portfolio.place_order(
            body.ticker, body.side, body.qty, body.order_type, body.limit_price
        )
    except ValueError as e:
        raise HTTPException(400, str(e)) from e


@app.post("/api/agent/chat")
async def agent_chat(body: ChatIn):
    msgs = [{"role": m.role, "content": m.content} for m in body.messages]
    if body.context:
        msgs = [
            {
                "role": "user",
                "content": f"[Контекст продукта]\n{body.context}",
            },
            *msgs,
        ]
    return await ollama_chat(msgs, client=alfa.get_me())


PULSE_STATIC = [
    {
        "id": "1",
        "author": "Альфа",
        "title": "Почему начинают с денежного рынка",
        "body": "Акции ты уже знаешь. Первый счёт удобнее на спокойном фонде: потренировать взнос, когда зарплата скачет.",
        "tag": "обучение",
    },
    {
        "id": "2",
        "author": "Рынок",
        "title": "БПИФ — это не «ещё одна акция»",
        "body": "Корзина в одной кнопке. Для практики первого взноса этого достаточно — не надо собирать портфель с нуля.",
        "tag": "новости",
    },
    {
        "id": "3",
        "author": "Сообщество",
        "title": "Первый взнос 100 ₽ — нормально",
        "body": "Маленькая сумма снимает страх. Главное — понять «зачем», а не гнаться за цифрой.",
        "tag": "пульс",
    },
    {
        "id": "4",
        "author": "Альфа",
        "title": "Диверсификация без умных слов",
        "body": "Не клади всё в одну акцию. Фонд уже держит корзину — для новичка этого достаточно.",
        "tag": "обучение",
    },
    {
        "id": "5",
        "author": "Рынок",
        "title": "Почему график скачет, а ты нет",
        "body": "День вниз не значит, что ты «всё потерял». Горизонт важнее вчерашней свечи.",
        "tag": "новости",
    },
    {
        "id": "6",
        "author": "Альфа",
        "title": "Комиссия агента — за объяснение",
        "body": "Модель не выбирает бумагу. Она говорит «почему так», после правил продукта.",
        "tag": "продукт",
    },
]


@app.get("/api/pulse")
def pulse():
    items = market.recent_news(5) + PULSE_STATIC
    return {"items": items}


@app.get("/api/academy")
def academy():
    return academy_payload()


_DIST = Path(__file__).resolve().parent.parent / "web" / "dist"


@app.get("/{full_path:path}")
def spa(full_path: str):
    if not _DIST.is_dir():
        raise HTTPException(404, "ui not built")
    if full_path:
        target = (_DIST / full_path).resolve()
        if _DIST in target.parents and target.is_file():
            return FileResponse(target)
    index = _DIST / "index.html"
    if not index.is_file():
        raise HTTPException(404, "ui not built")
    return FileResponse(index)
