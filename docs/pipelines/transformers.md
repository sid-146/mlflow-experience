# Custom Transformers

All transformers in `mlflow-experience` (`src.core.pipelines.transformers`) adhere to Scikit-Learn's `BaseEstimator` and `TransformerMixin` contracts.

---

## 1. Global DataFrame Output Configuration

By default, Scikit-Learn converts Pandas DataFrames into NumPy ndarrays upon transformation. `mlflow-experience` configures Scikit-Learn to output DataFrames globally:

```python
from sklearn import set_config

set_config(transform_output="pandas")
```

This guarantees that downstream transformers and debugging steps retain original column names and pandas metadata.

---

## 2. Transformer Implementations

### `RenameColumnsTransformer`
Applies a dictionary column mapping:
```python
class RenameColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mapping=None):
        self.mapping = mapping

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.rename(columns=self.mapping) if self.mapping else X
```

---

### `MissingValueTransformer`
Computes column-specific statistics during `fit()` and applies them during `transform()`:
- `mean`: Column mean computed on training data.
- `median`: Column median computed on training data.
- `mode`: Most frequent value computed on training data.
- `constant`: Injects user-specified `fill_value`.

---

### `CleaningTransformer`
Replaces arbitrary string patterns or invalid values across specified columns using dictionary replacements.

---

### `FilterTransformer`
Executes row-level filtering based on logical expressions (`X.query(condition)`).

---

### `ScalingTransformer`
Dynamically groups columns by strategy (`standard`, `minmax`, `robust`) and wraps them in a Scikit-Learn `ColumnTransformer(remainder="passthrough")`:
```python
self._strategy_map = {
    "standard": StandardScaler(),
    "minmax": MinMaxScaler(),
    "robust": RobustScaler(),
}
```

---

### `EncodingTransformer`
Groups categorical columns by encoding type (`one_hot`, `ordinal`) and wraps them in a `ColumnTransformer`:
```python
self._strategy_map = {
    "one_hot": OneHotEncoder(handle_unknown="ignore", sparse_output=False),
    "ordinal": OrdinalEncoder(),
}
```
Columns not explicitly listed for encoding are preserved via `remainder="passthrough"`.
