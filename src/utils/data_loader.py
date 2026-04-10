import yaml
import pandas as pd


from core.registry import DATA_READER_REGISTRY


def config_loader(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def get_extn(path: str) -> str:
    extn = path.split(".")[-1]
    return extn
