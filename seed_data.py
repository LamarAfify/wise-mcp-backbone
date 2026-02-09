
import sys
import os
import sqlite3

# Ensure app module can be found
sys.path.append(os.getcwd())

from app.storage import init_db, create_project, add_user, log_task_history, create_milestone
from app.schemas import Project, User, TaskHistory, Milestone
from app.config import DB_PATH
import datetime

def seed():
    print(f"Seeding database at {DB_PATH}")
    init_db(DB_PATH)

    # Clean up existing (optional, but good for idempotency if we had delete)
    # For now, just try to create. UUIDs usually prevent collision, but here we hardcode for testing.
    
    # Create Project
    try:
        p = Project(id="proj-1", name="North AI Workflow Hub", deadline="2025-01-31", status="active", created_at=datetime.datetime.utcnow().isoformat())
        create_project(DB_PATH, p)
        print("Project created.")
    except sqlite3.IntegrityError:
        print("Project already exists.")

    # Create Users
    users = [
        User(id="u1", name="Lamar", skills={"coding": 0.9, "writing": 0.6}),
        User(id="u2", name="Serena", skills={"writing": 0.9, "analytics": 0.4}),
        User(id="u3", name="Vishaka", skills={"analytics": 0.9, "coding": 0.5}),
    ]
    for u in users:
        try:
            add_user(DB_PATH, u)
            print(f"User {u.name} added.")
        except Exception as e:
            print(f"Error adding user {u.name}: {e}")

    # History for Vishaka (Analytics expert)
    # Simulate that she is fast and rated high
    try:
        log_task_history(DB_PATH, TaskHistory(
            id="h1", user_id="u3", task_type="analytics", duration_minutes=30, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()
        ))
        log_task_history(DB_PATH, TaskHistory(
            id="h2", user_id="u3", task_type="analytics", duration_minutes=25, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()
        ))
    except sqlite3.IntegrityError:
        pass

    # History for Serena (Writing expert)
    try:
        log_task_history(DB_PATH, TaskHistory(
            id="h3", user_id="u2", task_type="writing", duration_minutes=45, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()
        ))
    except sqlite3.IntegrityError:
        pass

    # History for Lamar (Coding expert)
    try:
        log_task_history(DB_PATH, TaskHistory(
            id="h4", user_id="u1", task_type="coding", duration_minutes=60, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()
        ))
    except sqlite3.IntegrityError:
        pass

    # Milestones
    milestones = [
        Milestone(id="m1", project_id="proj-1", title="Project Onboarding", status="completed", completed_at=datetime.datetime.utcnow().isoformat()),
        Milestone(id="m2", project_id="proj-1", title="Backend API", status="in_progress", due_date="2025-01-20"),
        Milestone(id="m3", project_id="proj-1", title="Frontend UI", status="pending", due_date="2025-01-25"),
    ]
    for m in milestones:
        try:
            create_milestone(DB_PATH, m)
            print(f"Milestone {m.title} added.")
        except sqlite3.IntegrityError:
            pass

if __name__ == "__main__":
    seed()
