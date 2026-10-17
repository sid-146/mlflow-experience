# YAML Configuration Reference

This guide is the complete reference for every section and option you can put in your experiment YAML file.

---

## Structure Overview

Every configuration file has 7 top-level sections:

```yaml
project:       # Who owns this experiment and what environment is it for?
mlflow:        # Where should MLflow log the run and what should it track?
dataset:       # What data are we training on, and how should it be split?
preprocessing: # What cleaning, imputation, encoding, and scaling steps are needed?
model:         # Which machine learning model should we train?
training:      # What is the training objective?
evaluation:    # Which evaluation metrics should be reported?
```

---

## 1. `project`

Defines basic metadata for organizational tracking.

```yaml
project:
  name: customer_churn_prediction  # Project identifier (string)
  owner: data_science_team          # Team or author name (string)
  environment: production           # "development", "staging", or "production"
  description: Telecom churn model  # Optional human description (string)
```

---

## 2. `mlflow`

Controls where experiment results, metrics, parameters, and models are sent.

```yaml
mlflow:
  experiment_name: customer_churn_experiments  # MLflow experiment name (created if missing)
  tracking_uri: http://localhost:5000         # MLflow server URL (default: http://localhost:5000)
  track_params: true                          # Log hyperparameters and options (default: true)
  track_metrics: true                         # Log evaluation metrics (default: true)
  track_artifacts:                            # Optional list of artifact names to log
    - model
    - preprocessing_objects
  tags:                                       # Custom key-value tags for easy filtering in UI
    stage: production
    team: analytics
```

!!! tip "Running without Docker"
    If you are not running a Docker MLflow server on port 5000, you can set `tracking_uri: sqlite:///mlflow.db` or `tracking_uri: file:./mlruns` to track everything locally!

---

## 3. `dataset`

Specifies where to load the training (and optional test) data and how to handle targets and splitting.

```yaml
dataset:
  dataset_name: telecom_churn_v1 # Dataset name label
  random_state: 42               # Seed for reproducible splitting (integer >= 0)
  train_test_split: 0.2          # Ratio to reserve for testing if no test dataset is given (e.g. 0.2 = 20%)

  # Training dataset source (Required)
  train:
    type: csv                    # "csv", "excel", "xlsx", or "json"
    path: data/raw/churn_train.csv # Path to the file (relative or absolute)
    id_column: CustomerID        # Unique identifier column (ignored during training)
    target_column: Churn         # Target variable column to predict

  # Dedicated test dataset source (Optional)
  test:
    type: csv
    path: data/raw/churn_test.csv
    id_column: CustomerID
    target_column: Churn
```

---

## 4. `preprocessing`

An ordered list of transformation steps. Steps execute in the exact order you write them.

Each step has:
- `name`: A descriptive name for the step (e.g. `handle_missing_age`).
- `type`: The transformer type matching `PreprocessingRegistry`.
- `params`: The options for that transformer.

Here are the supported preprocessing types and their parameters:

### A. `rename` (Rename Columns)
Renames raw column headers (e.g. stripping spaces, standardizing to lowercase snake_case):

```yaml
- name: rename_columns
  type: rename
  params:
    mapping:
      "Customer ID": customer_id
      "Total Spend": total_spend
      "Support Calls": support_calls
```

### B. `type_cast` (Cast Data Types)
Converts column data types:

```yaml
- name: cast_types
  type: type_cast
  params:
    columns:
      - name: age
        dtype: int
      - name: gender
        dtype: str
      - name: tenure
        dtype: int
```

### C. `missing` (Impute Missing Values)
Handles missing values on a per-column basis:

```yaml
- name: handle_missing
  type: missing
  params:
    columns:
      - name: age
        strategy: mean         # Options: mean, median, mode, constant

      - name: support_calls
        strategy: median

      - name: gender
        strategy: mode         # Uses the most frequent value

      - name: city
        strategy: constant     # Injects a custom fill value
        fill_value: "Unknown"
```

### D. `encoding` (Categorical Encoding)
Encodes categorical text columns into numbers:

```yaml
- name: encode_features
  type: encoding
  params:
    columns:
      # Ordinal encoding: Maps values to integers using the exact order specified
      - name: contract_length
        strategy: ordinal
        order: ['Monthly', 'Quarterly', 'Annual']

      - name: gender
        strategy: ordinal
        order: ['Male', 'Female']

      # One-Hot encoding: Creates binary indicator columns for each category
      - name: subscription_type
        strategy: one_hot
```

### E. `scaling` (Numerical Feature Scaling)
Scales numeric features to standard ranges:

```yaml
- name: scale_features
  type: scaling
  params:
    columns:
      # StandardScaler: Zero mean, unit variance
      - name: age
        strategy: standard

      # MinMaxScaler: Scaled to [0, 1] range
      - name: total_spend
        strategy: minmax

      # RobustScaler: Scaled using median and interquartile range (outlier-resilient)
      - name: payment_delay
        strategy: robust
```

### F. `cleaning` (Value Replacement)
Replaces specific values or fixes typos:

```yaml
- name: clean_categories
  type: cleaning
  params:
    replacements:
      contract:
        "month-to-month": "Monthly"
        "12 Month": "Annual"
```

### G. `filter` (Row Filtering)
Filters rows based on a query condition:

```yaml
- name: remove_invalid_tenure
  type: filter
  params:
    condition: "tenure >= 0 and total_spend >= 0"
```

---

## 5. `model`

Defines which model to train and its hyperparameters.

```yaml
model:
  type: logistic_regression          # "logistic_regression" or "xgboost"
  task: 'binary:classification'      # Task identifier name
  hyperparameters:                   # Passed directly to the model constructor
    C: 1.0
    max_iter: 250
    solver: saga
```

For XGBoost:

```yaml
model:
  type: xgboost
  task: 'xgboost:classification'
  hyperparameters:
    n_estimators: 500
    learning_rate: 0.01
    max_depth: 6
    random_state: 42
```

---

## 6. `training` & `evaluation`

Defines training objective flags and the metrics to calculate:

```yaml
training:
  objective: binary:logistic

evaluation:
  metrics:
    - accuracy
    - f1
```
