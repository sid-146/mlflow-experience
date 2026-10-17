# How to Train on Your Own Dataset

This guide shows you how to plug in your own CSV, Excel, or JSON dataset into `mlflow-experience` without writing any Python code.

---

## The Scenario

You have a new dataset (e.g. `data/raw/housing.csv` or `data/raw/employees.csv`) and want to train a model on it.

---

## Step 1: Place Your Data in `data/raw/`

Copy your raw dataset file into the `data/raw/` directory:

```bash
# Example
cp /path/to/my_data.csv data/raw/my_data.csv
```

---

## Step 2: Create a New YAML Configuration File

Create a new file in `configs/`, for example `configs/my_data.yaml`:

```yaml
project:
  name: my_custom_project
  owner: analytics_team
  environment: development
  description: Predicting target variable for custom dataset

mlflow:
  experiment_name: my_custom_experiments
  tracking_uri: http://localhost:5000
  track_params: true
  track_metrics: true

dataset:
  dataset_name: custom_dataset_v1
  random_state: 42
  train_test_split: 0.2  # 80% train, 20% test

  train:
    type: csv                    # "csv", "excel", or "json"
    path: data/raw/my_data.csv   # Path to your file
    id_column: id                # Primary key / ID column (excluded from training)
    target_column: target        # The column you want to predict

preprocessing:
  # Add your cleaning, imputation, and encoding steps here
  - name: handle_missing
    type: missing
    params:
      columns:
        - name: feature_1
          strategy: mean

model:
  type: logistic_regression
  task: 'binary:classification'
  hyperparameters:
    max_iter: 200

training:
  objective: binary:logistic

evaluation:
  metrics:
    - accuracy
    - f1
```

---

## Step 3: What If You Already Have Separate Train & Test Files?

If you already have pre-split train and test files (e.g. `my_train.csv` and `my_test.csv`), define both under `dataset`:

```yaml
dataset:
  dataset_name: pre_split_data
  random_state: 42

  train:
    type: csv
    path: data/raw/my_train.csv
    id_column: user_id
    target_column: label

  test:
    type: csv
    path: data/raw/my_test.csv
    id_column: user_id
    target_column: label
```

When `dataset.test` is provided, the `DataSplitter` skips random splitting and evaluates directly on your test file.

---

## Step 4: Run the Experiment

```bash
uv run python -m main --config configs/my_data.yaml --logging-level INFO
```

The pipeline will read your data, isolate features from the target column, apply preprocessing, train the model, and print evaluation metrics!
