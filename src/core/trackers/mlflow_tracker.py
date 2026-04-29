from typing import Optional 

import mlflow

from src.core.context.contexts import RunContext
from src.core.logging.logger import console


class MLflowTracker:
    # Todo: Think if it can be implemented better
    # Todo: Get more core control over mlflow client and its functionalities, currently it is just a wrapper around mlflow client.
    # Todo: Add mlflow Trace and other thing
    def __init__(self, context: RunContext):
        self.context = context
        self.experiment_name = context.mlflow.experiment_name or "default"
        self.experiment_id = context.mlflow.experiment_id or "placeholder"
        self.tracking_uri = context.mlflow.tracking_uri or "http://localhost:5000"
        mlflow.set_tracking_uri(self.tracking_uri)

        self.run_id: Optional[str] = None
        console.debug("MLFlow tracker initialized for experiment...")

    def start_run(self):
        console.debug("Creating run...")
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        if experiment is None:
            console.info(
                f"Did not find any existing experiment with name : {self.experiment_name}"
            )
            mlflow.create_experiment(self.experiment_name)
        else:
            console.debug("Found existing experiment.")
        mlflow.set_experiment(self.experiment_name)
        self.run = mlflow.start_run()
        self.run_id = self.run.info.run_id 

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict):
        mlflow.log_metrics(metrics)

    def log_model(self, model):
        mlflow.sklearn.log_model(model, "model")

    def end_run(self):
        mlflow.end_run()

    def log_artifact(self, artifact_path: str, artifact_name: str = None):
        mlflow.log_artifact(artifact_path, artifact_name)


    # ################# Utilities ######################
    def _ensure_active_run(self):
        if self.run_id is None:
            raise RuntimeError("No active run, call start_run() function to create a new run.")
        return True

# import mlflow
# from mlflow.tracking import MlflowClient
# from typing import Optional, Dict, Any


# class MLflowTracker:
#     def __init__(self, context):
#         self.context = context

#         self.tracking_uri = context.mlflow.tracking_uri or "http://localhost:5000"
#         self.experiment_name = context.mlflow.experiment_name or "default"

#         mlflow.set_tracking_uri(self.tracking_uri)
#         self.client = MlflowClient(tracking_uri=self.tracking_uri)

#         self.experiment_id = self._get_or_create_experiment(self.experiment_name)
#         self.run_id: Optional[str] = None

#     # -------------------------
#     # Experiment Handling
#     # -------------------------
#     def _get_or_create_experiment(self, name: str) -> str:
#         experiment = self.client.get_experiment_by_name(name)

#         if experiment:
#             return experiment.experiment_id

#         return self.client.create_experiment(name)

#     # -------------------------
#     # Run Lifecycle
#     # -------------------------
#     def start_run(self, run_name: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
#         if self.run_id is not None:
#             raise RuntimeError("Run already active. End the current run before starting a new one.")

#         tags = tags or {}

#         run = self.client.create_run(
#             experiment_id=self.experiment_id,
#             tags=tags
#         )

#         self.run_id = run.info.run_id

#         if run_name:
#             self.client.set_tag(self.run_id, "mlflow.runName", run_name)

#     def end_run(self, status: str = "FINISHED"):
#         if self.run_id is None:
#             return

#         self.client.set_terminated(self.run_id, status=status)
#         self.run_id = None

#     # -------------------------
#     # Logging
#     # -------------------------
#     def log_param(self, key: str, value: Any):
#         self._ensure_active_run()
#         self.client.log_param(self.run_id, key, value)

#     def log_params(self, params: Dict[str, Any]):
#         for k, v in params.items():
#             self.log_param(k, v)

#     def log_metric(self, key: str, value: float, step: Optional[int] = None):
#         self._ensure_active_run()
#         self.client.log_metric(self.run_id, key, value, step=step)

#     def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
#         for k, v in metrics.items():
#             self.log_metric(k, v, step)

#     def log_artifact(self, local_path: str):
#         self._ensure_active_run()
#         self.client.log_artifact(self.run_id, local_path)

#     def log_model(self, model, artifact_path: str = "model"):
#         """
#         Still uses mlflow flavor API because client doesn't handle model flavors directly.
#         """
#         self._ensure_active_run()

#         with mlflow.start_run(run_id=self.run_id):
#             mlflow.sklearn.log_model(model, artifact_path)

#     # -------------------------
#     # Utilities
#     # -------------------------
#     def set_tag(self, key: str, value: str):
#         self._ensure_active_run()
#         self.client.set_tag(self.run_id, key, value)

#     def _ensure_active_run(self):
#         if self.run_id is None:
#             raise RuntimeError("No active run. Call start_run() first.")
