import random
from collections import defaultdict

from client import IncidentEnv

# connect to running OpenEnv server
env = IncidentEnv(base_url="http://localhost:8000").sync()

ACTIONS = ["scale", "restart", "ignore"]

# Q-table
Q = defaultdict(lambda: {a: 0 for a in ACTIONS})

# hyperparameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

def get_state_key(state):
    return (
        state["cpu"] // 10,
        state["latency"] // 100,
        state["errors"] // 5
    )

episodes = 50

for ep in range(episodes):

    # ---- RESET (OpenEnv style) ----
    result = env.reset()
    state = result["observation"]

    state_key = get_state_key(state)
    total_reward = 0

    for step in range(50):

        # epsilon-greedy
        if random.random() < epsilon:
            action = random.choice(ACTIONS)
        else:
            action = max(Q[state_key], key=Q[state_key].get)

        # ---- STEP (OpenEnv style) ----
        result = env.step(action)

        next_state = result["observation"]
        reward = result["reward"]
        done = result["done"]

        next_key = get_state_key(next_state)

        # Q-learning update
        best_next = max(Q[next_key].values())
        Q[state_key][action] += alpha * (
            reward + gamma * best_next - Q[state_key][action]
        )

        state_key = next_key
        total_reward += reward

        if done:
            break

    print(f"Episode {ep+1}: Total Reward = {total_reward}")