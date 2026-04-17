from typing import Optional, Any, Dict, List, Literal
from pydantic import BaseModel, field_validator

from src.core.constants.constants import FILE_TYPES


#####################
# Base Column Config
#####################
class ColumnConfig(BaseModel):
    name: str


#####################
# Rename Policy
#####################
class RenamePolicy(BaseModel):
    mapping: Dict[str, str]

    @field_validator("mapping")
    def validate_mapping(cls, v):
        if not v:
            raise ValueError("Rename mapping cannot be empty")
        return v


#####################
# TypeCast Policy
#####################
class TypeCastConfig(ColumnConfig):
    dtype: str
    format: Optional[str] = None


class TypeCastPolicy(BaseModel):
    columns: List[TypeCastConfig]

    @field_validator("columns")
    def validate_columns(cls, v):
        if not v:
            raise ValueError("TypeCast requires at least one column")
        return v


#########################
# Missing Value Policy
#########################
class MissingValueConfig(ColumnConfig):
    strategy: Literal["mean", "median", "mode", "constant"]
    fill_value: Optional[Any] = None


class MissingValuePolicy(BaseModel):
    columns: List[MissingValueConfig]


#####################
# Encoding Policy
#####################
class EncodingConfig(ColumnConfig):
    strategy: Literal["one_hot", "label", "target"]


class EncodingPolicy(BaseModel):
    columns: List[EncodingConfig]


#####################
# Scaling Policy
#####################
class ScalingConfig(ColumnConfig):
    strategy: Literal["standard", "minmax", "robust"]
    params: Optional[Dict[str, Any]] = None


class ScalingPolicy(BaseModel):
    columns: List[ScalingConfig]


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


#####################
# Dataset Policy
#####################
class DatasetPolicy(BaseModel):
    type: FILE_TYPES
    path: str
    id_column: str
    target_column: str
