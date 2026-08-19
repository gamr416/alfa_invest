"""Sanitize assistant replies: profanity, obfuscation, prompt-leak."""

from __future__ import annotations

import re

SAFE_REPLY = "давайте поговорим о чем-то другом"

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


def _fold(text: str) -> str:
    return text.lower().replace("ё", "е")


def _compact(text: str) -> str:
    """Drop separators so «ху-я», «х у й», «х.у.й» collapse to the stem."""
    return re.sub(r"[^а-яa-z]+", "", _fold(text))


def _stems_hit(haystack: str) -> bool:
    return any(stem.replace("ё", "е") in haystack for stem in _STEMS)


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


def filter_reply(text: str) -> str:
    if is_profane(text) or is_prompt_leak(text):
        return SAFE_REPLY
    return text
