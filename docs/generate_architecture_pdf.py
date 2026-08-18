#!/usr/bin/env python3
"""Сборка подробного PDF по архитектуре и стратегиям кейса Альфа-будущее."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "alfa-budushchee-arhitektura-i-strategii.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

RED = HexColor("#EF3124")
INK = HexColor("#111111")
MUTED = HexColor("#555555")
LINE = HexColor("#DDDDDD")
BG = HexColor("#F7F7F7")


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            "CoverTitle",
            fontName="DejaVuBold",
            fontSize=26,
            leading=32,
            textColor=white,
            alignment=TA_LEFT,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "CoverSub",
            fontName="DejaVu",
            fontSize=12,
            leading=16,
            textColor=white,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            "H1",
            fontName="DejaVuBold",
            fontSize=16,
            leading=22,
            textColor=RED,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "H2",
            fontName="DejaVuBold",
            fontSize=13,
            leading=18,
            textColor=INK,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "H3",
            fontName="DejaVuBold",
            fontSize=11,
            leading=15,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            "Body",
            fontName="DejaVu",
            fontSize=9.5,
            leading=13.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "BulletBody",
            fontName="DejaVu",
            fontSize=9.5,
            leading=13.5,
            textColor=INK,
            leftIndent=4,
        )
    )
    s.add(
        ParagraphStyle(
            "Caption",
            fontName="DejaVu",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "Cell",
            fontName="DejaVu",
            fontSize=8,
            leading=11,
            textColor=INK,
        )
    )
    s.add(
        ParagraphStyle(
            "CellHead",
            fontName="DejaVuBold",
            fontSize=8,
            leading=11,
            textColor=white,
        )
    )
    s.add(
        ParagraphStyle(
            "Footer",
            fontName="DejaVu",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    s.add(
        ParagraphStyle(
            "Mono",
            fontName="DejaVu",
            fontSize=8,
            leading=11.5,
            textColor=INK,
            backColor=BG,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return s


S = styles()


def p(text, style="Body"):
    return Paragraph(text.replace("\n", "<br/>"), S[style])


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, S["BulletBody"]), leftIndent=12, bulletColor=RED) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=14,
        bulletFontName="DejaVu",
        bulletFontSize=9,
        spaceAfter=8,
    )


def tbl(rows, col_widths=None):
    data = []
    for i, row in enumerate(rows):
        st = "CellHead" if i == 0 else "Cell"
        data.append([Paragraph(str(c), S[st]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RED),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG]),
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(RED)
    canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(18 * mm, A4[1] - 5.5 * mm, "Альфа-будущее  ·  архитектура и стратегии")
    canvas.setFillColor(HexColor("#F0F0F0"))
    canvas.rect(0, 0, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(18 * mm, 5 * mm, "Не юрконсультация. Демо / кейс. 18 августа 2026")
    canvas.drawRightString(A4[0] - 18 * mm, 5 * mm, str(doc.page))
    canvas.restoreState()


def cover_page(canvas, doc):
    if doc.page != 1:
        header_footer(canvas, doc)
        return
    canvas.saveState()
    canvas.setFillColor(RED)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("DejaVu", 11)
    canvas.drawString(22 * mm, A4[1] - 40 * mm, "Кейс «Альфа-будущее»")
    canvas.setFont("DejaVuBold", 28)
    y = A4[1] - 58 * mm
    for line in ["Архитектура решения", "и продуктовые стратегии"]:
        canvas.drawString(22 * mm, y, line)
        y -= 12 * mm
    canvas.setFont("DejaVu", 11)
    canvas.drawString(22 * mm, 55 * mm, "Mobile-first веб · paper-брокер · правила выше ИИ")
    canvas.drawString(22 * mm, 45 * mm, "ЦА 18–26 · первый осознанный взнос от 100 ₽ · LQDT")
    canvas.drawString(22 * mm, 32 * mm, "Сводка по репозиторию alfa_invest · август 2026")
    canvas.restoreState()


def build():
    story = []
    story.append(Spacer(1, 220 * mm))
    story.append(PageBreak())

    story.append(p("1. Зачем этот документ", "H1"))
    story.append(
        p(
            "Документ собирает в одном месте продуктовую стратегию, архитектурные решения, "
            "гипотезы персонализации, правовой контур и то, как это реализовано в демо. "
            "Источник правды по архитектуре — папка architecture/ (точка входа architecture/README.md). "
            "Кейс описан в docs/project.md, фиксация MVP — docs/mvp.md, глоссарий — CONTEXT.md, "
            "когорта — ADR-0002. Это не прод Альфа-Банка, а кликабельная оболочка «как банковское приложение»."
        )
    )
    story.append(
        p(
            "Северная звезда кейса: доля клиентов 18–26 с первым осознанным взносом за 90 дней после показа фичи. "
            "Бизнес-цель формулировки кейса: +10% конверсии открытия инвестиционного счёта за год."
        )
    )

    story.append(p("2. Проблема и позиционирование", "H1"))
    story.append(p("2.1. Рыночный контекст", "H2"))
    story.append(
        p(
            "За десять лет розничные инвестиции стали массовыми. Экономически активная молодёжь знает акции, "
            "облигации, вклад, инфляцию и риск потери денег. Барьер не в азбуке рынка, а в первом взносе: "
            "нет практики, доход нестабильный, страх «ошибиться раз и навсегда». Типичный путь конкурентов: "
            "баннер «инвестиции» → открытие счёта → витрина бумаг → опционально обучение. Слабое место — "
            "персонализация и объяснение риска до покупки. Белое пятно: первый шаг из повседневного сценария "
            "банка (кэшбэк, остаток, копилка) плюс «почему именно это» без обещания доходности."
        )
    )
    story.append(p("2.2. Боли, барьеры, мотивации", "H2"))
    story.append(
        tbl(
            [
                ["Боли", "Барьеры", "Мотивации"],
                [
                    "Знаю про акции — не знаю, с чего начать",
                    "Страх потери при первом взносе",
                    "Защита от инфляции мелкой суммой",
                ],
                [
                    "Доход скачет, «это не для меня»",
                    "Нет практики, только теория",
                    "Привычный мобильный банк",
                ],
                [
                    "Боюсь ошибиться навсегда",
                    "Витрина акций вместо первого шага",
                    "Понятный «зачем» без обещания заработка",
                ],
            ],
            [60 * mm, 60 * mm, 55 * mm],
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        p(
            "<b>Целевой первый шаг (First Conscious Contribution):</b> осознанный взнос от 100 ₽ "
            "в консервативный инструмент (фонд денежного рынка или облигационный БПИФ) после короткого "
            "обучения и объяснения выбора. Это снимает страх «я не умею», а не учит азбуке рынка."
        )
    )

    story.append(p("3. Когорта и возрастной контур", "H1"))
    story.append(
        p(
            "<b>ADR-0002 (accepted, 18 августа 2026, заменяет ADR-0001 18–24).</b> Working Cohort — "
            "экономически активная молодёжь РФ 18–26: студенты, выпускники, начинающие специалисты. "
            "Нет инвестсчёта или счёт пустой. Профиль: переход к самостоятельности, нестабильный доход, "
            "живут в мобильном банке, знания есть, практики нет. 14–17 — Minor Contour, не GTM и не вход MVP "
            "(нет родительского контура). 27+ могут пользоваться фичей, но не входят в северную звезду кейса. "
            "Age Gate: отказ младше 18 (в коде экран «Пока нельзя»)."
        )
    )
    story.append(
        p(
            "Срезы 18–21 (учёба, стипендия/подработка, страх маленькой суммы) и 22–26 (выпуск/джун, кэшбэк "
            "и копилка, цель подушка / не съела инфляция / поездка) — это copy, не отдельные модули и не "
            "разные бэкенды."
        )
    )
    story.append(
        p(
            "Демо-клиент: Аня, 21 год, female, cohort 18–26, остаток 12 450 ₽, кэшбэк 780 ₽, копилка 3 200 ₽, "
            "зарплатный признак есть, инвестсчёта нет. Логина нет — GET /api/me всегда отдаёт этот профиль "
            "(возраст можно подменить DEMO_AGE)."
        )
    )

    story.append(p("4. Продуктовые стратегии и гипотезы", "H1"))
    story.append(
        p(
            "Три гипотезы GenAI из кейса. Приоритет MVP: гипотеза 2 плюс кусок гипотезы 1. "
            "Проверка задумана как кликабельный прототип + диалог с ИИ + опрос 15–20 человек когорты. "
            "Сигналы: клик по точке входа, доходимость обучения, открытие счёта, первый взнос."
        )
    )
    story.append(p("Стратегия A. Первый шаг на сдачу (гипотеза 1)", "H2"))
    story.append(
        p(
            "Проблема: «мало денег». Ассистент предлагает сумму из кэшбэка или свободного остатка в фонд "
            "денежного рынка и объясняет, почему сумма безопасна для бюджета. Эффект: первый взнос. "
            "Сложность: средняя. В MVP это баннер/виджет («свободные 700 ₽ после кэшбэка»), старт с LQDT "
            "от 100 ₽, Bank Context (остаток, копилка, кэшбэк) без сырой ленты трат. Should, не must."
        )
    )
    story.append(p("Стратегия B. Почему именно это (гипотеза 2, ядро MVP)", "H2"))
    story.append(
        p(
            "Проблема: не понимают выбор и риск. Цель (подушка / гаджет / поездка) → три учебных вопроса "
            "риска (горизонт, приоритет, сумма) → один инструмент и две альтернативы простым языком. "
            "Эффект: осознанность и меньше отказов. Сложность: средне-высокая. Карточка продукта: LQDT "
            "плюс альтернативы SBGB и FXRU. Текст «почему» пишет Ollama по уже выбранному продукту, "
            "модель не назначает бумагу."
        )
    )
    story.append(p("Стратегия C. Тренер привычки на 4 недели (гипотеза 3)", "H2"))
    story.append(
        p(
            "Проблема: нет привычки. Микроуроки и напоминание регулярного взноса без давления на риск. "
            "Эффект: повторный взнос. Сложность: ниже средней. В демо: академия, калькулятор сложного "
            "процента как учебная модель (явно «не прогноз»), пульс, paper-повторы сделок. Полноценный "
            "4-недельный тренер и push в репо не доведены."
        )
    )
    story.append(p("Стратегия D. Гибрид персонализации, не чёрный ящик", "H2"))
    story.append(
        bullets(
            [
                "<b>Eligibility Rules</b> выбирают допустимый продукт: возраст, риск, горизонт, квалификация, запреты ЦБ. Правила выше модели.",
                "<b>Bank Context</b> влияет на сумму и формулировку цели: остаток, копилка, кэшбэк, признак регулярного дохода.",
                "<b>Explanation Copy</b>: генеративный ИИ пишет только «почему выбрано это, а не альтернативы» по уже отобранному продукту.",
                "ИИ не назначает рисковый актив и не обещает доходность. Перед показом — фильтр формулировок (system prompt + продуктовый контекст отдельным сообщением).",
            ]
        )
    )
    story.append(p("Стратегия E. Консервативный первый шаг, полный брокер как учебный контур", "H2"))
    story.append(
        p(
            "Первый заход — LQDT (фонд денежного рынка). Акции в каталоге есть, но с бейджем риска, "
            "не как первый шаг. Это сознательный компромисс с «гриля»: каталог как полный брокер-демо "
            "на стабах, чтобы после взноса человек мог пощупать бумагу, стакан и свечи без реальных денег. "
            "Won’t: маржа, крипта, обещание доходности, выбор актива промптом, отдельное приложение-стартап."
        )
    )
    story.append(p("Стратегия F. ИИ только объясняет и чатит", "H2"))
    story.append(
        p(
            "Продуктовое правило зафиксировано в architecture/README.md: выбор продукта — правила + UI, "
            "не модель. Агент обязателен как помощник, но ордер модель не ждёт. Нет Ollama — честный "
            "офлайн-текст, UI агента не прячем. История чата на бэке не хранится: фронт шлёт messages "
            "в POST /api/agent/chat. think: false / пустой блок think в Modelfile — иначе модель уходит "
            "в цепочку рассуждений и пустой content."
        )
    )
    story.append(p("Стратегия G. Спокойный тон вместо давления", "H2"))
    story.append(
        p(
            "Нет «успей купить». Обучение до сделки. Учебный риск-квиз не имитирует тест Банка России. "
            "Геймификация без лутбоксов и денежных розыгрышей (риск 244-ФЗ). Награды детерминированные "
            "(прогресс уроков). Empty state — плачущий маскот, не FOMO."
        )
    )
    story.append(p("Стратегия H. Данные и локализация", "H2"))
    story.append(
        p(
            "Персональные данные граждан РФ не собирать и не хранить на зарубежном аналитическом/облачном "
            "SaaS (152-ФЗ ст. 18). Ollama и стабы — локально. В MVP нет сырой ленты трат, только агрегаты "
            "Bank Context. Фича встраивается в контур банка, не живёт отдельным стартапом."
        )
    )
    story.append(p("Стратегия I. Конкурентное отличие", "H2"))
    story.append(
        p(
            "На рынке: БКС (сканер, покупка с карт), Альфа-прод (PRO API, Альфа-индекс, робот-советник), "
            "ВТБ (заявки до отмены, IPO), Финам (теханализ), Сбер (простота ПИФов). Наше отличие не в "
            "терминале и не в роботе, который сам балансирует портфель, а в первом шаге из банка: "
            "маленькая сумма, объяснимый консервативный продукт, учебный paper после взноса. "
            "Не копируем 150–200 экранов Т-Инвестиций: 6 хабов + дочерние."
        )
    )

    story.append(p("5. Ограничения, MoSCoW и этика", "H1"))
    story.append(
        tbl(
            [
                ["Класс", "Содержание"],
                ["Must", "Возраст 18+, дисклеймеры на уровне продукта (не в каждом пузыре чата), без обещания доходности, объяснимость, правила выше ИИ"],
                ["Should", "Сумма из остатка/кэшбэка, живой Ollama"],
                ["Could", "Родительский контур для &lt;18 (сейчас Age Gate отказ)"],
                ["Won’t", "Акции как первый шаг, крипта, маржа, отдельное приложение, выбор бумаги промптом, тёмная тема / liquid glass"],
            ],
            [28 * mm, 147 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("Риски и снятие", "H2"))
    story.append(
        tbl(
            [
                ["Риск", "Как снимаем"],
                ["Манипуляция новичком", "Только консервативный первый шаг, сравнение альтернатив"],
                ["Обещание доходности, &lt;18", "Шаблоны, Age Gate, согласие родителя в будущем контуре"],
                ["Давление «успей купить»", "Спокойный тон, учёба до сделки"],
                ["Галлюцинации ИИ", "Правила выше модели, узкий system, контекст продукта отдельно, fallback"],
                ["Лишняя персоналка", "Агрегаты, не лента трат; локальный инференс"],
                ["Фишинговые «рекомендации»", "Только внутри приложения банка"],
            ],
            [50 * mm, 125 * mm],
        )
    )

    story.append(p("6. Архитектура текущего MVP", "H1"))
    story.append(p("6.1. Формат и стек", "H2"))
    story.append(
        p(
            "Отдельный mobile-first веб (Vite + React 19 + TypeScript + React Router), рамка телефона ~390 px, "
            "светлая тема, акцент #EF3124, шрифт IBM Plex Sans. API: FastAPI + uvicorn. Портфель в RAM процесса. "
            "Рынок и клиент — стабы. Vite проксирует /api на 127.0.0.1:8000. CORS открыт для демо."
        )
    )
    story.append(
        p(
            "Поток: онбординг маскота → портфель / каталог / сделка / пульс / учёба / агент."
        )
    )
    story.append(p("6.2. Слои", "H2"))
    story.append(
        p(
            "Браузер → web (Vite) → api (FastAPI) → stubs/alfa (профиль), stubs/market (инструменты, свечи, "
            "стакан, новости), stubs/portfolio (paper-счёт) → Ollama bonsai-8b:latest (чат) или fallback-текст."
        )
    )
    story.append(p("6.3. Карта репозитория", "H2"))
    story.append(
        tbl(
            [
                ["Путь", "Роль"],
                ["web/", "UI"],
                ["server/main.py", "HTTP API"],
                ["server/stubs/alfa.py", "Профиль Ани"],
                ["server/stubs/market.py", "Каталог, котировки, OHLC, стакан, демо-новости"],
                ["server/stubs/portfolio.py", "Paper-портфель и заявки"],
                ["server/ollama_client.py", "Чат + fallback"],
                ["Modelfile", "Локальная bonsai-8b, пустой think"],
                ["architecture/", "Живая архитектура"],
                ["docs/", "Кейс, MVP, ADR, этот PDF"],
            ],
            [55 * mm, 120 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("6.4. HTTP API", "H2"))
    story.append(
        tbl(
            [
                ["Метод", "Путь", "Назначение"],
                ["GET", "/api/health", "API ok + статус Ollama"],
                ["GET", "/api/me", "Профиль"],
                ["GET", "/api/portfolio", "Кэш, позиции, onboarded, goal"],
                ["POST", "/api/onboard", "{ goal } — флаг онбординга"],
                ["GET", "/api/operations", "Лента сделок и комиссий"],
                ["GET", "/api/instruments", "?q=&amp;kind=all|stock|etf|conservative"],
                ["GET", "/api/instruments/{ticker}", "Карточка, sparkline, candles, book, metrics"],
                ["POST", "/api/orders", "paper buy|sell"],
                ["POST", "/api/agent/chat", "Ollama или fallback"],
                ["GET", "/api/pulse", "Посты"],
                ["GET", "/api/academy", "Уроки"],
            ],
            [22 * mm, 62 * mm, 91 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("6.5. Paper-ордер", "H2"))
    story.append(
        bullets(
            [
                "Старт: cash = 10 000 ₽, позиции пустые, onboarded = false.",
                "Исполнение сразу по текущей цене стаба (рынок). Limit в модели есть, демо бьёт по рынку. Нет биржи и очереди.",
                "Комиссия: max(0,05% от суммы, 1 ₽), списывается отдельно, пишется в операции.",
                "Buy без денег / sell сверх позиции → 400.",
                "Средняя цена позиции пересчитывается при докупке. day_pnl в снимке — vs avg, не «за календарный день».",
                "Рестарт uvicorn обнуляет счёт. Флаг онбординга на сервере тоже; клиент может остаться внутри из-за localStorage alfa-onboarded.",
            ]
        )
    )
    story.append(p("6.6. Рынок-стаб", "H2"))
    story.append(
        p(
            "Инструменты: LQDT, SBGB, FXRU (conservative ETF); SBER, GAZP, YDEX, VTBR (акции); TMOS (индексный ETF). "
            "Свечи: OHLC на 24 дня, последняя close ≈ текущая цена; UI режет 7/14/24. Стакан: 8 уровней bid/ask "
            "вокруг цены, подписи что это чужие заявки «сейчас». Демо-новости привязаны к тикерам, явно учебные."
        )
    )
    story.append(p("6.7. ИИ-агент", "H2"))
    story.append(
        p(
            "Модель по умолчанию bonsai-8b:latest (OLLAMA_MODEL), URL http://127.0.0.1:11434. "
            "num_predict 96, num_ctx 1024, temperature 0.3, таймаут чтения 240 с, keep_alive 30m. "
            "System: когорта 18–26, не лекция «что такое акция», без обещания доходности, не выбирать бумагу, "
            "не имитировать тест ЦБ, без юрхвоста в ответе, обращение по имени и роду. Блок клиента из get_me(). "
            "Контекст продукта (онбординг LQDT) вставляется отдельным user-сообщением [Контекст продукта]. "
            "Форс-fallback: OLLAMA_URL на закрытый порт. Профиль показывает офлайн."
        )
    )
    story.append(p("6.8. Клиентское состояние", "H2"))
    story.append(
        tbl(
            [
                ["Ключ", "Где", "Смысл"],
                ["alfa-onboarded", "localStorage", "'1' после прохождения или пропуска"],
                ["academy-done", "localStorage", "JSON прогресса уроков; API всегда done: false"],
            ],
            [40 * mm, 35 * mm, 100 * mm],
        )
    )

    story.append(p("7. Пользовательский путь и экраны", "H1"))
    story.append(p("7.1. Онбординг /onboarding", "H2"))
    story.append(
        bullets(
            [
                "Пока нет localStorage и серверного onboarded — редирект на онбординг с любого пути.",
                "Привет маскота hello, кэшбэк с карты.",
                "Цель: подушка / гаджет / поездка (маскот type).",
                "Три вопроса: горизонт, приоритет, сумма (учебный квиз, не тест ЦБ).",
                "Карточка LQDT + альтернативы SBGB / FXRU; «почему» от Ollama или fallback.",
                "Сумма взноса, покупка LQDT (buy), paper-ордер. Пропуск тоже ставит onboarded.",
            ]
        )
    )
    story.append(p("7.2. Хабы после гейта", "H2"))
    story.append(
        tbl(
            [
                ["Экран", "Что"],
                ["Портфель /", "Сумма, кэш/бумаги, баннер первого шага, плитки, активы, движение рынка, сегодня"],
                ["Каталог /catalog", "Поиск, чипы, список; баннер консервативных фондов"],
                ["Пульс /pulse", "Лента постов с тегами"],
                ["Учёба /learn", "Микроуроки; /learn/compound — калькулятор сложного процента"],
                ["Профиль /profile", "Карта/кэшбэк/копилка, статус Ollama, вход в агента"],
            ],
            [48 * mm, 127 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("7.3. Дочерние окна (таббар скрыт, стрелка в красной шапке)", "H2"))
    story.append(
        p(
            "/instrument/:ticker — свечи, стакан, метрики, Купить/Продать. /buy/:ticker — заявка, ?side=sell. "
            "/operations — лента. /analytics — PnL, покупки/продажи/комиссии, состав. /agent — мессенджер. "
            "/pulse/:id, /learn/:id. parentOf() задаёт назад: инструмент/покупка → каталог, агент → профиль, "
            "операции/аналитика → портфель."
        )
    )
    story.append(p("7.4. Маскот и дизайн", "H2"))
    story.append(
        p(
            "hello — речь, онбординг, пульс, учёба. sit-in-front-of-computer — ввод, квиз, заявка. "
            "buy — подтверждение покупки. crying — empty state. avatar — чат. Шапка заливка #EF3124, "
            "«АЛЬФА ИНВЕСТИЦИИ». CTA красные, радиус ~10 px, без теней и стекла. Свечи: зелёный вверх, "
            "красный вниз. На узком экране телефон на весь viewport."
        )
    )

    story.append(p("8. План распределённой системы (упражнение, не прод)", "H1"))
    story.append(
        p(
            "architecture/distributed.md: слои «как на много пользователей», крутится локально в Docker Compose. "
            "Не лям RPS. Сейчас один FastAPI, портфель в RAM, один клиент без логина, Ollama сбоку."
        )
    )
    story.append(
        tbl(
            [
                ["Тема", "Решение"],
                ["Сделки", "Paper, исполнение сразу в API, без matching engine"],
                ["Юзер", "В проде SSO банка. Здесь user_id «уже после логина»"],
                ["Правда", "Один Postgres: юзер, кэш, позиции, ордера, операции, каталог, пульс, академия"],
                ["Котировки", "Redis last/стакан/sparkline. Пишет API при старте или cache-miss"],
                ["Деньги", "numeric, не float"],
                ["Агент", "Профиль gpu в Compose, api без depends_on Ollama"],
                ["Не брать", "Kafka, k8s, nginx, второй инстанс API, лента MOEX"],
            ],
            [35 * mm, 140 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Каталог ≠ котировка: меню редко — Postgres; табло часто — Redis. Пропажа Redis допустима "
            "(перегреть из стаба). Пропажа Postgres — потеря счёта, недопустима. Volume только у Postgres. "
            "Путь от MVP: 1) Postgres + user_id, убрать in-memory; 2) сиды каталога и контента; 3) Redis; "
            "4) docker-compose.yml; 5) профиль Ollama."
        )
    )

    story.append(p("9. Контур Альфа PRO WebSocket API (ориентир на прод)", "H1"))
    story.append(
        p(
            "В architecture/alfa-bank-api.md лежит спецификация PRO WebSocket API Альфа-Инвестиций "
            "(локальный терминал, роутер ws://127.0.0.1:3366/router/). Это не то, чем ходит MVP: демо "
            "сидит на REST-стабах. Документ нужен как карта, чем заменять стабы при встройке в банк."
        )
    )
    story.append(
        bullets(
            [
                "Роутер: RoutingRequest / RoutingError. Команды listen, unlisten, broadcast, register, unregister, request, response.",
                "Каналы: шина (много подписчиков) и сервис-респондер (один обязан отвечать).",
                "Публикация табличных сущностей на #Data.Bus.&lt;EntityType&gt;.",
                "Сервисы терминала покрывают портфель, заявки, котировки, справочники — будущий контракт вместо server/stubs/.",
                "Открытый PRO API у прода — киллер-фича автоматизаторов; наш кейс его не дублирует, а учит первого взноса до робота.",
            ]
        )
    )

    story.append(p("10. Правовая стратегия", "H1"))
    story.append(
        p(
            "Сводки в architecture/pravovaya-baza-*.md. Не юридическая консультация: перед запуском сверка "
            "с актуальной редакцией и юристом по финансовому праву."
        )
    )
    story.append(
        p(
            "<b>Водораздел:</b> пока продукт — образовательный симулятор с виртуальными деньгами и без "
            "персональных инвестрекомендаций, он вне лицензирования ЦБ как брокер/советник. Реальные сделки "
            "или индивидуальные советы («тебе стоит купить») — другой режим: 39-ФЗ ст. 6.1, реестр инвестсоветников, "
            "для сложных инструментов — тест неквала ст. 3.1. Поэтому агент запрещает «тебе стоит купить» и "
            "выбор бумаги."
        )
    )
    story.append(
        tbl(
            [
                ["Норма", "Как это ложится на наше решение"],
                ["39-ФЗ квалификация и тест неквала", "Учебный квиз явно не тест ЦБ; system запрещает имитацию квалификации"],
                ["39-ФЗ ст. 6.1 инвестконсультирование", "Правила выбирают продукт; ИИ только объясняет уже выбранное"],
                ["152-ФЗ ПДн и ст. 18 локализация", "Нет зарубежного SaaS аналитики; Ollama локально; &lt;18 не пускаем"],
                ["436-ФЗ маркировка", "Образовательный контент; темы риска — консервативно"],
                ["38-ФЗ ст. 28 реклама финансов", "Не обещать доходность; калькулятор сложного процента подписан «не прогноз»"],
                ["244-ФЗ азарт", "Нет лутбоксов и денежных призов за случайный исход"],
                ["149-ФЗ информация", "Пульс — контент банка, не пользовательская соцсеть"],
                ["Магазины приложений", "Демо — веб; прод в банке не отдельный стор-рейтинг"],
                ["Стратегия ЦБ до 2030", "Поведение и привычка, не только знания — совпадает с First Conscious Contribution"],
            ],
            [48 * mm, 127 * mm],
        )
    )

    story.append(p("11. Метрики и промо", "H1"))
    story.append(
        p(
            "Воронка: показ виджета → старт → обучение → риск-профиль → выбор → счёт → первый взнос → повтор за 30 дней. "
            "A/B: виджет против текущего пути «Инвестиции» — в репозитории не реализован. "
            "Промо-сообщение: «Знаешь, что такое вклад и риск. Первый шаг — маленькая сумма, без обещания заработка»."
        )
    )
    story.append(
        p(
            "В коде метрики ещё не инструментированы. Это продуктовый контур кейса, не дашборд."
        )
    )

    story.append(p("12. Что сознательно не делали", "H1"))
    story.append(
        bullets(
            [
                "Свечной зум, realtime-стакан, живая биржа, matching engine.",
                "Соцсеть блогеров, налоговые отчёты, маржа, крипта, тёмная тема.",
                "Отдельное приложение, обещание доходности, выбор актива промптом.",
                "Родительский стоп-кран (Could). Kafka/k8s «для красоты слайда».",
            ]
        )
    )

    story.append(p("13. Как запустить демо", "H1"))
    story.append(
        p(
            "Терминал 1: source .venv/bin/activate && cd server && uvicorn main:app --host 127.0.0.1 --port 8000<br/>"
            "Терминал 2: cd web && npm run dev<br/>"
            "Открыть http://127.0.0.1:5173<br/>"
            "Ollama: ollama create bonsai-8b -f Modelfile && ollama serve. "
            "Выключить модель только для приложения: OLLAMA_URL=http://127.0.0.1:1 перед uvicorn."
        )
    )

    story.append(p("14. Краткая формула решения", "H1"))
    story.append(
        p(
            "Когорта 18–26 знает рынок и боится практики. Мы не учим азбуке и не даём робота-советника. "
            "Мы берём банковский контекст, правилами кладём человека в LQDT от 100 ₽, моделью объясняем "
            "почему не акции, затем даём учебный брокер, чтобы привычка появилась на бумаге, а не на страхе. "
            "Архитектура сегодня — один процесс и стабы. Архитектура завтра — Postgres как правда, Redis как "
            "табло, SSO банка, тот же запрет «ИИ не выбирает бумагу». Право держит продукт в зоне симулятора, "
            "пока нет реальных поручений и персональных рекомендаций."
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Альфа-будущее: архитектура и стратегии",
        author="Кейс Альфа-будущее",
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    build()
