from __future__ import annotations

from ..utils import utc_now_iso


def health_check() -> dict:
    return {"status": "ok", "time": utc_now_iso()}
