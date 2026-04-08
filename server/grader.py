def grade_easy(state):
    return max(0.0, min(1.0, (70 - state["cpu"]) / 70))


def grade_medium(state):
    score = 0.0
    if state["error_rate"] < 5:
        score += 0.5
    if state["latency"] < 400:
        score += 0.5
    return score


def grade_hard(state):
    if (
        state["cpu"] < 60
        and state["error_rate"] < 5
        and state["latency"] < 300
    ):
        return 1.0
    return 0.0


def get_score(task, state):
    if task == "easy":
        return grade_easy(state)
    elif task == "medium":
        return grade_medium(state)
    elif task == "hard":
        return grade_hard(state)
    return 0.0