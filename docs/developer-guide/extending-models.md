# Adding a New Model

Adding a new machine learning algorithm to `mlflow-experience` takes less than 5 minutes.

---

## Example: Adding `RandomForestClassifier`

Suppose you want to support Scikit-Learn's `RandomForestClassifier`.

### Step 1: Update `ModelType` (`src/core/constants/registry.py`)

1. Import the model class at the top of the file:
   ```python
   from sklearn.ensemble import RandomForestClassifier
   ```

2. Add the enum value and map it in `model_class`:
   ```python
   class ModelType(str, Enum):
       logistic_regression = "logistic_regression"
       xgboost = "xgboost"
       random_forest = "random_forest"  # <--- Add this

       @property
       def model_class(self):
           mapping = {
               ModelType.logistic_regression: LogisticRegression,
               ModelType.xgboost: XGBClassifier,
               ModelType.random_forest: RandomForestClassifier,  # <--- Add this
           }
           return mapping.get(self)
   ```

---

### Step 2: Use It in Your YAML Configuration

You can now use `random_forest` in any configuration file. Any parameters you pass under `hyperparameters` will be forwarded directly to the `RandomForestClassifier` constructor:

```yaml
model:
  type: random_forest
  task: 'random_forest:classification'
  hyperparameters:
    n_estimators: 200
    max_depth: 10
    min_samples_split: 5
    random_state: 42
    n_jobs: -1
```

---

### Step 3: Run the Pipeline

```bash
uv run python -m main --config configs/your_config.yaml
```

The `ModelBuilder` will automatically instantiate `RandomForestClassifier` with your hyperparameters and add it as the final step of the pipeline.
