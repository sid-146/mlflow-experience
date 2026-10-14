# Model Building & Estimator Factory

The `ModelBuilder` (`src.core.pipelines.model_builder`) serves as the factory responsible for instantiating the terminal estimator in the Scikit-Learn pipeline.

---

## 1. The `ModelType` Registry

Model families are registered in the `ModelType` enum (`src.core.constants.registry`):

```python
class ModelType(str, Enum):
    logistic_regression = "logistic_regression"
    random_forest = "random_forest"
    xgboost = "xgboost"

    @property
    def model_class(self):
        mapping = {
            ModelType.logistic_regression: LogisticRegression,
            ModelType.random_forest: None,  # Placeholder for future implementation
            ModelType.xgboost: XGBClassifier,
        }
        return mapping.get(self)
```

---

## 2. Dynamic Instantiation

The `ModelBuilder.build()` method looks up the class corresponding to `context.type`:

```python
class ModelBuilder:
    def __init__(self, context: ModelContext):
        self.context = context

    def build(self):
        model_class = self.context.type.model_class
        if model_class is None:
            raise ValueError(f"Given model: {self.context.type} is not configured yet.")

        if self.context.hyperparameters:
            model_instance = model_class(**self.context.hyperparameters)
        else:
            model_instance = model_class()

        return [(self.context.task, model_instance)]
```

The resulting tuple `[(task_name, model_instance)]` is appended as the final step in the pipeline.
