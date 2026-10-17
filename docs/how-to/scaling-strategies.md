# How to Scale Numerical Features

Numerical features often have vastly different ranges. For example, `age` may range from 18 to 90, while `annual_income` ranges from \$20,000 to \$500,000. Without scaling, models like Logistic Regression or SVM will assign disproportionate weight to large-magnitude columns.

This guide shows how to configure feature scalers in `mlflow-experience`.

---

## Supported Scaling Strategies

| Strategy | Scikit-Learn Class | Best Used For | Outlier Sensitivity |
| :--- | :--- | :--- | :--- |
| `standard` | `StandardScaler` | Features with a roughly normal (bell-curve) distribution. Centers at mean = 0 and std = 1. | **Sensitive** to extreme outliers. |
| `minmax` | `MinMaxScaler` | Bounded data or when you need features strictly within the `[0, 1]` range. | **Highly Sensitive** to outliers (compresses valid range). |
| `robust` | `RobustScaler` | Datasets with frequent outliers (e.g., salaries, transaction amounts). Centers using median and interquartile range (IQR). | **Resistant** to outliers. |

---

## Step 1: Configure Scaling in YAML

Define a `scaling` step in your `preprocessing` list:

```yaml
preprocessing:
  - name: scale_features
    type: scaling
    params:
      columns:
        # Standard scaling for normally distributed features
        - name: age
          strategy: standard

        # Robust scaling for features with heavy tails or outliers
        - name: annual_income
          strategy: robust

        - name: total_spend
          strategy: robust

        # Min-Max scaling for scores with known boundaries
        - name: satisfaction_score
          strategy: minmax

        - name: credit_rating_percent
          strategy: minmax
```

---

## How It Works

1. **Grouped Execution**:
   - `mlflow-experience` groups all columns by their chosen strategy and applies them using Scikit-Learn's `ColumnTransformer`.
2. **Remainder Passthrough**:
   - Any column not explicitly listed (e.g., one-hot encoded flags or IDs) is preserved untouched via `remainder="passthrough"`.
3. **No Data Leakage**:
   - The scaler computes statistics (`mean`, `std`, `median`, `min`, `max`) **only on the training split**. During test evaluation or inference, it applies those learned parameters without recalculating on test data.

---

## End-to-End Pipeline Order

For clean feature transformations, follow this logical sequence:

```yaml
preprocessing:
  # 1. Impute missing numbers
  - name: handle_missing
    type: missing
    params:
      columns:
        - name: age
          strategy: median
        - name: annual_income
          strategy: median

  # 2. Scale numeric columns
  - name: scale_features
    type: scaling
    params:
      columns:
        - name: age
          strategy: standard
        - name: annual_income
          strategy: robust

  # 3. Encode categorical features
  - name: encode_categories
    type: encoding
    params:
      columns:
        - name: education_level
          strategy: one_hot
```

---

## Step 2: Run the Pipeline

```bash
uv run python -m main --config configs/my_experiment.yaml --logging-level INFO
```

The model will train on appropriately scaled features, boosting convergence speed and prediction quality.
