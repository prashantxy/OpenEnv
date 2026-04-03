from openenv import EnvClient
from models import IncidentAction, IncidentObservation, IncidentState

class IncidentEnvClient(
    EnvClient[IncidentAction, IncidentObservation, IncidentState]
):
    action_type = IncidentAction
    observation_type = IncidentObservation
    state_type = IncidentState