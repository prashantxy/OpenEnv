import random
from openenv.core import Environment

class IncidentEnvironment(Environment):

    def __init__(self):
        super().__init__()
        self._state = {}
        self.reset()

    def reset(self, seed=None, episode_id=None, **kwargs):
        super().reset(seed=seed, episode_id=episode_id)

        self._state = {
            "cpu": random.randint(40, 60),
            "latency": random.randint(150, 300),
            "errors": random.randint(0, 3)
        }

        return {
            "observation": self._state,
            "reward": 0,
            "done": False,
            "info": {}
        }

    def step(self, action, timeout_s=None, **kwargs):

        # ---- Normalize action ----
        if isinstance(action, int):
            mapping = {0: "scale", 1: "restart", 2: "ignore"}
            action = mapping.get(action, "ignore")

        if isinstance(action, str):
            action = {"fix": action}

        fix = action.get("fix", "ignore")

        # ---- SYSTEM DEGRADATION ----
        self._state["cpu"] += random.randint(5, 15)
        self._state["latency"] += random.randint(10, 50)
        self._state["errors"] += random.randint(0, 2)

        # ---- ACTION EFFECTS ----
        if fix == "scale":
            self._state["cpu"] -= 30
            self._state["latency"] -= 60

        elif fix == "restart":
            self._state["errors"] -= 8
            self._state["latency"] -= 40

        # clamp values
        self._state["cpu"] = max(0, min(100, self._state["cpu"]))
        self._state["latency"] = max(50, min(1000, self._state["latency"]))
        self._state["errors"] = max(0, min(50, self._state["errors"]))

        # ---- REWARD FUNCTION ----
        reward = 0

        if self._state["cpu"] > 80:
            reward -= 15
        if self._state["latency"] > 500:
            reward -= 15
        if self._state["errors"] > 10:
            reward -= 20

        if self._state["cpu"] < 60 and self._state["errors"] < 5:
            reward += 10

        if fix == "scale" and self._state["cpu"] < 50:
            reward -= 8

        if fix == "restart" and self._state["errors"] < 3:
            reward -= 8

        if fix == "ignore" and (self._state["cpu"] > 80 or self._state["errors"] > 10):
            reward -= 10

        # ---- DONE ----
        done = self._state["cpu"] > 95 or self._state["errors"] > 30

        if done:
            reward -= 50

        return {
            "observation": self._state,
            "reward": reward,
            "done": done,
            "info": {}
        }

    @property
    def state(self):
        return self._state