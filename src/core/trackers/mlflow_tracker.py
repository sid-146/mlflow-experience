import mlflow


class MLflowTracker:
    def __init__(self, config: dict):
        self.experiment_name = config.get("experiment_name", "default")

    # Todo: handle existing experiment
    def start_run(self):
        mlflow.set_experiment(self.experiment_name)
        mlflow.start_run()

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict):
        mlflow.log_metrics(metrics)

    def log_model(self, model):
        mlflow.sklearn.log_model(model, "model")

    def end_run(self):
        mlflow.end_run()
