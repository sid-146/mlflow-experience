# How to Handle Missing Data

Missing values (NaNs or nulls) cause most machine learning models to fail. This guide shows you how to clean up missing values using column-specific strategies in YAML.

---

## The Scenario

Your raw data has missing values:
- `age` is missing on some rows (numeric, approximately normal).
- `salary` is missing on some rows (numeric, highly skewed with outliers).
- `gender` is missing on some rows (categorical).
- `referral_source` is missing on some rows (categorical, where missing means "Direct").

---

## Strategy Selection Guide

| Column Type | Data Characteristic | Recommended Strategy | Explanation |
| :--- | :--- | :--- | :--- |
| Numeric | Symmetric / Normal | `mean` | Replaces nulls with the arithmetic average. |
| Numeric | Skewed / Has Outliers | `median` | Replaces nulls with the 50th percentile (not distorted by extreme values). |
| Categorical | Frequent category expected | `mode` | Replaces nulls with the most frequent value in the column. |
| Categorical/Numeric | Specific default meaning | `constant` | Replaces nulls with a custom value (e.g. `"Unknown"`, `"None"`, or `0`). |

---

## YAML Configuration Example

Add a `missing` step to your `preprocessing` list:

```yaml
preprocessing:
  - name: impute_missing_values
    type: missing
    params:
      columns:
        # 1. Use Mean for normally distributed numeric columns
        - name: age
          strategy: mean

        # 2. Use Median for skewed numeric columns
        - name: salary
          strategy: median

        # 3. Use Mode for standard categorical columns
        - name: gender
          strategy: mode

        # 4. Use Constant for columns with a custom fallback
        - name: referral_source
          strategy: constant
          fill_value: "Direct"
```

---

## How It Works During Training and Testing

`MissingValueTransformer` ensures **zero data leakage**:

1. **During Training (`fit`)**:
   - The transformer calculates the mean of `age` (e.g. `34.2`), the median of `salary` (e.g. `$58,000`), and the mode of `gender` (e.g. `"Male"`) using **training data only**.
   - These computed values are stored in memory inside `self.fill_values`.
2. **During Testing & Inference (`transform`)**:
   - When new test data or live inference data arrives, nulls are filled with the **exact values computed during training** (`34.2`, `$58,000`, `"Male"`).
   - It never recalculates statistics on the test set!
