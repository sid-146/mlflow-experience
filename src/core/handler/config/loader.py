import yaml


def config_loader(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config
