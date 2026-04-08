from pydantic import BaseModel
from typing import Dict, List


class IncidentAction(BaseModel):
    fix: str  # scale | restart | ignore


class IncidentObservation(BaseModel):
    cpu: int
    latency: int
    error_rate: int
    services: Dict = {}
    logs: List[str] = []


class IncidentState(BaseModel):
    cpu: int
    latency: int
    error_rate: int