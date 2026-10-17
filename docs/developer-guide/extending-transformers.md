# Adding a New Transformer

This tutorial shows you how to add a new preprocessing transformer to `mlflow-experience` in 4 simple steps.

---

## Example: Building an Outlier Clipping Transformer

Let's say you want to build an `OutlierTransformer` that clips values above or below specific quantiles.

### Step 1: Create the Policy (`src/core/context/policies.py`)

Define the Pydantic models to validate the YAML settings:

```python
# src/core/context/policies.py

class OutlierConfig(ColumnConfig):
    method: Literal["clip", "zscore"] = "clip"
    lower_quantile: Optional[float] = 0.01
    upper_quantile: Optional[float] = 0.99

class OutlierPolicy(BaseModel):
    columns: List[OutlierConfig]
```

---

### Step 2: Implement the Transformer (`src/core/pipelines/transformers.py`)

Create a class that inherits from `BaseEstimator` and `TransformerMixin`:

```python
# src/core/pipelines/transformers.py
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, params=None):
        self.params = params
        self.bounds_ = {}

    def fit(self, X, y=None):
        # Learn upper and lower bounds on training set ONLY
        if hasattr(self.params, "columns"):
            for col in self.params.columns:
                lower = X[col.name].quantile(col.lower_quantile)
                upper = X[col.name].quantile(col.upper_quantile)
                self.bounds_[col.name] = (lower, upper)
        return self

    def transform(self, X):
        X = X.copy()
        for col_name, (lower, upper) in self.bounds_.items():
            if col_name in X.columns:
                X[col_name] = X[col_name].clip(lower=lower, upper=upper)
        return X
```

---

### Step 3: Register in `PreprocessingRegistry` (`src/core/constants/registry.py`)

Add your new type to `PreprocessingRegistry`:

```python
# src/core/constants/registry.py

class PreprocessingRegistry(str, Enum):
    # ... existing entries ...
    outliers = "outliers"

    @property
    def policy_class(self):
        mapping = {
            # ... existing mappings ...
            PreprocessingRegistry.outliers: OutlierPolicy,
        }
        return mapping.get(self)

    @property
    def transformer_class(self):
        mapping = {
            # ... existing mappings ...
            PreprocessingRegistry.outliers: OutlierTransformer,
        }
        return mapping.get(self)
```

---

### Step 4: Use It in Your YAML File

Add the step to `preprocessing` in your config:

```yaml
preprocessing:
  - name: clip_outliers
    type: outliers
    params:
      columns:
        - name: total_spend
          method: clip
          lower_quantile: 0.01
          upper_quantile: 0.99
```

Run the pipeline:

```bash
uv run python -m main --config configs/mvp.yaml
```

Your new transformer will be instantiated, fitted on training data, applied to test data, and included in the pipeline!
