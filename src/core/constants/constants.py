from typing import Literal

FILE_TYPES = Literal[
    "csv",
    "parquet",
    "excel",
    "xlsx",
]


NUMERIC_MISSING_STRATEGY = Literal[
    "mean",
    "median",
    "mode",
    "most_frequent",
    "drop",
]

CATEGORICAL_MISSING_STRATEGY = Literal[
    "constant",
    "drop",
]

NUMERIC_OPERATORS: Literal[">", ">=", "<", "<=", "=="]
