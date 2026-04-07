from pydantic import BaseModel
from typing import List, Dict

# ---- ACTION ----
class IncidentAction(BaseModel):
    fix: str  # "scale", "restart", "ignore"


# ---- OBSERVATION ----
class IncidentObservation(BaseModel):
    cpu: float
    latency: float
    errors: float

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