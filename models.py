from pydantic import BaseModel
from typing import List, Dict

# Action
class IncidentAction(BaseModel):
    action_type: str  # restart_db, scale_api, etc.

# Observation (returned after step/reset)
class IncidentObservation(BaseModel):
    cpu: float
    latency: float
    error_rate: float
    services: Dict[str, str]
    logs: List[str]
    reward: float = 0.0
    done: bool = False

# State (full internal state)
class IncidentState(BaseModel):
    step_count: int
    total_reward: float
    episode_id: str