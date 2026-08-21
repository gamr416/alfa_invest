#!/usr/bin/env python3
"""PDF-слайды Альфа-будущее — мало текста, инфографика, альбом A4."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "slides" / "alfa-budushchee-slides-market-6-7.pdf"

FONT = "Liberation"
FONT_B = "LiberationBold"
pdfmetrics.registerFont(TTFont(FONT, "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont(FONT_B, "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"))

RED = HexColor("#EF3124")
INK = HexColor("#111111")
MUTED = HexColor("#666666")
LINE = HexColor("#E8E8E8")
BG = HexColor("#F6F6F6")
SOFT = HexColor("#FFF5F4")
GREEN = HexColor("#1A9E4A")

PAGE = landscape(A4)
W, H = PAGE


def header(c: canvas.Canvas, title: str, page: int, total: int) -> float:
    bar_h = 40
    c.setFillColor(RED)
    c.rect(0, H - bar_h, W, bar_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(FONT_B, 10)
    c.drawString(28, H - 24, "АЛЬФА · БУДУЩЕЕ")
    c.setFont(FONT, 8)
    c.drawRightString(W - 28, H - 24, f"{page}/{total}")
    c.setFillColor(INK)
    c.setFont(FONT_B, 24)
    c.drawString(28, H - bar_h - 32, title)
    return H - bar_h - 48


def footer(c: canvas.Canvas) -> None:
    c.setFillColor(MUTED)
    c.setFont(FONT, 7)
    c.drawString(28, 12, "Фича банка · не стартап · авг 2026")


def pill(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill: Color) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)


def arrow_right(c: canvas.Canvas, x: float, y: float, color: Color = RED) -> None:
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(x, y, x + 18, y)
    path = c.beginPath()
    path.moveTo(x + 18, y)
    path.lineTo(x + 12, y + 5)
    path.lineTo(x + 12, y - 5)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def stars_bar(c: canvas.Canvas, x: float, y: float, n: int, max_n: int = 5, w: float = 70) -> None:
    """Горизонтальный бар силы 0–5."""
    c.setFillColor(BG)
    c.roundRect(x, y, w, 8, 2, fill=1, stroke=0)
    fill_w = w * (n / max_n)
    c.setFillColor(RED)
    c.roundRect(x, y, fill_w, 8, 2, fill=1, stroke=0)


# ─── 1. Рынок (1 слайд) ──────────────────────────────────────────────────────


def slide_market(c: canvas.Canvas, page: int, total: int) -> None:
    y = header(c, "Рынок · 2026", page, total)

    # 4 trend icons as big tiles
    trends = [
        ("01", "Дешевле", "ETF > активные фонды"),
        ("02", "Шире доступ", "Private → retail"),
        ("03", "AI", "Персонализация"),
        ("04", "CX", "Дистрибуция > продукт"),
    ]
    tw = (W - 56 - 30) / 4
    th = 130
    for i, (num, title, sub) in enumerate(trends):
        x = 28 + i * (tw + 10)
        pill(c, x, y - th, tw, th, white)
        c.setFillColor(RED)
        c.setFont(FONT_B, 28)
        c.drawString(x + 16, y - 40, num)
        c.setFillColor(INK)
        c.setFont(FONT_B, 16)
        c.drawString(x + 16, y - 72, title)
        c.setFillColor(MUTED)
        c.setFont(FONT, 10)
        c.drawString(x + 16, y - 96, sub)

    # Big numbers row
    ny = y - th - 28
    stats = [
        ("$943B", "model portfolios"),
        ("$308B", "BlackRock · ~⅓"),
        ("→ CX+AI", "где конкурировать"),
    ]
    sw = (W - 56 - 20) / 3
    for i, (v, l) in enumerate(stats):
        x = 28 + i * (sw + 10)
        fill = SOFT if i == 2 else BG
        pill(c, x, ny - 90, sw, 90, fill)
        c.setFillColor(RED if i == 2 else INK)
        c.setFont(FONT_B, 28)
        c.drawCentredString(x + sw / 2, ny - 42, v)
        c.setFillColor(MUTED)
        c.setFont(FONT, 10)
        c.drawCentredString(x + sw / 2, ny - 68, l)

    # One-line takeaway
    c.setFillColor(INK)
    c.setFont(FONT_B, 13)
    c.drawCentredString(W / 2, 48, "Выигрывает не продукт, а путь клиента + объяснение")
    footer(c)
    c.showPage()


# ─── 2. Конкуренты ───────────────────────────────────────────────────────────


def slide_competitors(c: canvas.Canvas, page: int, total: int) -> None:
    y = header(c, "Конкуренты → наша ниша", page, total)

    # Left: radar-like bars vs competitors
    left_w = 340
    pill(c, 28, y - 280, left_w, 280, white)
    c.setFillColor(INK)
    c.setFont(FONT_B, 12)
    c.drawString(44, y - 28, "Где сильные брокеры")

    axes = [
        ("Каталог / терминал", 5),
        ("Обучение рынку", 4),
        ("Робот-портфель", 4),
        ("Первый шаг 18–26", 2),
        ("Банк → взнос", 2),
        ("ИИ объясняет выбор", 1),
    ]
    ay = y - 58
    for label, n in axes:
        c.setFillColor(MUTED)
        c.setFont(FONT, 9)
        c.drawString(44, ay, label)
        stars_bar(c, 200, ay - 1, n, w=140)
        ay -= 34

    # Right: our niche funnel visual
    rx = 28 + left_w + 16
    rw = W - rx - 28
    pill(c, rx, y - 280, rw, 280, SOFT)

    c.setFillColor(RED)
    c.setFont(FONT_B, 12)
    c.drawString(rx + 18, y - 28, "Белое пятно")

    steps = [
        "кэшбэк / остаток",
        "цель + квиз",
        "LQDT + «почему»",
        "взнос от 100 ₽",
    ]
    sy = y - 70
    for i, s in enumerate(steps):
        pill(c, rx + 40, sy - 36, rw - 80, 36, white)
        c.setFillColor(RED)
        c.setFont(FONT_B, 14)
        c.drawCentredString(rx + rw / 2, sy - 22, f"{i + 1}.  {s}")
        if i < len(steps) - 1:
            c.setFillColor(RED)
            c.setFont(FONT_B, 14)
            c.drawCentredString(rx + rw / 2, sy - 48, "↓")
        sy -= 52

    c.setFillColor(INK)
    c.setFont(FONT_B, 11)
    c.drawCentredString(W / 2, 48, "Они продают доступ к рынку · мы — безопасный первый шаг")
    footer(c)
    c.showPage()


# ─── 6. Персонализация ───────────────────────────────────────────────────────


def slide_personalization(c: canvas.Canvas, page: int, total: int) -> None:
    y = header(c, "6 · Персонализация", page, total)

    boxes = [
        ("ДАННЫЕ", "остаток\nкэшбэк\nцель", BG),
        ("ПРАВИЛА", "18+\nwhitelist\nconservative", SOFT),
        ("LLM", "только\n«почему»\n+ fallback", BG),
    ]
    bw = 160
    bh = 160
    gap = 36
    total_w = 3 * bw + 2 * gap
    x0 = (W - total_w) / 2
    by = y - 40

    for i, (title, body, fill) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        pill(c, x, by - bh, bw, bh, fill)
        c.setFillColor(RED)
        c.setFont(FONT_B, 12)
        c.drawCentredString(x + bw / 2, by - 28, title)
        c.setFillColor(INK)
        c.setFont(FONT_B, 14)
        lines = body.split("\n")
        ly = by - 60
        for line in lines:
            c.drawCentredString(x + bw / 2, ly, line)
            ly -= 22
        if i < 2:
            arrow_right(c, x + bw + 6, by - bh / 2)

    # Result chip
    cy = by - bh - 50
    pill(c, W / 2 - 220, cy - 50, 440, 50, INK)
    c.setFillColor(white)
    c.setFont(FONT_B, 14)
    c.drawCentredString(W / 2, cy - 30, "→  Product Card: LQDT + 2 альтернативы")

    # Ban row
    bans = ["не выбирает тикер", "не обещает %", "не ставит ордер"]
    bx = (W - 3 * 180 - 20) / 2
    for i, b in enumerate(bans):
        x = bx + i * 190
        pill(c, x, 55, 180, 36, white)
        c.setFillColor(RED)
        c.setFont(FONT_B, 10)
        c.drawCentredString(x + 90, 68, f"✕  {b}")

    footer(c)
    c.showPage()


# ─── 7. Финмодель ────────────────────────────────────────────────────────────


def slide_finance(c: canvas.Canvas, page: int, total: int) -> None:
    y = header(c, "7 · Финмодель фичи", page, total)

    # Hero one-liner
    c.setFillColor(RED)
    c.setFont(FONT_B, 14)
    c.drawCentredString(W / 2, y - 8, "700 ₽ чек ≠ бизнес   ·   кейс = 3 слоя")

    layers = [
        ("ЛИФТ", "11,1%", "+10% счетов"),
        ("MIX УК", "30%", "AKMM после LQDT"),
        ("PRIMARY", "94 млн ₽", "удержание 3г"),
    ]
    lw = (W - 56 - 24) / 3
    lh = 140
    ly = y - 40
    for i, (t, v, s) in enumerate(layers):
        x = 28 + i * (lw + 12)
        pill(c, x, ly - lh, lw, lh, SOFT if i == 0 else white)
        c.setFillColor(MUTED)
        c.setFont(FONT_B, 10)
        c.drawCentredString(x + lw / 2, ly - 28, t)
        c.setFillColor(RED)
        c.setFont(FONT_B, 32)
        c.drawCentredString(x + lw / 2, ly - 72, v)
        c.setFillColor(INK)
        c.setFont(FONT, 11)
        c.drawCentredString(x + lw / 2, ly - 100, s)

    # Product flow + KPIs
    fy = ly - lh - 30
    # flow
    flow = [("цель",), ("квиз",), ("LQDT",), ("AKMM",)]
    fw = 110
    fx0 = 28
    for i, (label,) in enumerate(flow):
        x = fx0 + i * (fw + 28)
        pill(c, x, fy - 48, fw, 48, RED if label in ("LQDT", "AKMM") else BG)
        c.setFillColor(white if label in ("LQDT", "AKMM") else INK)
        c.setFont(FONT_B, 13)
        c.drawCentredString(x + fw / 2, fy - 28, label)
        if i < len(flow) - 1:
            arrow_right(c, x + fw + 4, fy - 24)

    # KPI chips
    kpis = [("3,36 млн", "working"), ("18,7k", "взносы Y1"), ("781 млн ₽", "AUM Y3")]
    kx = 28 + 4 * (fw + 28) - 20
    # Actually place KPIs on the right if space, else below
    # Better: row under flow
    ky = fy - 48 - 28
    kw = (W - 56 - 20) / 3
    for i, (v, l) in enumerate(kpis):
        x = 28 + i * (kw + 10)
        pill(c, x, ky - 55, kw, 55, BG)
        c.setFillColor(INK)
        c.setFont(FONT_B, 16)
        c.drawCentredString(x + kw / 2, ky - 22, v)
        c.setFillColor(MUTED)
        c.setFont(FONT, 9)
        c.drawCentredString(x + kw / 2, ky - 40, l)

    footer(c)
    c.showPage()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
    c.setTitle("Альфа-будущее — слайды")
    slides = [slide_market, slide_competitors, slide_personalization, slide_finance]
    total = len(slides)
    for i, fn in enumerate(slides, 1):
        fn(c, i, total)
    c.save()
    print(f"OK → {OUT}")


if __name__ == "__main__":
    main()
