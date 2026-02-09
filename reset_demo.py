
import sys
import os
import sqlite3

# Ensure app module can be found
sys.path.append(os.getcwd())

from app.storage import init_db, add_user, log_task_history
from app.schemas import User, TaskHistory
from app.config import DB_PATH
import datetime

def reset():
    print(f"Resetting database at {DB_PATH}")
    
    # 1. Remove existing DB file to clear all projects/milestones
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Existing database removed.")

    # 2. Re-initialize tables
    init_db(DB_PATH)
    print("Database Schema initialized.")

    # 3. Seed ONLY Users and History (No Projects)
    # This prepares the Recommendation Engine but leaves the "Stage" empty for the demo
    
    users = [
        User(id="u1", name="Lamar", skills={"coding": 0.9, "writing": 0.6}),
        User(id="u2", name="Serena", skills={"writing": 0.9, "analytics": 0.4}),
        User(id="u3", name="Vishaka", skills={"analytics": 0.9, "coding": 0.5}),
    ]
    for u in users:
        add_user(DB_PATH, u)
    
    print("Users seeded.")

    # History for Recommendations
    history_items = [
        # Vishaka - Analytics
        TaskHistory(id="h1", user_id="u3", task_type="analytics", duration_minutes=30, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()),
        TaskHistory(id="h2", user_id="u3", task_type="analytics", duration_minutes=25, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()),
        # Serena - Writing
        TaskHistory(id="h3", user_id="u2", task_type="writing", duration_minutes=45, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()),
        # Lamar - Coding
        TaskHistory(id="h4", user_id="u1", task_type="coding", duration_minutes=60, success_rating=5, timestamp=datetime.datetime.utcnow().isoformat()),
    ]
    
    for h in history_items:
        log_task_history(DB_PATH, h)

    print("History seeded. Ready for Demo!")

if __name__ == "__main__":
    reset()
