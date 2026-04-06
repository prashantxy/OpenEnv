from openenv_core.web import create_web_interface_app
from .environment import IncidentEnvironment
from .models import IncidentAction, IncidentObservation

env = IncidentEnvironment()

app = create_web_interface_app(
    env,
    IncidentAction,
    IncidentObservation
)