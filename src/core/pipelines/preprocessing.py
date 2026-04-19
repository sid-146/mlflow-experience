from sklearn.pipeline import Pipeline

from src.core.context.contexts import RunContext
from src.core.logging.logger import console


class PreprocessingPipeline:
    def __init__(self, context: RunContext):
        self.context = context
        self.steps = []

    def _make_data_for_pipeline(self):
        return

    # Todo: Revisit This function.
    def _instantiate_transformer(self, transformer_class, params):
        """
        Instantiate a transformer with the appropriate parameters based on its type.
        """
        # Handle transformers that accept policy objects with specific attributes
        if hasattr(params, "mapping"):  # RenamePolicy
            return transformer_class(mapping=params.mapping)
        elif hasattr(params, "columns"):
            # For policies with columns list (MissingValuePolicy, EncodingPolicy, ScalingPolicy)
            # Pass the entire params object for now - transformers need to be updated to handle this
            return transformer_class(params=params)
        else:
            # Fallback: try to instantiate with params as kwargs if it's dict-like
            try:
                if hasattr(params, "dict"):
                    return transformer_class(**params.dict())
                else:
                    return transformer_class(**params)
            except TypeError:
                # If all else fails, instantiate without parameters
                return transformer_class()

    def build(self):
        for step in self.context.preprocessing:
            transformer_class = step.type.transformer_class
            if transformer_class is None:
                console.warning(
                    f"{step.type} is not mapped in Preprocess registry, skipping..."
                )
            else:
                # Instantiate the transformer with parameters
                transformer_instance = self._instantiate_transformer(
                    transformer_class, step.params
                )
                self.steps.append(
                    (
                        step.name,
                        transformer_instance,
                    )
                )
        return self.steps
