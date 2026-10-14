# Adding a New Model Estimator

This guide walks you through integrating a new machine learning algorithm into the platform.

---

## Example: Adding Scikit-Learn `RandomForestClassifier`

### Step 1: Update `ModelType` (`src/core/constants/registry.py`)

Import the algorithm and register it in `ModelType.model_class`:

```python
from sklearn.ensemble import RandomForestClassifier

class ModelType(str, Enum):
    logistic_regression = "logistic_regression"
    xgboost = "xgboost"
    random_forest = "random_forest"

    @property
    def model_class(self):
        mapping = {
            ModelType.logistic_regression: LogisticRegression,
            ModelType.xgboost: XGBClassifier,
            ModelType.random_forest: RandomForestClassifier,
        }
        return mapping.get(self)
```

---

### Step 2: Use in YAML Configuration

Any valid keyword arguments for the model constructor can be passed under `hyperparameters`:

```yaml
model:
  type: random_forest
  task: 'random_forest:classification'
  hyperparameters:
    n_estimators: 300
    max_depth: 15
    min_samples_split: 5
    random_state: 42
    n_jobs: -1

training:
  objective: binary:classification

evaluation:
  metrics:
    - accuracy
    - f1
```

---

### Step 3: Run the Experiment

Execute `main.py` with your new configuration:

```bash
python -m main --config configs/random_forest.yaml --logging-level INFO
```
