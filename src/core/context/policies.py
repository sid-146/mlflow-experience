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


# Follow two classes were supposed to be used for train and test data
# but as train and test dataset follow same structure, we can directly use DatasetPolicy
# for both train and test dataset.
class SourcePolicy(BaseModel):
    type: FILE_TYPES
    path: str


class TargetPolicy(BaseModel):
    type: FILE_TYPES
    path: str
    target_column: str


class DatasetPolicy(BaseModel):
    type: FILE_TYPES
    path: str
    id_column: str
    target_column: str
