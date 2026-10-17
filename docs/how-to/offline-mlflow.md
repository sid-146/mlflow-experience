# How to Run MLflow Without Docker

By default, `mlflow-experience` is configured to connect to an MLflow server running in Docker at `http://localhost:5000`. However, you can track experiments completely **offline** on your local machine without running Docker.

---

## Option 1: Local SQLite Database (Recommended)

Using a local SQLite database allows you to log parameters, metrics, and models to a single local database file (`mlflow.db`).

### Step 1: Update Your YAML Configuration

Set `tracking_uri` to point to a local SQLite database file:

```yaml
project:
  name: offline_exploration
  owner: data_scientist
  environment: local

mlflow:
  experiment_name: local_experiments
  # SQLite tracking URI (stores data in mlflow.db in your project root)
  tracking_uri: sqlite:///mlflow.db
  track_params: true
  track_metrics: true
  track_artifacts:
    - classification_report
    - confusion_matrix
```

### Step 2: Run Your Experiment

Execute the training pipeline using `uv`:

```bash
uv run python -m main --config configs/my_experiment.yaml --logging-level INFO
```

MLflow will automatically initialize `mlflow.db` and log all run parameters, metrics, and artifacts locally.

### Step 3: Launch the MLflow UI

View your runs, graphs, and metric comparisons by starting the MLflow UI pointed at the SQLite file:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## Option 2: File-Based Tracking (`mlruns` Directory)

If you prefer not to use SQLite, you can write experiment runs directly to local JSON and YAML files inside an `mlruns/` directory:

### Step 1: Configure YAML

```yaml
mlflow:
  experiment_name: file_based_experiments
  tracking_uri: file:./mlruns
  track_params: true
  track_metrics: true
```

### Step 2: Run Your Pipeline

```bash
uv run python -m main --config configs/my_experiment.yaml
```

### Step 3: Launch the MLflow UI

```bash
uv run mlflow ui
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) to inspect your runs.

---

## Comparison: When to Use What

| Mode | Tracking URI | Prerequisites | Best For |
| :--- | :--- | :--- | :--- |
| **Docker Compose** | `http://localhost:5000` | Docker Desktop / Engine running | Multi-user development, persistent PostgreSQL backend, production staging. |
| **Local SQLite** | `sqlite:///mlflow.db` | None (`uv run`) | Single-developer laptop, quick experiments, offline working, no Docker overhead. |
| **Local Files** | `file:./mlruns` | None (`uv run`) | Ephemeral prototyping, git-ignored local run folders. |

---

## Switching Back to Docker

When you are ready to switch back to the shared Docker stack:

1. Start the Docker containers:
   ```bash
   docker compose up -d
   ```
2. Set `tracking_uri: http://localhost:5000` in your YAML config.
3. Run your pipeline!
