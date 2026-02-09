# tools/resources.py

import sqlite3
from datetime import datetime
import json


def ensure_resource_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS resource_state (
            id TEXT PRIMARY KEY,
            updated_at TEXT NOT NULL,
            status TEXT NOT NULL,
            capacity REAL,
            owner TEXT,
            team TEXT,
            notes TEXT,
            metadata TEXT
        )
        """
    )
    conn.commit()


def update_resource_state(
    db_path: str,
    id: str,
    status: str = "unknown",
    capacity: float | None = None,
    owner: str | None = None,
    team: str | None = None,
    notes: str | None = None,
    metadata: dict | None = None,
):
    conn = sqlite3.connect(db_path)
    ensure_resource_table(conn)

    now = datetime.utcnow().isoformat()
    metadata_json = json.dumps(metadata or {})

    conn.execute(
        """
        INSERT INTO resource_state (id, updated_at, status, capacity, owner, team, notes, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            updated_at=excluded.updated_at,
            status=excluded.status,
            capacity=excluded.capacity,
            owner=excluded.owner,
            team=excluded.team,
            notes=excluded.notes,
            metadata=excluded.metadata
        """,
        (id, now, status, capacity, owner, team, notes, metadata_json),
    )
    conn.commit()
    conn.close()

    return {
        "id": id,
        "updated_at": now,
        "status": status,
        "capacity": capacity,
        "owner": owner,
        "team": team,
        "notes": notes,
    }


def get_resource_state(db_path: str, id: str):
    conn = sqlite3.connect(db_path)
    ensure_resource_table(conn)

    row = conn.execute(
        "SELECT id, updated_at, status, capacity, owner, team, notes, metadata FROM resource_state WHERE id = ?",
        (id,),
    ).fetchone()
    conn.close()

    if not row:
        return {
            "found": False,
            "id": id,
            "status": "unknown",
            "message": "No resource state found.",
        }

    return {
        "found": True,
        "id": row[0],
        "updated_at": row[1],
        "status": row[2],
        "capacity": row[3],
        "owner": row[4],
        "team": row[5],
        "notes": row[6],
        "metadata": json.loads(row[7] or "{}"),
    }

