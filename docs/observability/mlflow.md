# MLflow Tracking

`mlflow-experience` integrates with **MLflow** via `MLflowTracker` (`src/core/trackers/mlflow_tracker.py`) to give you complete visibility into every experiment run.

---

## 1. What Gets Tracked Automatically?

For every pipeline run, `MLflowTracker` records:

1. **Parameters**:
   - Model type and hyperparameters.
   - Dataset paths and splitting ratios.
2. **Metrics**:
   - Training and testing scores (Accuracy, F1 Score).
3. **Artifacts**:
   - Full console and file execution logs (`logs/<run_name>.log`).
   - Trained model binaries.
4. **Tags & Metadata**:
   - Project name, owner, execution environment.
   - Git commit hash and active branch.

---

## 2. Viewing Results in the MLflow UI

1. Start your MLflow server (either via Docker or locally).
2. Open [http://localhost:5000](http://localhost:5000) in your browser.
3. You will see:
   - **Experiment List**: Listed on the left (e.g. `customer_churn_experiments`).
   - **Run History**: Table of every execution, including timestamps, durations, and metric scores.
   - **Comparison View**: Select multiple runs and click **Compare** to see side-by-side metric charts and hyperparameter differences.
   - **Artifact Browser**: Click any run and select the **Artifacts** tab to inspect the saved session log file.

---

## 3. Running MLflow Locally (Without Docker)

You don't need Docker to use MLflow! You can run a lightweight local MLflow tracking server directly with `uv`:

```bash
uv run mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --port 5000
```

This creates:
- `mlflow.db`: A local SQLite file that holds all your experiment metadata.
- `./mlruns`: A local directory where artifacts and models are stored.

### Or use Direct File Tracking
You can even configure your YAML to write directly to a local directory without starting any server:

```yaml
mlflow:
  experiment_name: customer_churn_experiments
  tracking_uri: file:./mlruns
```
