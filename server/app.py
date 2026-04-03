from fastapi import FastAPI
import gradio as gr

from .environment import IncidentEnvironment

env = IncidentEnvironment()
app = FastAPI()

# -------- API ROUTES --------
@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step(action: int):
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    return {"state": env.state}


# -------- GRADIO UI --------
def ui_reset():
    return env.reset()

def ui_step(action):
    state, reward, done, _ = env.step(int(action))
    return state, reward, done

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 RL OpenEnv Interface")

    state_output = gr.Textbox(label="State")
    reward_output = gr.Number(label="Reward")
    done_output = gr.Checkbox(label="Done")

    action_input = gr.Number(label="Action", value=0)

    reset_btn = gr.Button("Reset")
    step_btn = gr.Button("Step")

    reset_btn.click(fn=ui_reset, outputs=state_output)

    step_btn.click(
        fn=ui_step,
        inputs=action_input,
        outputs=[state_output, reward_output, done_output]
    )


# mount gradio inside FastAPI
app = gr.mount_gradio_app(app, demo, path="/ui")