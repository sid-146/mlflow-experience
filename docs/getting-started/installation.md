# Installation & Setup

This guide will help you set up your machine to run `mlflow-experience`.

---

## 1. Prerequisites

- **Python**: Version `3.11` or `3.12` (Python 3.12 recommended).
- **uv**: We recommend [uv](https://docs.astral.sh/uv/) because it installs dependencies in seconds and manages virtual environments automatically.
- **Git**: To clone the repository.
- **Docker** *(Optional)*: Required only if you want to run the self-hosted MLflow + PostgreSQL + MinIO stack. You can also run MLflow locally without Docker!

---

## 2. Clone the Repository

Open your terminal and clone the repository:

```bash
git clone https://github.com/sid-146/mlflow-experience.git
cd mlflow-experience
```

---

## 3. Install Dependencies

### Option A: Using `uv` (Recommended)

If you have `uv` installed, simply run:

```bash
uv sync
```

This single command will:
1. Create a `.venv` virtual environment if it doesn't already exist.
2. Install all required packages pinned in `uv.lock`.

To install `uv` if you don't have it yet:
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option B: Using Standard `pip`

If you prefer using standard Python `venv` and `pip`:

=== "Windows (PowerShell)"
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

=== "macOS / Linux"
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

---

## 4. Verify Your Environment

Test that the CLI tool runs and displays help:

=== "Using uv"
    ```bash
    uv run python -m main --help
    ```

=== "Using standard venv"
    ```bash
    python -m main --help
    ```

You should see:
```text
usage: main.py [-h] --config CONFIG [--logging-level LOGGING_LEVEL]

options:
  -h, --help            show this help message and exit
  --config CONFIG       Config File Path
  --logging-level LOGGING_LEVEL
                        Debug Level
```

---

## 5. Setting up MLflow

You have two simple choices for MLflow tracking:

### Choice 1: Run MLflow Locally (Zero Docker Needed)

You can run an MLflow server directly in a separate terminal:

```bash
uv run mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --port 5000
```

Open [http://localhost:5000](http://localhost:5000) in your browser. All your experiment runs and metrics will show up here.

### Choice 2: Run via Docker Compose

If you have Docker Desktop installed and want a production-like stack with PostgreSQL and MinIO S3 storage:

```bash
docker compose up -d
```

- MLflow UI: [http://localhost:5000](http://localhost:5000)
- MinIO Storage Console: [http://localhost:9001](http://localhost:9001) (User: `minioadmin`, Pass: `minioadminpass`)
