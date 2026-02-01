import argparse

import mlflow

from src.core.registry import MODEL_REGISTRY
from src.utils.data_loader import config_loader


def run(*args, **kwargs):
    print(kwargs)
    return
    experiment = mlflow.set_experiment(experiment_name=kwargs["experiment"])

    print("Starting Run...")
    with mlflow.start_run(run_name=kwargs["run"]) as run:
        print("Added experiment:", experiment.experiment_id)
        mlflow.log_param("model_type", kwargs["model"])

    return


if __name__ == "__main__":
    # Todo: move this to yaml config file.

    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, required=True, help="Config File Path")
    # parser.add_argument("--model", type=str, required=True)
    # parser.add_argument("--run", type=str, required=True, help="Run Name")

    args = parser.parse_args()
    config = config_loader(args.config)

    run(**config)
