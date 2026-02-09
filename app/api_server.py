
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import sqlite3
import json
import os

from app.storage import _connect, get_project_details, get_user_performance, add_user, create_project, create_milestone, log_task_history
from app.schemas import Project, User, Milestone, TaskHistory
from app.config import DB_PATH
from app.tools.workflow import recommend_task_assignee

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard")
def get_dashboard():
    return get_project_details(DB_PATH)

@app.post("/users")
def create_user(user: User):
    add_user(DB_PATH, user)
    return {"status": "success"}

@app.post("/projects")
def new_project(project: Project):
    create_project(DB_PATH, project)
    return {"status": "success"}

@app.post("/milestones")
def add_milestone_endpoint(milestone: Milestone):
    create_milestone(DB_PATH, milestone)
    return {"status": "success"}

@app.post("/milestones/{id}/complete")
def complete_milestone_endpoint(id: str):
    from datetime import datetime
    from app.storage import update_milestone_status
    import datetime as dt
    update_milestone_status(DB_PATH, id, "completed", completed_at=dt.datetime.utcnow().isoformat())
    return {"status": "success"}

@app.post("/history")
def add_history(history: TaskHistory):
    log_task_history(DB_PATH, history)
    return {"status": "success"}

@app.get("/recommend/{project_id}/{task_type}")
def get_recommendation(project_id: str, task_type: str):
    # Get all users as candidates
    conn = _connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    users = cur.execute("SELECT id FROM users").fetchall()
    conn.close()
    
    candidate_ids = [u["id"] for u in users]
    if not candidate_ids:
        return {"recommended_user_id": None}
        
    rec_id = recommend_task_assignee(DB_PATH, project_id, task_type, candidate_ids)
    return {"recommended_user_id": rec_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
