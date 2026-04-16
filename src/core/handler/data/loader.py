from pathlib import Path
from typing import Dict, Callable

import pandas as pd
import os


from src.core.context.contexts import RunContext
from src.core.logging.logger import console


class DataLoader:
    def __init__(self, context: RunContext):
        self.context = context
        self.data: pd.DataFrame = pd.DataFrame()
        self.X = None
        self.y = None
        self.X_test = None
        self.y_Test = None

        self.DATA_READER_FUNCTIONS: Dict[str, Callable[[str], pd.DataFrame]] = {
            "csv": pd.read_csv,
            "excel": pd.read_excel,
            "json": pd.read_json,
            "classmethod": self.method,
        }

    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path

        cwd_path = Path(os.getcwd()) / path
        if cwd_path.exists():
            return str(cwd_path)

        repo_root = Path(__file__).resolve().parents[4]
        repo_path = repo_root / path
        if repo_path.exists():
            return str(repo_path)

        return str(path)

    def load_data(self):
        if self.context.dataset.train:
            self._load_train_data()
        else:
            raise ValueError("Train dataset configuration")

        if self.context.dataset.test:
            self._load_test_data()
        else:
            console.info(
                "Test dataset configuration not provided. Skipping test dataset loading."
            )

        console.info("Data Loading complete.")

    # Todo: Figure out how to load and store test dataset, new method or in this function only.
    def _load_train_data(self):
        path = self._resolve_path(self.context.dataset.train.path)
        extn = self.context.dataset.train.type

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found on given path: {path}")

        func = self.DATA_READER_FUNCTIONS.get(extn, False)
        if not func:
            raise ValueError(
                f"Unsupported file extension: {extn} \nSupported : {list(self.DATA_READER_FUNCTIONS.keys())}"
            )
        self.data = func(path)
        if self.data.empty:
            raise pd.errors.EmptyDataError("File is empty")

        self.X = self.data.drop(self.context.dataset.train.target_column, axis=1)
        self.y = self.data[self.context.dataset.train.target_column]

        console.debug(f"Training dataset shape : {self.X.shape}")
        console.debug(f"Target variable shape : {self.y.shape}")

    def _load_test_data(self):
        path = self._resolve_path(self.context.dataset.test.path)
        extn = self.context.dataset.test.type

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found on given path: {path}")

        func = self.DATA_READER_FUNCTIONS.get(extn, False)
        if not func:
            raise ValueError(
                f"Unsupported file extension: {extn} \nSupported : {list(self.DATA_READER_FUNCTIONS.keys())}"
            )
        self.data = func(path)
        if self.data.empty:
            raise pd.errors.EmptyDataError("File is empty")

        self.X_test = self.data.drop(self.context.dataset.test.target_column, axis=1)
        self.y_test = self.data[self.context.dataset.test.target_column]

        console.debug(f"Test dataset shape : {self.X_test.shape}")
        console.debug(f"Test target variable shape : {self.y_test.shape}")

    def method(self):
        raise NotImplementedError(
            "This is placeholder for showing example how to add custom functions to handle."
        )
