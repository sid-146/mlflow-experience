# Adding a New Preprocessing Transformer

This tutorial guides you through creating and registering a custom transformer in `mlflow-experience`.

---

## Example: Building an Outlier Clipping Transformer

Suppose we want a transformer that clips numerical outliers based on quantile thresholds.

### Step 1: Define the Policy (`src/core/context/policies.py`)

Create the Pydantic configuration models:

```python
class OutlierConfig(ColumnConfig):
    method: Literal["clip", "zscore"]
    lower_quantile: Optional[float] = 0.01
    upper_quantile: Optional[float] = 0.99

class OutlierPolicy(BaseModel):
    columns: List[OutlierConfig]
```

---

### Step 2: Implement the Transformer (`src/core/pipelines/transformers.py`)

Subclass `BaseEstimator` and `TransformerMixin`:

```python
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, params=None):
        self.params = params
        self.bounds_ = {}

    def fit(self, X, y=None):
        if hasattr(self.params, "columns"):
            for col in self.params.columns:
                lower = X[col.name].quantile(col.lower_quantile)
                upper = X[col.name].quantile(col.upper_quantile)
                self.bounds_[col.name] = (lower, upper)
        return self

    def transform(self, X):
        X = X.copy()
        for col, (lower, upper) in self.bounds_.items():
            if col in X.columns:
                X[col] = X[col].clip(lower=lower, upper=upper)
        return X
```

---

### Step 3: Register in `PreprocessingRegistry` (`src/core/constants/registry.py`)

Add the identifier and associate it with its policy and transformer class:

```python
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

### Step 4: Use in YAML Configuration

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
