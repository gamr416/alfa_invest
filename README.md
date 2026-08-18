# Альфа-инвестиции MVP

Mobile-first веб-оболочка инвестиций для кейса «Альфа-будущее». ЦА **18–26**.

**Полная документация:** [docs/mvp.md](docs/mvp.md)  
Кейс: [docs/project.md](docs/project.md) · архитектура: [architecture/README.md](architecture/README.md)

## Запуск

```bash
# API
cd alfa_invest && source .venv/bin/activate
cd server && uvicorn main:app --host 127.0.0.1 --port 8000

# UI
cd alfa_invest/web && npm run dev
```

http://127.0.0.1:5173 — Vite проксирует `/api` на :8000.

Ollama: модель `bonsai-8b:latest` (локальный GGUF), `ollama serve`.

```bash
ollama create bonsai-8b -f Modelfile
```

Fallback без модели:

```bash
OLLAMA_URL=http://127.0.0.1:1 uvicorn main:app --host 127.0.0.1 --port 8000
```

## Стек

Vite + React + TS · FastAPI · paper-портфель в памяти · стабы Alfa и рынка.
