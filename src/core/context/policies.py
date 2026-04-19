from pydantic import BaseModel


from core.constants.constants import FILE_TYPES
from core.constants.constants import (
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


class SchemaPolicy(BaseModel):
    required_columns: Optional[List[str]] = None
    optional_columns: Optional[List[str]] = None
    rename: Optional[Dict[str, str]] = None
    drop: Optional[List[str]] = None


class TypeCastPolicy(BaseModel):
    type: str
    strip_chars: Optional[List[str]] = None
    format: Optional[str] = None


class MissingValuePolicy(BaseModel):
    strategy: str
    value: Optional[Union[str, float, str]] = None
    threshold: Optional[float] = None


class FilterPolicy(BaseModel):
    type: int
    operator: NUMERIC_OPERATORS
    value: Union[float, int]

    @model_validator(mode="after")
    def validate_operator(self):
        if self.type == "str":
            if self.operator != "==":
                raise ValidationError(
                    "Equals to operators is only supported with string type."
                )


class OutliersPolicy(BaseModel):
    method: str
    lower_percentile: Optional[float] = None
    upper_percentile: Optional[float] = None
    threshold: Optional[float] = None

    @model_validator(mode="after")
    def validate(self):
        if self.method == "zscore":
            if not self.threshold:
                raise ValidationError("Threshold can not be none for zscore")
        elif self.method == "clip":
            if not (self.lower_percentile and self.upper_percentile):
                raise ValidationError(
                    "Upper and Lower limit percentile should be present for clip method."
                )
