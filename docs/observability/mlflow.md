# MLflow Tracking Integration

`mlflow-experience` provides deep integration with **MLflow** through the `MLflowTracker` class (`src.core.trackers.mlflow_tracker`).

---

## 1. Tracker Initialization

The tracker reads settings from `context.mlflow`:

```python
class MLflowTracker:
    def __init__(self, context: RunContext):
        self.context = context
        self.experiment_name = context.mlflow.experiment_name or "default"
        self.experiment_id = context.mlflow.experiment_id or "placeholder"
        self.tracking_uri = context.mlflow.tracking_uri or "http://localhost:5000"
        mlflow.set_tracking_uri(self.tracking_uri)
```

---

## 2. Automatic Experiment Creation

When `start_run()` is called:
1. The tracker queries MLflow for an experiment matching `experiment_name`.
2. If none exists, it creates the experiment on the tracking server.
3. Sets the experiment as active and initializes `self.run = mlflow.start_run()`.

```python
def start_run(self):
    experiment = mlflow.get_experiment_by_name(self.experiment_name)
    if experiment is None:
        mlflow.create_experiment(self.experiment_name)
    mlflow.set_experiment(self.experiment_name)
    self.run = mlflow.start_run()
```

---

## 3. What Gets Logged

- **Parameters**: Hyperparameters and configuration flags (`mlflow.log_params`).
- **Metrics**: In-sample and out-of-sample evaluation metrics such as Accuracy and F1 Score (`mlflow.log_metrics`).
- **Models**: Exported model pipeline binaries via `mlflow.sklearn.log_model`.
- **Artifacts**: Local execution log files and configuration artifacts (`mlflow.log_artifact`).
