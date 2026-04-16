from sklearn.model_selection import train_test_split
from typing import Tuple

from src.core.context.contexts import RunContext
from src.core.logging.logger import console


class DataSplitter:
    def __init__(self, context: RunContext):
        self.context = context
        self.test_size = context.dataset.train_test_split or 0.2
        self.random_state = 42 or context.dataset.random_state

    def split(self, X, y) -> Tuple:
        if X is None or y is None:
            raise ValueError("X and y cannot be None for train-test split")

        if not self.context.dataset.train_test_split:
            console.warning(
                "train_test_split ratio not provided in config, using default value of 0.2"
            )

        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
        )
