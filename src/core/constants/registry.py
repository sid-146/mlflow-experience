from enum import Enum
from typing import Callable, Dict

from src.core.models.linear import build_model as build_linear_model
from src.core.context.policies import (
    RenamePolicy,
    TypeCastPolicy,
    MissingValuePolicy,
    EncodingPolicy,
    ScalingPolicy,
)
from src.core.pipelines.transformers import (
    RenameColumnsTransformer,
    MissingValueTransformer,
    CleaningTransformer,
    FilterTransformer,
    EncodingTransformer,
    ScalingTransformer,
)

import pandas as pd

MODEL_REGISTRY: Dict[str, Callable] = {
    "linear": build_linear_model,
}


DATA_READER_FUNCTIONS: Dict[str, Callable[[str], pd.DataFrame]] = {
    "csv": pd.read_csv,
    "excel": pd.read_excel,
    "json": pd.read_json,
}


class PreprocessingRegistry(str, Enum):
    rename_columns = "rename"
    type_cast = "type_cast"
    missing_values = "missing"
    encoding = "encoding"
    scaling = "scaling"
    cleaning = "cleaning"
    filter = "filter"

    @property
    def policy_class(self):
        mapping = {
            PreprocessingRegistry.rename_columns: RenamePolicy,
            PreprocessingRegistry.type_cast: TypeCastPolicy,
            PreprocessingRegistry.missing_values: MissingValuePolicy,
            PreprocessingRegistry.encoding: EncodingPolicy,
            PreprocessingRegistry.scaling: ScalingPolicy,
            PreprocessingRegistry.cleaning: None,
            PreprocessingRegistry.filter: None,
        }
        return mapping.get(self)

    @property
    def transformer_class(self):
        mapping = {
            PreprocessingRegistry.rename_columns: RenameColumnsTransformer,
            # PreprocessingType.type_cast: None,  # Handled via custom logic or future transformer
            PreprocessingRegistry.missing_values: MissingValueTransformer,
            PreprocessingRegistry.encoding: EncodingTransformer,
            PreprocessingRegistry.scaling: ScalingTransformer,
            PreprocessingRegistry.cleaning: CleaningTransformer,
            PreprocessingRegistry.filter: FilterTransformer,
        }
        return mapping.get(self)
