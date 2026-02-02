import yaml
import pandas as pd


from src.core.registry import DATA_READER_REGISTRY


def config_loader(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def load_data(file_path: str, extn: str) -> pd.DataFrame:
    func = DATA_READER_REGISTRY.get(extn)
    if not func:
        raise ValueError(f"Unsupported file extension: {extn}")
    df = func(file_path)
    return df
