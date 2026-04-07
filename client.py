from openenv import SyncEnvClient
from server.models import IncidentAction, IncidentObservation, IncidentState


class IncidentEnvClient(SyncEnvClient):
    action_type = IncidentAction
    observation_type = IncidentObservation
    state_type = IncidentState