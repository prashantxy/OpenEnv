from client import IncidentEnvClient
from models import IncidentAction

with IncidentEnvClient(base_url="http://localhost:8000").sync() as env:

    result = env.reset()
    obs = result.observation

    while not obs.done:
        if obs.error_rate > 0.2:
            action = "restart_db"
        elif obs.latency > 400:
            action = "scale_api"
        else:
            action = "do_nothing"

        result = env.step(IncidentAction(action_type=action))
        obs = result.observation

    print("Final reward:", obs.reward)

    state = env.state()
    print("Steps:", state.step_count)