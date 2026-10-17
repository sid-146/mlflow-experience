# How to Encode Categorical Features

Machine learning models require numerical input. This guide shows how to transform text and category columns into numerical features using one-hot and ordinal encoding.

---

## The Scenario

You have columns with string or categorical values, such as:
- **Nominal categories** (no natural order): `department` (`"Sales"`, `"Engineering"`, `"HR"`), `city` (`"NYC"`, `"London"`, `"Tokyo"`).
- **Ordinal categories** (meaningful ranking): `education` (`"High School"`, `"Bachelor"`, `"Master"`, `"PhD"`), `risk_level` (`"Low"`, `"Medium"`, `"High"`).

---

## Supported Encoding Strategies

| Strategy | Transformer | When to Use |
| :--- | :--- | :--- |
| `one_hot` | Scikit-Learn `OneHotEncoder` | Categories without ordering. Automatically ignores unseen categories at inference (`handle_unknown="ignore"`). |
| `ordinal` | Scikit-Learn `OrdinalEncoder` | Categories with a specific hierarchical or natural order. |

---

## Step 1: Configure Encoding in YAML

Add an `encoding` step under the `preprocessing` section in your YAML configuration:

```yaml
preprocessing:
  - name: encode_categorical_features
    type: encoding
    params:
      columns:
        # 1. One-Hot Encoding for nominal columns
        - name: department
          strategy: one_hot

        - name: country
          strategy: one_hot

        # 2. Ordinal Encoding for ranked columns
        - name: customer_tier
          strategy: ordinal
          order: ["Bronze", "Silver", "Gold", "Platinum"]

        - name: experience_level
          strategy: ordinal
          order: ["Junior", "Mid", "Senior", "Lead"]
```

---

## How It Works Under the Hood

1. **One-Hot Encoding**:
   - Converts each unique category into a binary column (`0` or `1`).
   - If a new unseen category appears during testing or inference, it is assigned all zeros (`handle_unknown="ignore"`), preventing pipeline crashes.
2. **Ordinal Encoding**:
   - Maps each label to an integer based on the explicit order you define:
     - `"Bronze"` &rarr; `0.0`
     - `"Silver"` &rarr; `1.0`
     - `"Gold"` &rarr; `2.0`
     - `"Platinum"` &rarr; `3.0`
3. **Remainder Passthrough**:
   - Any column not listed in the `columns` block is untouched and passed directly to subsequent pipeline steps (`remainder="passthrough"`).

---

## Pipeline Execution Order Best Practice

Always place missing value imputation **before** categorical encoding if your categories contain missing (`NaN`) values:

```yaml
preprocessing:
  # 1. First impute missing values with the most frequent category
  - name: impute_categories
    type: missing
    params:
      columns:
        - name: department
          strategy: mode

  # 2. Then encode clean categories into numbers
  - name: encode_categories
    type: encoding
    params:
      columns:
        - name: department
          strategy: one_hot
```

---

## Step 2: Run Your Pipeline

```bash
uv run python -m main --config configs/my_experiment.yaml --logging-level INFO
```

The preprocessed DataFrame will automatically retain Pandas column labels so you can inspect feature transformations clearly in the logs.
