from pydantic import BaseModel
from typing import List, Dict

# ---- ACTION ----
class IncidentAction(BaseModel):
    fix: str  # "scale", "restart", "ignore"


# models.py
class IncidentObservation(BaseModel):
    cpu: float
    latency: float
    error_rate: float
    services: Dict[str, str]
    logs: List[str]
    reward: float = 0.0
    done: bool = False


# ---- STATE ----
class IncidentState(BaseModel):
    cpu: float
    latency: float
    errors: float

    step_count: int
    total_reward: float
    episode_id: str