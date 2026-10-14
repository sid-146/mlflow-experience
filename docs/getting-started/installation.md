# Installation & Setup

This guide walks you through setting up your local environment to run `mlflow-experience`. The project uses **uv** for blazing-fast, deterministic dependency resolution.

---

## Prerequisites

Ensure you have the following installed:

- **uv**: High-performance Python package installer and resolver ([Install uv](https://docs.astral.sh/uv/getting-started/installation/)).
- **Python**: Version `3.12` (managed automatically by uv if needed).
- **Docker & Docker Compose**: To run the MLflow tracking stack (PostgreSQL, MinIO, and MLflow server).
- **Git**: To clone the repository and track code revisions.

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/mlflow-experience.git
cd mlflow-experience
```

---

## 2. Environment Setup with `uv` (Recommended)

`uv` manages the virtual environment, Python version, and locked dependencies automatically:

```bash
# Synchronize environment with uv.lock (creates .venv and installs all dependencies)
uv sync
```

Alternatively, to manually initialize a virtual environment:

=== "Using uv"
    ```bash
    uv venv --python 3.12 .venv
    .\.venv\Scripts\Activate.ps1  # Windows
    # or
    source .venv/bin/activate     # Linux/macOS
    uv sync
    ```

=== "Using Standard pip"
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1  # Windows
    pip install -r requirements.txt
    ```

---

## 3. Running Commands with `uv run`

With `uv`, you don't even need to activate the virtual environment manually. Prefix any command with `uv run`:

```bash
# Run experiment pipeline
uv run python -m main --config configs/mvp.yaml --logging-level DEBUG

# Run MkDocs documentation server
uv run mkdocs serve
```

---

## 4. Spin up the MLflow Tracking Server

The platform includes a containerized MLflow environment running PostgreSQL (backend store) and MinIO (S3-compatible artifact store).

Start the stack with Docker Compose:

```bash
docker compose up -d
```

Verify the services are healthy:

```bash
docker compose ps
```

- **MLflow UI**: Open [http://localhost:5000](http://localhost:5000)
- **MinIO Console**: Open [http://localhost:9001](http://localhost:9001) (User: `minioadmin`, Password: `minioadminpass`)
