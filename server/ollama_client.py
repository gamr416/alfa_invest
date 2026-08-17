"""Ollama chat client — bonsai-27b, graceful fallback."""

from __future__ import annotations

import os
from typing import Any

import httpx

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL = os.getenv("OLLAMA_MODEL", "bonsai-27b:latest")

SYSTEM = """Ты — помощник Альфа-инвестиций для новичков 18–24.
Говори по-русски, просто, дружелюбно, как в мессенджере.
Отвечай развёрнуто: 2–4 коротких абзаца или 6–10 предложений. Можно список, если так яснее.
Не обещай доходность и не гарантируй прибыль.
Не советуй акции, крипту и маржу сверх уже выбранного продукта.
Если спрашивают «что купить» — направь к фонду денежного рынка или облигационному фонду как первому шагу.
Не добавляй юридические дисклеймеры в конец ответа.
Обращайся к клиенту по имени. Строго соблюдай род: женский — «ты готова», «поняла», «начала»; мужской — «ты готов», «понял», «начал». Не путай род ни в одном предложении.
"""


def _client_block(client: dict | None) -> str:
    if not client:
        return ""
    gender = client.get("gender") or ""
    if gender in ("female", "ж", "f"):
        rod = "женский. Обращайся в женском роде (готова, поняла, начала, молодчица)."
    elif gender in ("male", "м", "m"):
        rod = "мужской. Обращайся в мужском роде (готов, понял, начал, молодец)."
    else:
        rod = "не указан. Используй нейтральные формы без рода (ты, тебе)."
    name = client.get("name") or "клиент"
    age = client.get("age")
    age_s = f", {age} лет" if age is not None else ""
    return (
        f"\nКлиент: {name}{age_s}. Пол: {rod} "
        f"Имя в обращении: {name}."
    )


async def chat(
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    client: dict | None = None,
) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM + _client_block(client)}, *messages],
        "stream": False,
        "think": False,
        "options": {"temperature": temperature, "num_predict": 420},
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(2.0, read=240.0)) as http:
            r = await http.post(f"{OLLAMA_URL}/api/chat", json=payload)
            r.raise_for_status()
            data = r.json()
            msg = data.get("message") or {}
            text = (msg.get("content") or "").strip()
            if not text and msg.get("thinking"):
                parts = [p.strip() for p in str(msg["thinking"]).split("\n") if p.strip()]
                text = parts[-1] if parts else ""
            return {"ok": True, "reply": text, "model": MODEL}
    except Exception as e:
        name = (client or {}).get("name") or "друг"
        gender = (client or {}).get("gender")
        if gender in ("female", "ж", "f"):
            reply = (
                f"{name}, я сейчас без нейросети — сервер ассистента не отвечает. "
                "Можешь без меня: учёба в приложении и первый шаг в фонд денежного рынка LQDT от 100 ₽. "
                "Когда модель снова включится, я продолжу объяснять уже выбранный продукт."
            )
        else:
            reply = (
                f"{name}, я сейчас без нейросети — сервер ассистента не отвечает. "
                "Можешь без меня: учёба в приложении и первый шаг в фонд денежного рынка LQDT от 100 ₽. "
                "Когда модель снова включится, я продолжу объяснять уже выбранный продукт."
            )
        return {
            "ok": False,
            "reply": reply,
            "error": f"{type(e).__name__}: {e}",
            "model": MODEL,
            "fallback": True,
        }


async def health() -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            r.raise_for_status()
            names = [m.get("name", "") for m in r.json().get("models", [])]
            has = any(MODEL in n or n.startswith(MODEL.split(":")[0]) for n in names)
            return {"ok": True, "model": MODEL, "available": has, "models": names}
    except httpx.HTTPError as e:
        return {"ok": False, "model": MODEL, "available": False, "error": str(e)}
