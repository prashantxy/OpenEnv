import random
import os
from collections import defaultdict
from client import IncidentEnvClient

env = IncidentEnvClient()

ACTIONS = ["scale", "restart", "ignore"]

Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

alpha = 0.1
gamma = 0.9
epsilon = 0.2
episodes = 50


def get_state_key(obs):
    return (
        obs.cpu // 10,
        obs.latency // 50,
        obs.error_rate
    )


# ✅ SAVE FUNCTION (OUTSIDE LOOPS)
def save_to_python_file(Q, episodes, avg_reward):
    os.makedirs("data", exist_ok=True)  # ensure folder exists

    with open("data/learned_data.py", "w") as f:
        f.write("# Auto-generated learning data\n\n")

        f.write(f"Q_TABLE = {dict(Q)}\n\n")

        f.write("TRAINING_STATS = {\n")
        f.write(f"    'episodes': {episodes},\n")
        f.write(f"    'avg_reward': {avg_reward}\n")
        f.write("}\n")


# ---- TRAINING ----
for task in ["easy", "medium", "hard"]:
    print(f"\n=== Training on {task} ===")

    total_reward_all = 0

    for ep in range(episodes):

        result = env.reset(task=task)
        state = result.observation
        state_key = get_state_key(state)

        total_reward = 0

        for step in range(50):

            if random.random() < epsilon:
                action = random.choice(ACTIONS)
            else:
                action = max(Q[state_key], key=Q[state_key].get)

            result = env.step({"fix": action})

            next_state = result.observation
            reward = result.reward
            done = result.done

            next_key = get_state_key(next_state)

            if next_key not in Q:
                Q[next_key] = {a: 0.0 for a in ACTIONS}

            best_next = max(Q[next_key].values())

            Q[state_key][action] += alpha * (
                reward + gamma * best_next - Q[state_key][action]
            )

            state_key = next_key
            total_reward += reward

            if done:
                break

        total_reward_all += total_reward

        print(
            f"Episode {ep+1}: Reward = {total_reward}, Score = {result.info.get('score', 0)}"
        )

    # ✅ SAVE AFTER EACH TASK
    avg_reward = total_reward_all / episodes
    save_to_python_file(Q, episodes, avg_reward)

print("\n✅ Training complete. Data saved to data/learned_data.py")