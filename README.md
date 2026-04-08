
#  RL Incident Response Environment (OpenEnv)

## 📌 Overview

This project implements a **real-world reinforcement learning environment** for **incident response in distributed systems**.

Modern production systems (like cloud infrastructure, microservices, and APIs) frequently face issues such as:

* High CPU usage
* Increased latency
* Service errors

This environment simulates how **Site Reliability Engineers (SREs)** and **DevOps engineers** handle such incidents using actions like:

* Scaling infrastructure
* Restarting services
* Ignoring noise

An RL agent learns to **stabilize the system efficiently** under dynamic and uncertain conditions.

---

## 🎯 Motivation

Incident response is a **critical real-world task** performed by engineers daily.

This environment models:

* System degradation over time
* Trade-offs between actions
* Partial observability of system health
* Cost of wrong decisions

The goal is to train an agent that can **maintain system stability while minimizing failures**.

---

## 🧠 Environment Design

### 🔍 Observation Space

The agent observes system metrics:

| Feature      | Description                       |
| ------------ | --------------------------------- |
| `cpu`        | CPU utilization (0–100%)          |
| `latency`    | Request latency (ms)              |
| `error_rate` | Number of system errors           |
| `services`   | Service-level metadata (optional) |
| `logs`       | System logs (simulated)           |

---

### 🎮 Action Space

The agent can take one of the following actions:

| Action    | Description                        |
| --------- | ---------------------------------- |
| `scale`   | Reduce CPU and latency via scaling |
| `restart` | Reduce errors and latency          |
| `ignore`  | Take no action                     |

---

## 🏗️ OpenEnv API Compliance

This environment follows the OpenEnv specification:

* `reset()` → initializes environment
* `step(action)` → returns `(observation, reward, done, info)`
* `state` → returns internal state

All observations, actions, and states are implemented using **Pydantic models**.

---

## 🧪 Tasks & Difficulty Levels

The environment includes **3 tasks with increasing difficulty**:

### 🟢 Easy

* Objective: Keep CPU under control
* Score based on CPU stability

---

### 🟡 Medium

* Objective: Control both latency and errors
* Balanced system management required

---

### 🔴 Hard

* Objective: Maintain full system stability
* Must keep CPU, latency, and errors within limits simultaneously

---

## 📊 Reward Function

The reward function provides **dense feedback**:

### ✅ Positive Rewards

* Maintaining low CPU and low errors
* Stable system behavior

### ❌ Penalties

* High CPU (>80%)
* High latency (>500ms)
* High error count (>10)
* Incorrect actions (e.g., scaling unnecessarily)

### 💀 Terminal Penalty

* System crash conditions (CPU >95% or errors >30)

---

## 📈 Scoring (0.0 → 1.0)

Each task includes a **deterministic grader**:

* Easy → CPU-based score
* Medium → latency + error thresholds
* Hard → full system stability

---

## 🤖 Training

Run Q-learning training:

```bash
python train.py
```

The agent learns policies to maximize reward across all tasks.

---

## 🧪 API Usage

### Reset

```bash
curl -X POST http://127.0.0.1:8000/reset
```

### Step

```bash
curl -X POST http://127.0.0.1:8000/step \
-H "Content-Type: application/json" \
-d '{"fix": "scale"}'
```

### State

```bash
curl http://127.0.0.1:8000/state
```

---

## 🌐 Deployment (Hugging Face Spaces)

This project is deployed as a **Gradio-based Hugging Face Space**.

### Steps:

1. Create a new Space (SDK: Gradio)
2. Upload:

   * `app.py`
   * `server/`
   * `requirements.txt`
   * `Dockerfile`
   * `openenv.yaml`
3. Wait for build & run

---

## 🐳 Docker Support

Build and run locally:

```bash
docker build -t rl-openenv .
docker run -p 7860:7860 rl-openenv
```

---

## ⚙️ Setup Instructions

```bash
pip install -r requirements.txt
uvicorn server.app:app --reload
```

---

## 📦 Project Structure

```
Rl-OPENENV/
│
├── app.py
├── train.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
│
├── server/
│   ├── environment.py
│   ├── models.py
```

---

## 📊 Baseline Performance

| Task   | Avg Reward | Score |
| ------ | ---------- | ----- |
| Easy   | ~150       | ~0.8  |
| Medium | ~90        | ~0.6  |
| Hard   | ~40        | ~0.3  |

*(Values depend on training runs)*

---

## 🔐 Environment Variables

For baseline agents (optional):

```bash
export OPENAI_API_KEY=your_key_here
```

---

## 🚀 Future Improvements

* Multi-service simulation
* Real log parsing
* Multi-agent coordination
* Advanced RL algorithms (DQN, PPO)

---

## 🧑‍💻 Author

**Prashant Dubey**

---

## ⭐ Summary

This project demonstrates:

* Real-world RL application
* OpenEnv compliance
* Scalable system simulation
* Agent-based decision learning

---

🔥 *A step toward intelligent autonomous infrastructure management.*
