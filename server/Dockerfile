# ---- Base Image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install system deps (optional but safe) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy project ----
COPY . .

# ---- Install Python deps ----
RUN pip install --no-cache-dir --upgrade pip

# Install main dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    openenv-core \
    gradio \
    pydantic

# ---- Expose port ----
EXPOSE 8000

# ---- Environment variable for OpenEnv UI ----
ENV ENABLE_WEB_INTERFACE=true

# ---- Run server ----
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]