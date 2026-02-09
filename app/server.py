import argparse

from north_mcp_python_sdk import NorthMCPServer

from .config import APP_NAME, PORT, SERVER_SECRET, DB_PATH, DEBUG
from .storage import init_db
from .tools.health import health_check
from .tools.events import log_event, list_events

from .storage import create_project, add_user, create_milestone, update_milestone_status, log_task_history, get_project_details
from .schemas import Project, User, Milestone, TaskHistory
from .tools.workflow import recommend_task_assignee
from typing import List



def create_server():
    init_db(DB_PATH)

    kwargs = {"name": APP_NAME, "port": PORT, "debug": DEBUG}
    if SERVER_SECRET:
        kwargs["server_secret"] = SERVER_SECRET

    mcp = NorthMCPServer(**kwargs)

    @mcp.tool()
    def Lamar_Afify_v2_health_check():
        return health_check()

    @mcp.tool()
    def Lamar_Afify_v2_log_event(
        type: str,
        team: str,
        severity: str = "P3",
        timestamp: str = "",
        payload: dict = None,
    ):
        # Keep defaults simple for MCP parser
        if payload is None:
            payload = {}
        if not timestamp:
            timestamp = None  # let downstream set now
        return log_event(
            db_path=DB_PATH,
            type=type,
            team=team,
            severity=severity,
            timestamp=timestamp,
            payload=payload,
        )

    @mcp.tool()
    def Lamar_Afify_v2_list_events(
        team: str = "",
        type: str = "",
        severity: str = "",
        start_ts: str = "",
        end_ts: str = "",
        limit: int = 50,
    ):
        # Convert empty strings -> None so filters behave nicely
        team = team or None
        type = type or None
        severity = severity or None
        start_ts = start_ts or None
        end_ts = end_ts or None

        return list_events(
            db_path=DB_PATH,
            team=team,
            type=type,
            severity=severity,
            start_ts=start_ts,
            end_ts=end_ts,
            limit=limit,
        )

    @mcp.tool()
    def Lamar_Afify_v2_create_project(
        id: str,
        name: str,
        deadline: str,
        status: str = "active",
        created_at: str = None
    ):
        from datetime import datetime
        if not created_at: created_at = datetime.utcnow().isoformat()
        
        project = Project(id=id, name=name, deadline=deadline, status=status, created_at=created_at)
        create_project(DB_PATH, project)
        return {"status": "success", "project_id": id}

    @mcp.tool()
    def Lamar_Afify_v2_onboard_user(id: str, name: str, role: str = "member", skills: dict = None):
        if skills is None: skills = {}
        user = User(id=id, name=name, role=role, skills=skills)
        add_user(DB_PATH, user)
        return {"status": "success", "user_id": id}

    @mcp.tool()
    def Lamar_Afify_v2_add_milestone(
        id: str, project_id: str, title: str, due_date: str = None, assigned_to: str = None
    ):
        ms = Milestone(id=id, project_id=project_id, title=title, due_date=due_date, assigned_to=assigned_to)
        create_milestone(DB_PATH, ms)
        return {"status": "success", "milestone_id": id}

    @mcp.tool()
    def Lamar_Afify_v2_complete_milestone(id: str):
        from datetime import datetime
        update_milestone_status(DB_PATH, id, "completed", completed_at=datetime.utcnow().isoformat())
        return {"status": "success", "milestone_id": id}

    @mcp.tool()
    def Lamar_Afify_v2_get_dashboard():
        return get_project_details(DB_PATH)

    @mcp.tool()
    def Lamar_Afify_v2_recommend_assignee(project_id: str, task_type: str, candidate_users: List[str]):
        recommended_user = recommend_task_assignee(DB_PATH, project_id, task_type, candidate_users)
        return {"recommended_user_id": recommended_user, "task_type": task_type}

    @mcp.tool()
    def Lamar_Afify_v2_log_work(
        id: str, user_id: str, task_type: str, duration: int, rating: int
    ):
        from datetime import datetime
        history = TaskHistory(
            id=id,
            user_id=user_id,
            task_type=task_type,
            duration_minutes=duration,
            success_rating=rating,
            timestamp=datetime.utcnow().isoformat()
        )
        log_task_history(DB_PATH, history)
        return {"status": "success", "entry_id": id}

    return mcp


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="streamable-http")
    args = parser.parse_args()

    server = create_server()
    server.run(transport=args.transport)
