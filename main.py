import argparse

from src.core.handler.config.loader import config_loader
from src.core import RunContext
from src.core.logging.logger import console

from src.orchestrator import Orchestrator


def run(*args, **kwargs):
    console.debug("Reading data from config")
    context = RunContext.from_yaml_dict(config)
    orchestrator = Orchestrator(context)
    orchestrator.build()
    orchestrator.train()
    return


if __name__ == "__main__":
    # Todo: move this to yaml config file.

    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, required=True, help="Config File Path")
    parser.add_argument(
        "--logging-level", type=str, required=False, help="Debug Level", default="INFO"
    )
    # parser.add_argument("--model", type=str, required=True)
    # parser.add_argument("--run", type=str, required=True, help="Run Name")

    args = parser.parse_args()
    config = config_loader(args.config)
    console.setLevel(args.logging_level)
    run(**config)
