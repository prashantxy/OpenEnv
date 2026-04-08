from client import IncidentEnvClient
from server.models import IncidentAction

env = IncidentEnvClient(base_url="http://localhost:8000")

with env as client:
    result = client.reset()
    total_score = 0

    for _ in range(50):
        action = IncidentAction(action_type="scale")
        result = client.step(action)

        total_score += result.info.get("score", 0)

        if result.done:
            break

    print("Baseline Score:", total_score)