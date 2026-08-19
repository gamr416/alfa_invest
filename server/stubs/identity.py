"""Demo identity: RAM user_id from X-Demo-User, else default Anya."""

from __future__ import annotations

import re

ANYA_ID = "u-demo-1824"
_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,80}$")


def resolve(header: str | None) -> str:
    if not header:
        return ANYA_ID
    raw = header.strip()
    if not _ID_RE.fullmatch(raw):
        return ANYA_ID
    return raw
