# YAML Schema Specification

Every experiment in `mlflow-experience` is defined through a structured YAML file. This document details each top-level section and its allowed keys.

---

## Top-Level Schema Overview

```yaml
project:       # Metadata about the project and ownership
mlflow:        # MLflow server tracking settings and tags
dataset:       # Ingestion sources and train/test partition directives
preprocessing: # Ordered list of transformation steps
model:         # Model family, task, and hyperparameters
training:      # Training objective directives
evaluation:    # Evaluation metrics to compute
```

---

## 1. `project` Section

Defines organizational metadata and provenance.

| Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Project identifier (e.g., `customer_churn_prediction`). |
| `owner` | `string` | **Yes** | Responsible team or engineer (e.g., `data_science_team`). |
| `environment` | `string` | **Yes** | Execution stage (e.g., `development`, `staging`, `production`). |
| `description` | `string` | No | Free-text description of the project goal. |

---

## 2. `mlflow` Section

Governs telemetry, tracking URIs, and artifact capture.

| Key | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `experiment_name` | `string` | **Yes** | — | Name of the MLflow experiment. Automatically created if not found. |
| `tracking_uri` | `string` | No | `http://localhost:5000` | Remote or local tracking server URL. |
| `track_params` | `boolean` | No | `true` | Whether to automatically log configuration parameters. |
| `track_metrics` | `boolean` | No | `true` | Whether to automatically log computed evaluation metrics. |
| `track_artifacts`| `list[string]`| No | `[]` | List of artifact categories to log. |
| `tags` | `dict[string, string]` | No | `{}` | Custom key-value pairs assigned to the MLflow run. |

---

## 3. `dataset` Section

Directs data acquisition, file formats, and train/test splitting.

| Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `dataset_name` | `string` | **Yes** | Logical dataset label (e.g., `telecom_churn_v1`). |
| `random_state` | `integer` | **Yes** | Seed for reproducible pseudo-random data splitting. |
| `train_test_split` | `float` | No | Proportion of data reserved for testing if `test` source is omitted (e.g., `0.2`). |
| `train` | `DatasetPolicy` | **Yes** | Training data source definition. |
| `test` | `DatasetPolicy` | No | Optional dedicated holdout evaluation data source. |

### `DatasetPolicy` Attributes
- `type` (`"csv" | "parquet" | "excel" | "xlsx"`): File format.
- `path` (`string`): Absolute or relative file path on disk.
- `id_column` (`string`): Primary key or identifier column.
- `target_column` (`string`): Label or ground-truth prediction target column.

---

## 4. `preprocessing` Section

A list of step definitions executed sequentially. Each item specifies:
- `name` (`string`): Unique step identifier.
- `type` (`string`): Preprocessing operation corresponding to `PreprocessingRegistry`:
  - `rename`: Rename columns.
  - `type_cast`: Enforce specific column dtypes.
  - `missing`: Impute missing values.
  - `encoding`: Categorical feature encoding (one-hot, ordinal).
  - `scaling`: Numerical feature scaling (standard, minmax, robust).
  - `cleaning`: Arbitrary value replacement.
  - `filter`: Row-level logical query filtering.
- `params` (`dict`): Parameter dictionary or policy definition.

---

## 5. `model` Section

Defines the predictive estimator architecture.

| Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `type` | `string` | **Yes** | Estimator family (`logistic_regression`, `xgboost`, `random_forest`). |
| `task` | `string` | **Yes** | Task definition (e.g., `binary:classification`). |
| `hyperparameters` | `dict` | No | Keyword arguments passed directly to the model constructor. |

---

## 6. `training` & `evaluation` Sections

- `training.objective` (`string`): Loss function or training objective (e.g., `binary:logistic`).
- `evaluation.metrics` (`list[string]`): Target metrics to calculate and record (e.g., `["accuracy", "f1"]`).
