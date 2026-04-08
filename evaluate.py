from client import IncidentEnvClient

env = IncidentEnvClient()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    result = env.reset(task=task)

    total_score = 0

    for _ in range(50):
        result = env.step({"fix": "scale"})  # simple baseline
        total_score += result.info.get("score", 0)

        if result.done:
            break

    print(f"{task} → Avg Score: {total_score / 50}")