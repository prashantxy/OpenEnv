import random
from openenv.core import Environment
from server.models import IncidentObservation


class IncidentEnvironment(Environment):

    def __init__(self):
        super().__init__()
        self._state = {}
        self.step_count = 0
        self.task = "easy"  # default task
        self.reset()

    def reset(self, seed=None, episode_id=None, task="easy", **kwargs):
        super().reset(seed=seed, episode_id=episode_id)

        self.task = task
        self.step_count = 0

        self._state = {
            "cpu": random.randint(40, 60),
            "latency": random.randint(150, 300),
            "errors": random.randint(0, 3)
        }

        return {
            "observation": IncidentObservation(
                cpu=self._state["cpu"],
                latency=self._state["latency"],
                error_rate=self._state["errors"],
                services={},
                logs=[]
            ),
            "reward": 0.0,
            "done": False,
            "info": {
                "task": self.task,
                "score": 0.0
            }
        }

    def step(self, action, timeout_s=None, **kwargs):
        self.step_count += 1

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

        # ---- REWARD FUNCTION (learning signal) ----
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

        # ---- DONE CONDITION ----
        done = self._state["cpu"] > 95 or self._state["errors"] > 30

        if done:
            reward -= 50

        # ---- TASK SCORING (0 → 1) ----
        score = self.compute_score()

        return {
            "observation": IncidentObservation(
                cpu=self._state["cpu"],
                latency=self._state["latency"],
                error_rate=self._state["errors"],
                services={},
                logs=[]
            ),
            "reward": reward,
            "done": done,
            "info": {
                "task": self.task,
                "score": score,
                "step_count": self.step_count
            }
        }

    def compute_score(self):
        """Return normalized score (0.0 → 1.0)"""

        if self.task == "easy":
            # keep CPU low
            return max(0.0, min(1.0, (70 - self._state["cpu"]) / 70))

        elif self.task == "medium":
            score = 0.0
            if self._state["errors"] < 5:
                score += 0.5
            if self._state["latency"] < 400:
                score += 0.5
            return score

        elif self.task == "hard":
            if (
                self._state["cpu"] < 60 and
                self._state["errors"] < 5 and
                self._state["latency"] < 300
            ):
                return 1.0
            return 0.0

        return 0.0

    @property
    def state(self):
        return {
            "internal_state": self._state,
            "step_count": self.step_count,
            "task": self.task
        }