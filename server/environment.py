import random

class IncidentEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {
            "cpu": random.randint(30, 60),
            "latency": random.randint(100, 300),
            "errors": random.randint(0, 5)
        }
        return self.state

    def step(self, action):
        # ---- Normalize action ----
        if isinstance(action, int):
            mapping = {0: "scale", 1: "restart", 2: "ignore"}
            action = mapping.get(action, "ignore")

        if isinstance(action, str):
            action = {"fix": action}

        fix = action.get("fix", "ignore")

        # ---- Simulate system dynamics ----
        self.state["cpu"] += random.randint(-5, 15)
        self.state["latency"] += random.randint(-20, 40)
        self.state["errors"] += random.randint(-1, 3)

        # clamp values
        self.state["cpu"] = max(0, min(100, self.state["cpu"]))
        self.state["latency"] = max(50, min(1000, self.state["latency"]))
        self.state["errors"] = max(0, min(50, self.state["errors"]))

        # ---- Apply action effects ----
        if fix == "scale":
            self.state["cpu"] -= 20
            self.state["latency"] -= 50

        elif fix == "restart":
            self.state["errors"] = max(0, self.state["errors"] - 5)
            self.state["latency"] -= 30

        # ---- Reward function ----
        reward = 0

        # penalize bad system
        reward -= self.state["cpu"] * 0.02
        reward -= self.state["latency"] * 0.001
        reward -= self.state["errors"] * 0.5

        # bonus for good actions
        if fix == "scale" and self.state["cpu"] < 70:
            reward += 2

        if fix == "restart" and self.state["errors"] < 5:
            reward += 2

        # ---- Done condition ----
        done = self.state["errors"] > 40 or self.state["cpu"] > 95

        return self.state, reward, done, {}