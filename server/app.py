from fastapi import FastAPI
import gradio as gr

from .environment import IncidentEnvironment

env = IncidentEnvironment()
app = FastAPI()


# -------- HELPER: SERIALIZE --------
def serialize(result):
    return {
        "observation": result["observation"].model_dump(),
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"]
    }


# -------- API ROUTES --------
@app.post("/reset")
def reset(task: str = "easy"):
    result = env.reset(task=task)
    return serialize(result)


@app.post("/step")
def step(action: dict):
    result = env.step(action)
    return serialize(result)


@app.get("/state")
def get_state():
    return env.state


# -------- GRADIO UI --------
def ui_reset():
    result = env.reset()
    return result["observation"].model_dump()


def ui_step(action):
    action_map = {0: "scale", 1: "restart", 2: "ignore"}

    action_int = int(action)

    if action_int not in action_map:
        action_int = 2

    result = env.step({"fix": action_map[action_int]})

    return (
        result["observation"].model_dump(),
        result["reward"],
        result["done"]
    )


with gr.Blocks() as demo:
    gr.Markdown("# 🚀 RL Incident Control")

    state_output = gr.JSON(label="State")
    reward_output = gr.Number(label="Reward")
    done_output = gr.Checkbox(label="Done")

    action_input = gr.Number(label="Action (0=scale,1=restart,2=ignore)", value=0)

    gr.Button("Reset").click(fn=ui_reset, outputs=state_output)

    gr.Button("Step").click(
        fn=ui_step,
        inputs=action_input,
        outputs=[state_output, reward_output, done_output]
    )


# mount UI
app = gr.mount_gradio_app(app, demo, path="/ui")