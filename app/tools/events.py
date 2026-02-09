from __future__ import annotations

from typing import Any, Dict, Optional

from ..schemas import Event
from ..utils import new_id, utc_now_iso
from ..storage import insert_event, query_events


def log_event(
    db_path: str,
    type: str,
    team: str,
    severity: str = "P3",
    timestamp: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> dict:
    evt = Event(
        id=new_id("evt"),
        type=type,
        team=team,
        severity=severity,
        timestamp=timestamp or utc_now_iso(),
        payload=payload or {},
    )
    insert_event(db_path, evt)
    return {"ok": True, "event": evt.model_dump()}


def list_events(
    db_path: str,
    team: Optional[str] = None,
    type: Optional[str] = None,
    severity: Optional[str] = None,
    start_ts: Optional[str] = None,
    end_ts: Optional[str] = None,
    limit: int = 50,
) -> dict:
    rows = query_events(
        db_path=db_path,
        team=team,
        event_type=type,
        severity=severity,
        start_ts=start_ts,
        end_ts=end_ts,
        limit=limit,
    )
    return {"count": len(rows), "events": rows}
