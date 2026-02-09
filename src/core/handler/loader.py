import pandas as pd
import os


def load_data(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_parquet(path)
        if df.empty:
            raise pd.errors.EmptyDataError("File is empty.")
        return df
    else:
        raise FileNotFoundError("File not found on given path.")
