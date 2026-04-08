import random
from server.environment import IncidentEnvironment

env = IncidentEnvironment()

for ep in range(3):
    state = env.reset()
    total_reward = 0

    for _ in range(50):
        action = random.choice(["scale", "restart", "ignore"])
        state, reward, done, info = env.step(action)

        total_reward += reward
        if done:
            break

    print(f"Task: {info['task']} | Score: {info['score']} | Reward: {total_reward}")