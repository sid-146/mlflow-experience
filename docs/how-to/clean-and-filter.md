# How to Clean Values and Filter Rows

Raw datasets are rarely clean. They often contain inconsistent casing, legacy abbreviations, spelling errors, or invalid rows (e.g., negative ages or test accounts).

This guide shows how to clean values and filter rows directly in your YAML configuration.

---

## The Scenario

Suppose your raw dataset has:
1. Inconsistent labels in `gender`: `"M"`, `"F"`, `"Male"`, `"Female"`.
2. Typos in `status`: `"actv"` instead of `"active"`.
3. Erroneous records: Rows where `age <= 0` or `income < 0`.

---

## Step 1: Replace Inconsistent Values (`cleaning`)

The `cleaning` step applies a dictionary replacement to specific columns using Pandas `replace()`.

Add a `cleaning` step under `preprocessing`:

```yaml
preprocessing:
  - name: standardize_text_values
    type: cleaning
    params:
      replacements:
        gender:
          "M": "Male"
          "F": "Female"
        status:
          "actv": "active"
          "inactv": "inactive"
        country:
          "USA": "United States"
          "US": "United States"
          "UK": "United Kingdom"
```

Any value not in the dictionary remains unchanged.

---

## Step 2: Remove Invalid Rows (`filter`)

The `filter` step applies a Pandas query expression to remove invalid rows from your dataset.

Add a `filter` step under `preprocessing`:

```yaml
preprocessing:
  - name: remove_invalid_rows
    type: filter
    params:
      condition: "age > 0 and income >= 0 and status != 'TEST'"
```

### Supported Query Syntax

The `condition` string accepts standard Pandas query syntax:
- Comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical operators: `and`, `or`, `not`
- Membership: `country in ['United States', 'Canada', 'Mexico']`
- String matching: `status != 'DELETED'`

!!! tip "Pipeline Order Recommendation"
    Always place `filter` and `cleaning` steps at the very **top** of your `preprocessing` pipeline. This ensures missing value imputers, encoders, and scalers only compute statistics on clean, valid data.

---

## Complete Preprocessing Example

Here is how cleaning and filtering fit into a complete preprocessing workflow:

```yaml
preprocessing:
  # 1. Clean inconsistent strings
  - name: standardize_categories
    type: cleaning
    params:
      replacements:
        gender:
          "M": "Male"
          "F": "Female"

  # 2. Filter bad records
  - name: remove_bad_rows
    type: filter
    params:
      condition: "age >= 18 and income > 0"

  # 3. Impute missing values
  - name: impute_missing
    type: missing
    params:
      columns:
        - name: income
          strategy: median

  # 4. Scale numeric values
  - name: scale_numbers
    type: scaling
    params:
      columns:
        - name: income
          strategy: robust

  # 5. Encode categories
  - name: encode_categories
    type: encoding
    params:
      columns:
        - name: gender
          strategy: one_hot
```

---

## Step 3: Run the Pipeline

```bash
uv run python -m main --config configs/my_experiment.yaml --logging-level INFO
```

The pipeline will clean dirty values, drop invalid records, and train your model on sanitized data.
