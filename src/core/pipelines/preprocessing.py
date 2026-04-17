from src.core.context.contexts import RunContext
from src.core.logging.logger import console


class PreprocessingPipeline:
    def __init__(self, context: RunContext):
        self.context = context
        self.steps = []

    def build(self, X):
        for step in self.context.preprocessing:
            transformer = step.type.transformer_class
            if transformer is None:
                console.warning(
                    f"{step.type} is not mapped in Preprocess registry, skipping..."
                )
            else:
                self.steps.append((step.name, transformer))

        print(self.steps)
