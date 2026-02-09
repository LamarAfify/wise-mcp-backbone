
from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

from .schemas import Event, Project, User, Milestone, TaskHistory


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    conn = _connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            team TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            skills_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS milestones (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            assigned_to TEXT,
            due_date TEXT,
            completed_at TEXT,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS task_history (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            task_type TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            success_rating INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.commit()
    conn.close()


# -----------------------
# Events
# -----------------------

def insert_event(db_path: str, event: Event) -> None:
    import json

    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (id, type, team, severity, timestamp, payload_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            event.id,
            event.type,
            event.team,
            event.severity,
            event.timestamp,
            json.dumps(event.payload, ensure_ascii=False),
        ),
    )
    conn.commit()
    conn.close()


def query_events(
    db_path: str,
    team: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    start_ts: Optional[str] = None,
    end_ts: Optional[str] = None,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    import json

    conn = _connect(db_path)
    cur = conn.cursor()

    where = []
    params: List[Any] = []

    if team:
        where.append("team = ?")
        params.append(team)
    if event_type:
        where.append("type = ?")
        params.append(event_type)
    if severity:
        where.append("severity = ?")
        params.append(severity)
    if start_ts:
        where.append("timestamp >= ?")
        params.append(start_ts)
    if end_ts:
        where.append("timestamp <= ?")
        params.append(end_ts)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
        SELECT id, type, team, severity, timestamp, payload_json
        FROM events
        {where_sql}
        ORDER BY timestamp DESC
        LIMIT ?
    """
    params.append(limit)

    rows = cur.execute(sql, params).fetchall()
    conn.close()

    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "type": r["type"],
                "team": r["team"],
                "severity": r["severity"],
                "timestamp": r["timestamp"],
                "payload": json.loads(r["payload_json"]),
            }
        )
    return out



# -----------------------
# Workflow Hub Functions
# -----------------------

def create_project(db_path: str, project: Project) -> None:
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO projects (id, name, deadline, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (project.id, project.name, project.deadline, project.status, project.created_at),
    )
    conn.commit()
    conn.close()

def add_user(db_path: str, user: User) -> None:
    import json
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (id, name, role, skills_json) VALUES (?, ?, ?, ?)",
        (user.id, user.name, user.role, json.dumps(user.skills)),
    )
    conn.commit()
    conn.close()

def create_milestone(db_path: str, milestone: Milestone) -> None:
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO milestones (id, project_id, title, status, assigned_to, due_date, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (milestone.id, milestone.project_id, milestone.title, milestone.status, milestone.assigned_to, milestone.due_date, milestone.completed_at),
    )
    conn.commit()
    conn.close()

def update_milestone_status(db_path: str, milestone_id: str, status: str, completed_at: Optional[str] = None) -> None:
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE milestones SET status = ?, completed_at = ? WHERE id = ?",
        (status, completed_at, milestone_id),
    )
    conn.commit()
    conn.close()

def log_task_history(db_path: str, history: TaskHistory) -> None:
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO task_history (id, user_id, task_type, duration_minutes, success_rating, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (history.id, history.user_id, history.task_type, history.duration_minutes, history.success_rating, history.timestamp),
    )
    conn.commit()
    conn.close()

def get_project_details(db_path: str) -> Dict[str, Any]:
    # Simplifying: get all projects and milestones (assuming single active project context for now or returning list)
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    projects = cur.execute("SELECT * FROM projects").fetchall()
    users = cur.execute("SELECT * FROM users").fetchall()
    milestones = cur.execute("SELECT * FROM milestones").fetchall()
    
    conn.close()
    
    return {
        "projects": [dict(p) for p in projects],
        "users": [dict(u) for u in users],
        "milestones": [dict(m) for m in milestones]
    }

def get_user_performance(db_path: str, user_id: str) -> List[Dict[str, Any]]:
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM task_history WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
