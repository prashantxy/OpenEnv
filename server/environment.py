import random

class IncidentEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {
            "cpu": random.randint(40, 60),
            "latency": random.randint(150, 300),
            "errors": random.randint(0, 3)
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

        # ---- SYSTEM NATURAL DEGRADATION (IMPORTANT) ----
        # system always tends to worsen
        self.state["cpu"] += random.randint(5, 15)
        self.state["latency"] += random.randint(10, 50)
        self.state["errors"] += random.randint(0, 2)

        # ---- APPLY ACTION EFFECTS (STRONG IMPACT) ----
        if fix == "scale":
            self.state["cpu"] -= 30
            self.state["latency"] -= 60

        elif fix == "restart":
            self.state["errors"] -= 8
            self.state["latency"] -= 40

        # clamp values
        self.state["cpu"] = max(0, min(100, self.state["cpu"]))
        self.state["latency"] = max(50, min(1000, self.state["latency"]))
        self.state["errors"] = max(0, min(50, self.state["errors"]))

        # ---- REWARD FUNCTION (STRONG SIGNALS) ----
        reward = 0

        # heavy penalties
        if self.state["cpu"] > 80:
            reward -= 15
        if self.state["latency"] > 500:
            reward -= 15
        if self.state["errors"] > 10:
            reward -= 20

        # reward stability
        if self.state["cpu"] < 60 and self.state["errors"] < 5:
            reward += 10

        # penalize bad decisions
        if fix == "scale" and self.state["cpu"] < 50:
            reward -= 8

        if fix == "restart" and self.state["errors"] < 3:
            reward -= 8

        # slight penalty for doing nothing under stress
        if fix == "ignore" and (self.state["cpu"] > 80 or self.state["errors"] > 10):
            reward -= 10

        # ---- DONE CONDITION ----
        done = self.state["cpu"] > 95 or self.state["errors"] > 30

        if done:
            reward -= 50  # strong failure penalty

        return self.state, reward, done, {}