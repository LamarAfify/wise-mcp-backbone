
from typing import List, Dict, Any
from ..schemas import TaskHistory
from ..storage import get_user_performance

def recommend_task_assignee(db_path: str, project_id: str, task_type: str, candidate_user_ids: List[str]) -> str:
    """
    Analyzes user history to recommend the best assignee for a task type.
    Simple logic: Returns the user with the highest average success rating * (1 / average duration) for this task type.
    """
    best_score = -1
    best_user = None

    for user_id in candidate_user_ids:
        history = get_user_performance(db_path, user_id)
        relevant_tasks = [h for h in history if h['task_type'] == task_type]
        
        if not relevant_tasks:
            # Default score for users with no history in this task
            score = 0
        else:
            avg_rating = sum(h['success_rating'] for h in relevant_tasks) / len(relevant_tasks)
            avg_duration = sum(h['duration_minutes'] for h in relevant_tasks) / len(relevant_tasks)
            if avg_duration == 0: avg_duration = 1 # Avoid div by zero
            
            # Score formula: Rating (higher is better) / Duration (lower is better)
            # Normalizing duration might be needed, but for now simple ratio
            score = avg_rating / avg_duration

        if score > best_score:
            best_score = score
            best_user = user_id
            
    return best_user if best_user else candidate_user_ids[0] # Default to first if all zero
