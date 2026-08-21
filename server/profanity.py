"""Sanitize assistant replies: profanity, prompt-leak, violent/extremist roleplay."""

from __future__ import annotations

import re

SAFE_REPLY = "Давайте поговорим о чем-то другом"
TOPIC_REDIRECT = (
    "Это не про инвестиции. Давай лучше про первый взнос, риск или фонд денежного рынка — с чего начнём?"
)

# Stems of common Russian mat and frequent English swears.
# Short ambiguous fragments (ебу; блять inside потреблять) are avoided.
_STEMS = (
    "хуй",
    "хуя",
    "хуё",
    "хуи",
    "хую",
    "хуйня",
    "хуета",
    "хуев",
    "пизд",
    "спизд",
    "бляд",
    "ебать",
    "ебан",
    "ебал",
    "ебло",
    "ебуч",
    "заеб",
    "наеб",
    "проеб",
    "выеб",
    "уебок",
    "уебан",
    "мудак",
    "мудил",
    "пидор",
    "пидар",
    "педик",
    "гондон",
    "гандон",
    "долбоеб",
    "охуе",
    "нахер",
    "похер",
    "херня",
    "херни",
    "залуп",
    "пенис",
    "вагин",
    "fuck",
    "bitch",
    "shit",
    "asshole",
    "cunt",
)

# Whole words only — "блять" is a suffix of потреблять/оскорблять.
_WORD_RE = re.compile(
    r"(?<![а-яa-zё])"
    r"(?:бля|блять|блядь|сука|суки|суку|суке|жопа|жопу|жопе|жопой)"
    r"(?![а-яa-zё])",
    re.IGNORECASE,
)

# Distinctive fragments from SYSTEM / client block.
_LEAK_MARKERS = (
    "обращайся в женском роде",
    "обращайся в мужском роде",
    "имя в обращении",
    "готова, поняла, начала, молодчица",
    "готов, понял, начал, молодец",
    "не читай лекцию",
    "учебный paper",
    "не имитируй тест банка россии",
    "ты — помощник альфа",
    "ты - помощник альфа",
    "не советуй акции, крипту и маржу",
    "соблюдай род",
)

_REPEAT_ROOT_RE = re.compile(r"(?:хуя|хуй){2,}|(?:ху){3,}")

# Output: violence-as-aesthetics, genocide framing, dehumanization.
_HARM_PHRASES = (
    "убийство это не драма",
    "убийство — это не драма",
    "убийство - это не драма",
    "you are a weed",
    "youre a weed",
    "you're a weed",
    "garden needs to be clean",
    "the garden needs to be clean",
    "сад должен быть чист",
    "сад нужно чистить",
    "untermensch",
    "унтерменш",
    "final solution",
    "окончательное решение",
)

_KILL_MARKERS = (
    "убийств",
    "убивает",
    "убиваю",
    "серийный убийц",
    "serial killer",
    "serialkiller",
    "маньяк",
)

_KILL_AESTHETIC = (
    "не драма",
    "это чистота",
    "это - чистота",
    "это — чистота",
    "убирает проблему",
    "убираю проблему",
    "чистота",
)

_NAZI_MARKERS = (
    "нацист",
    "nazi",
    "гестапо",
    "gestapo",
    "ss officer",
    "ssofficer",
    "третий рейх",
    "third reich",
    "геноцид",
    "genocide",
    "холокост",
    "holocaust",
)

_DEHUMANIZE = (
    "сорняк",
    "weed",
    "недочеловек",
    "подчеловек",
)

_GARDEN_CLEAN = (
    "сад",
    "garden",
    "огород",
)

_SCENE_MARKERS = (
    "допрос",
    "interrogat",
    "пытка",
    "пыток",
    "пытать",
    "заключен",
    "prisoner",
    "камер",
    "тюремщик",
    "концлагер",
)

_XENO_MARKERS = (
    "ксенофоб",
    "xenophob",
    "расизм",
    "racist",
    "racism",
    "расов",
)

# User asks to play the scene (refuse before generation).
_JAILBREAK_INTENT = (
    "serial killer",
    "серийный убийц",
    "монолог убийц",
    "nazi officer",
    "нацистский офицер",
    "нацист и заключ",
    "play a nazi",
    "ты нацист",
    "ты убийца",
    "interrogation scene",
    "сцена допроса",
    "сцена пыт",
    "literary form",
    "как заключенн",
    "officer + prisoner",
    "officer and prisoner",
)


def _fold(text: str) -> str:
    return text.lower().replace("ё", "е")


def _compact(text: str) -> str:
    """Drop separators so «ху-я», «х у й», «х.у.й» collapse to the stem."""
    return re.sub(r"[^а-яa-z]+", "", _fold(text))


def _stems_hit(haystack: str) -> bool:
    return any(stem.replace("ё", "е") in haystack for stem in _STEMS)


