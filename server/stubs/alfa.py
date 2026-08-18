"""Stub: Alfa Bank client profile."""

from __future__ import annotations

import os


def get_me() -> dict:
    age = int(os.getenv("DEMO_AGE", "21"))
    return {
        "id": "u-demo-1824",
        "name": "Аня",
        "gender": "female",
        "age": age,
        "currency": "RUB",
        "balance": 12450.0,
        "cashback": 780.0,
        "piggy": 3200.0,
        "salary": True,
        "has_invest_account": False,
        "cohort": "18-26",
    }
