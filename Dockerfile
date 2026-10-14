# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Copy uv binary from the official Astral uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Install dependencies using uv sync (leverages lockfile for deterministic builds)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . /app
RUN uv sync --frozen

# Place the virtual environment at the front of PATH
ENV PATH="/app/.venv/bin:$PATH"

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Entry point for container execution
CMD ["python", "-m", "main", "--config", "configs/mvp.yaml"]
