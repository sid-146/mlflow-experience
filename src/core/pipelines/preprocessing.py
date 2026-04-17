from src.core.context.contexts import RunContext
from src.core.pipelines.transformers import (
    RenameColumnsTransformer,
    MissingValueTransformer,
    CleaningTransformer,
    FilterTransformer,
    ColumnTransformer,
)


# Todo: Move this to registry and make it dynamic based on configuration
STEP_REGISTRY = {
    "rename_columns": RenameColumnsTransformer,
    # "type_cast": TypeCastTransformer,
    "missing_values": MissingValueTransformer,
    "cleaning": CleaningTransformer,
    # "outliers": OutlierTransformer,
    "filter": FilterTransformer,
}


class PreprocessingPipeline:
    def __init__(self, context: RunContext):
        self.context = context
        self.steps = []

    def build(self):
        return
