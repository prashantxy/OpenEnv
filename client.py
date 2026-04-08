from openenv.async_client import SyncEnvClient, AsyncEnvClient
from server.models import IncidentAction, IncidentObservation, IncidentState


class IncidentEnvClient(SyncEnvClient):
    action_type = IncidentAction
    observation_type = IncidentObservation
    state_type = IncidentState

    def __init__(self, async_client=None):
        if async_client is None:
            async_client = AsyncEnvClient()
        super().__init__(async_client)