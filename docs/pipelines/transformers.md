# Custom Transformers Reference

All transformers in `mlflow-experience` live in `src/core/pipelines/transformers.py`. They inherit from Scikit-Learn's `BaseEstimator` and `TransformerMixin` and are designed to work seamlessly within `sklearn.pipeline.Pipeline`.

---

## Retaining DataFrame Format

By default, Scikit-Learn transformers convert DataFrames into NumPy arrays. This strips column names and makes debugging painful.

We enable Pandas output globally:

```python
from sklearn import set_config

set_config(transform_output="pandas")
```

Every transformer takes a Pandas DataFrame as input and outputs a Pandas DataFrame with column names preserved.

---

## 1. `RenameColumnsTransformer`

**Purpose**: Renames columns in the DataFrame based on a dictionary mapping.

### YAML Example
```yaml
- name: rename_columns
  type: rename
  params:
    mapping:
      "Customer ID": customer_id
      "Total Spend": total_spend
```

### Python Logic
- `fit(X, y)`: Does nothing (stateless). Returns `self`.
- `transform(X)`: Calls `X.rename(columns=self.mapping)`.

---

## 2. `MissingValueTransformer`

**Purpose**: Imputes missing (null/NaN) values using column-specific strategies.

### Supported Strategies
- `mean`: Fills missing values with the column mean (numerical).
- `median`: Fills missing values with the column median (numerical).
- `mode`: Fills missing values with the most frequent value (categorical/numerical).
- `constant`: Fills missing values with a specific `fill_value`.

### YAML Example
```yaml
- name: handle_missing
  type: missing
  params:
    columns:
      - name: age
        strategy: mean
      - name: gender
        strategy: mode
      - name: city
        strategy: constant
        fill_value: "Unknown"
```

### State Learning
- `fit(X, y)`: Computes the mean, median, mode, or constant on the **training set only** and stores them in `self.fill_values[col_name]`.
- `transform(X)`: Calls `X.fillna(self.fill_values)`.

---

## 3. `ScalingTransformer`

**Purpose**: Scales numerical columns using different scalers without writing multiple separate steps.

### Supported Strategies
- `standard`: `StandardScaler()` (mean = 0, variance = 1).
- `minmax`: `MinMaxScaler()` (scaled to $[0, 1]$).
- `robust`: `RobustScaler()` (uses median and interquartile range to handle outliers).

### YAML Example
```yaml
- name: scale_features
  type: scaling
  params:
    columns:
      - name: age
        strategy: standard
      - name: total_spend
        strategy: minmax
```

### How It Works Under the Hood
`ScalingTransformer` groups columns by strategy and builds a Scikit-Learn `ColumnTransformer`:
- Columns using `standard` are routed to `StandardScaler()`.
- Columns using `minmax` are routed to `MinMaxScaler()`.
- Any unmentioned columns pass through untouched via `remainder="passthrough"`.

---

## 4. `EncodingTransformer`

**Purpose**: Converts categorical text columns into numbers for machine learning models.

### Supported Strategies
- `ordinal`: Uses `OrdinalEncoder()` with an explicit `order` list.
- `one_hot`: Uses `OneHotEncoder(sparse_output=False, handle_unknown="ignore")`.

### YAML Example
```yaml
- name: encode_features
  type: encoding
  params:
    columns:
      # Ordinal: preserves rank order
      - name: contract_length
        strategy: ordinal
        order: ['Monthly', 'Quarterly', 'Annual']

      # One-Hot: creates binary dummy columns
      - name: subscription_type
        strategy: one_hot
```

### How It Works Under the Hood
Columns are grouped by strategy into a `ColumnTransformer`. One-hot encoding creates new columns (e.g. `subscription_type_Basic`, `subscription_type_Premium`), and unmentioned columns are preserved.

---

## 5. `CleaningTransformer`

**Purpose**: Replaces specific categorical values or fixes inconsistencies.

### YAML Example
```yaml
- name: clean_categories
  type: cleaning
  params:
    replacements:
      contract:
        "month-to-month": "Monthly"
        "12 Month": "Annual"
```

### Python Logic
- `transform(X)`: Loops over the columns and applies `X[col].replace(mapping)`.

---

## 6. `FilterTransformer`

**Purpose**: Filters rows based on a query condition.

### YAML Example
```yaml
- name: filter_valid_rows
  type: filter
  params:
    condition: "tenure >= 0 and total_spend >= 0"
```

### Python Logic
- `transform(X)`: Calls `X.query(self.condition)`.

*(Note: Row drops are best used during initial raw data preparation so the feature matrix $X$ and target vector $y$ stay aligned).*
