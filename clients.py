from openenv.core.client import EnvClient
from server.models import IncidentAction, IncidentObservation, IncidentState


class IncidentEnvClient(
    EnvClient[IncidentAction, IncidentObservation, IncidentState]
):
    action_type = IncidentAction
    observation_type = IncidentObservation
    state_type = IncidentState