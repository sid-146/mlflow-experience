from src.core.context.contexts import ModelContext
from src.core.logging.logger import console


class ModelBuilder:
    def __init__(self, context: ModelContext):
        self.context = context

    def build(self):
        model_class = self.context.type.model_class

        if model_class is None:
            console.error(f"Given mode : {self.context.type} is not configured yet.")
            raise ValueError(f"Given mode : {self.context.type} is not configured yet.")

        if self.context.hyperparameters:
            hp = self.context.hyperparameters
            model_instance = model_class(**hp)
        else:
            console.info("No hyper parameters given in config.")
            console.warning("Initiating without hyper parameters")
            model_instance = model_class()

        return [(self.context.task, model_instance)]
