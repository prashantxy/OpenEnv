import random
from collections import defaultdict
from client import IncidentEnvClient
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
env = IncidentEnvClient(base_url="http://localhost:8000")

for ep in range(episodes):
    result = env.reset()
    state = result.observation
    state_key = get_state_key(state)
    total_reward = 0

    for step in range(50):

        if random.random() < epsilon:
            action = random.choice(ACTIONS)
        else:
            action = max(Q[state_key], key=Q[state_key].get)

        result = env.step({"action_type": action})

        next_state = result.observation
        reward = result.reward
        done = result.done

        next_key = get_state_key(next_state)

        best_next = max(Q[next_key].values())
        Q[state_key][action] += alpha * (
            reward + gamma * best_next - Q[state_key][action]
        )

        state_key = next_key
        total_reward += reward

        if done:
            break

    print(f"Episode {ep+1}: Total Reward = {total_reward}")