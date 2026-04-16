from typing import Callable, Dict

from src.core.models.linear import build_model as build_linear_model

import pandas as pd

MODEL_REGISTRY: Dict[str, Callable] = {
    "linear": build_linear_model,
}


DATA_READER_FUNCTIONS: Dict[str, Callable[[str], pd.DataFrame]] = {
    "csv": pd.read_csv,
    "excel": pd.read_excel,
    "json": pd.read_json,
}