def _any_in(haystack: str, needles: tuple[str, ...]) -> bool:
    return any(n in haystack for n in needles)


def is_prompt_leak(text: str) -> bool:
    folded = _fold(text)
    return any(marker in folded for marker in _LEAK_MARKERS)


def is_profane(text: str) -> bool:
    if not text:
        return False
    folded = _fold(text)
    compact = _compact(text)
    if _WORD_RE.search(folded):
        return True
    if _stems_hit(folded) or _stems_hit(compact):
        return True
    if _REPEAT_ROOT_RE.search(compact):
        return True
    return False


def is_harmful(text: str) -> bool:
    """Violence glorification, genocide/nazi roleplay, interrogation-xenophobia."""
    if not text:
        return False
    folded = _fold(text)
    compact = _compact(text)

    if _any_in(folded, _HARM_PHRASES) or _any_in(compact, tuple(_compact(p) for p in _HARM_PHRASES)):
        return True

    kill = _any_in(folded, _KILL_MARKERS) or _any_in(compact, ("serialkiller", "серийныйубийц"))
    if kill and _any_in(folded, _KILL_AESTHETIC):
        return True

    nazi = _any_in(folded, _NAZI_MARKERS) or "nazi" in compact or "геноцид" in compact
    if nazi:
        return True

    if _any_in(folded, _DEHUMANIZE) and _any_in(folded, _GARDEN_CLEAN):
        return True
    if "weed" in compact and "garden" in compact:
        return True

    scene = _any_in(folded, _SCENE_MARKERS)
    xeno = _any_in(folded, _XENO_MARKERS)
    if scene and xeno:
        return True
    if scene and "страх" in folded and _any_in(
        folded, ("чуж", "мигрант", "иностран", "foreign", "другой народ", "другой рас")
    ):
        return True
    if xeno and _any_in(folded, ("это страх", "как страх", "страх другого", "страх чуж")):
        return True

    return False


def is_jailbreak_request(text: str) -> bool:
    if not text:
        return False
    folded = _fold(text)
    compact = _compact(text)
    if _any_in(folded, _JAILBREAK_INTENT):
        return True
    if _any_in(compact, ("serialkiller", "naziofficer", "interrogationscene")):
        return True
    if "убийц" in folded and _any_in(folded, ("серийн", "монолог", "сыграй", "роль убий")):
        return True
    if "нацист" in folded and _any_in(folded, ("офицер", "заключ", "плен", "сыграй", "роль")):
        return True
    if is_harmful(text):
        return True
    return False


def is_blocked(text: str) -> bool:
    return is_profane(text) or is_prompt_leak(text) or is_harmful(text)


_GREET_RE = re.compile(
    r"^(?:привет(?:ик)?|прив|здравствуй(?:те)?|добр(?:ый|ое)\s+(?:день|утро|вечер)|хай|hello|hi|hey)"
    r"[\s!.?,]*$",
    re.IGNORECASE,
)

_TOPIC_MARKERS = (
    "инвест",
    "вклад",
    "влож",
    "акци",
    "облигац",
    "офз",
    "фонд",
    "бпиф",
    "etf",
    "портфел",
    "брокер",
    "бирж",
    "дивиденд",
    "купон",
    "доходност",
    "инфляц",
    "риск",
    "кэшбэк",
    "кешбек",
    "копилк",
    "lqdt",
    "sbgb",
    "fxru",
    "иис",
    "налог",
    "тикер",
    "бумаг",
    "руб",
    "капитал",
    "накоп",
    "подушк",
    "комисс",
    "счёт",
    "счет",
    "альфа",
    "денежн",
    "волатил",
    "диверсиф",
    "горизонт",
    "взнос",
    "котиров",
    "экономик",
    "финанс",
    "бюджет",
    "депозит",
    "процент",
    "деньг",
    "денег",
    "деньги",
    "доход",
    "рынок",
    "ликвидн",
    "консерватив",
    "ключев",
    "новичк",
    "инструмент",
    "стратег",
    "банк",
    "пай",
    "паев",
    "управляющ",
)


def is_greeting(text: str) -> bool:
    return bool(_GREET_RE.match((text or "").strip()))


def is_invest_topic(text: str) -> bool:
    if not text:
        return False
    folded = _fold(text)
    compact = _compact(text)
    if "₽" in text:
        return True
    if _any_in(folded, _TOPIC_MARKERS):
        return True
    if _any_in(compact, ("lqdt", "sbgb", "fxru", "etf", "бпиф", "иис")):
        return True
    return False


def filter_reply(text: str, *, require_topic: bool = False) -> str:
    if is_blocked(text):
        return SAFE_REPLY
    # Soft: long answers without any invest markers look like drift.
    # Short definitions often omit buzzwords — do not redirect them.
    if require_topic and len(text) > 120 and not is_invest_topic(text):
        return TOPIC_REDIRECT
    return text
