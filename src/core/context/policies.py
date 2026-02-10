from pydantic import BaseModel


from src.core.constants.constants import FILE_TYPES
from src.core.constants.constants import (
    NUMERIC_MISSING_STRATEGY,
    CATEGORICAL_MISSING_STRATEGY,
)


class NumericMissingPolicy(BaseModel):
    strategy: NUMERIC_MISSING_STRATEGY


class CategoricalMissingPolicy(BaseModel):
    strategy: CATEGORICAL_MISSING_STRATEGY
    fill_value: str


class SourcePolicy(BaseModel):
    type: FILE_TYPES
    path: str
