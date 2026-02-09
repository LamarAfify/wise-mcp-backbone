
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str
    type: str = Field(..., description="e.g. jira_issue_updated, pr_merged, customer_escalation")
    team: str = Field(..., description="e.g. Payments")
    severity: str = Field(..., description="e.g. P0, P1, P2, P3")
    timestamp: str = Field(..., description="UTC ISO timestamp")
    payload: Dict[str, Any] = Field(default_factory=dict)


class Decision(BaseModel):
    id: str
    title: str
    made_by: List[str] = Field(default_factory=list)
    owners: List[str] = Field(default_factory=list)
    timestamp: str = Field(..., description="UTC ISO timestamp")
    rationale: str = ""
    expected_outcomes: Dict[str, Any] = Field(default_factory=dict)
    actual_outcomes: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class ResourceUpdate(BaseModel):
    id: str
    resource: str = Field(..., description="e.g. SupportQueue, CloudSpend, OncallLoad")
    team: Optional[str] = Field(default=None, description="optional team scope")
    metric: str = Field(..., description="e.g. tickets, dollars, available_hours")
    value: float
    unit: str = Field(..., description="e.g. tickets, CAD, hours")
    timestamp: str = Field(..., description="UTC ISO timestamp")
    notes: str = ""


class Project(BaseModel):
    id: str
    name: str
    deadline: str = Field(..., description="ISO date string")
    status: str = "active"
    created_at: str = Field(..., description="UTC ISO timestamp")


class User(BaseModel):
    id: str
    name: str
    role: str = "member"
    skills: Dict[str, float] = Field(default_factory=dict, description="Skill scores 0-1")


class Milestone(BaseModel):
    id: str
    project_id: str
    title: str
    status: str = "pending"  # pending, in_progress, completed
    assigned_to: Optional[str] = None  # User ID
    due_date: Optional[str] = None
    completed_at: Optional[str] = None


class TaskHistory(BaseModel):
    id: str
    user_id: str
    task_type: str  # e.g., 'data-analytics', 'writing', 'coding'
    duration_minutes: int
    success_rating: int = Field(..., description="1-5 rating")
    timestamp: str


