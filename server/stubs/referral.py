"""Share-only referral: code, claim, invited_count. No reward."""

from __future__ import annotations

import hashlib

from .identity import ANYA_ID

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

_user_to_code: dict[str, str] = {}
_code_to_user: dict[str, str] = {}
_invitee_to_inviter: dict[str, str] = {}


def _mint(user_id: str, salt: int = 0) -> str:
    seed = f"{user_id}:{salt}".encode()
    n = int.from_bytes(hashlib.sha256(seed).digest()[:8], "big")
    chars: list[str] = []
    for _ in range(6):
        chars.append(_ALPHABET[n % len(_ALPHABET)])
        n //= len(_ALPHABET)
    return "".join(chars)


def code_for(user_id: str) -> str:
    existing = _user_to_code.get(user_id)
    if existing:
        return existing
    salt = 0
    while True:
        code = _mint(user_id, salt)
        owner = _code_to_user.get(code)
        if owner is None or owner == user_id:
            _user_to_code[user_id] = code
            _code_to_user[code] = user_id
            return code
        salt += 1


def invited_count(user_id: str) -> int:
    return sum(1 for inviter in _invitee_to_inviter.values() if inviter == user_id)


def snapshot(user_id: str) -> dict:
    code = code_for(user_id)
    return {
        "code": code,
        "path": f"/onboarding?ref={code}",
        "invited_count": invited_count(user_id),
    }


def claim(code: str, invitee_id: str) -> dict:
    cleaned = (code or "").strip().upper()
    if len(cleaned) < 4:
        raise ValueError("Нет такого кода")
    inviter = _code_to_user.get(cleaned)
    if not inviter:
        # Lazy-register default Anya so a pasted demo code still resolves after restart
        if cleaned == code_for(ANYA_ID):
            inviter = ANYA_ID
        else:
            raise ValueError("Нет такого кода")
    if inviter == invitee_id:
        raise ValueError("Нельзя пригласить себя")
    prev = _invitee_to_inviter.get(invitee_id)
    if prev and prev != inviter:
        raise ValueError("Уже есть приглашение")
    _invitee_to_inviter[invitee_id] = inviter
    return {"ok": True, "invited_count": invited_count(inviter)}


code_for(ANYA_ID)
