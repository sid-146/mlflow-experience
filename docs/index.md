# mlflow-experience

> **A simple, configuration-driven MLOps pipeline built with Scikit-Learn, Pydantic, and MLflow.**

Welcome to `mlflow-experience`! This project lets you build, train, evaluate, and track machine learning experiments without writing boilerplate code. Instead of editing Python scripts every time you want to try a new feature, a different scaler, or a new model, you define your experiment in a **YAML configuration file**.

---

## Why Use This Project?

1. **No Manual Glue Code**: Define your data source, preprocessing steps, model type, and hyperparameters in YAML.
2. **No Data Leakage**: Transformations (like scalers, encoders, and imputers) learn their parameters only on the training set and apply them safely to the test set.
3. **DataFrames Stay DataFrames**: We use Scikit-Learn's `transform_output="pandas"` so column names are never lost during preprocessing.
4. **Automatic MLflow Tracking**: Your hyperparameters, evaluation metrics, model files, and console logs are automatically saved to MLflow.
5. **Type Safety with Pydantic**: Your YAML configuration is checked before running. If a column name is missing or a strategy typo exists, it fails immediately with a clear error.

---

## Quick Example

Here is how simple an experiment looks in YAML:

```yaml
# configs/mvp.yaml (snippet)
dataset:
  train:
    type: csv
    path: data/raw/churn_train.csv
    target_column: Churn
    id_column: CustomerID

preprocessing:
  - name: handle_missing
    type: missing
    params:
      columns:
        - name: Age
          strategy: mean

  - name: scale_features
    type: scaling
    params:
      columns:
        - name: Age
          strategy: standard

model:
  type: logistic_regression
  task: 'binary:classification'
  hyperparameters:
    max_iter: 250
```

Run this in your terminal:

```bash
uv run python -m main --config configs/mvp.yaml
```

The pipeline loads the data, cleans missing values, scales features, fits a logistic regression model, evaluates accuracy and F1 score, and logs the run to MLflow.

---

## How It Works

```mermaid
graph LR
    Config[YAML Config] --> Validator[Pydantic Validation]
    Validator --> Loader[Data Loader & Splitter]
    Loader --> Preprocessor[Preprocessing Pipeline]
    Preprocessor --> Model[Model Estimator]
    Model --> Evaluator[Evaluation Metrics]
    Evaluator --> MLflow[MLflow Tracking & Artifacts]
```

---

## Documentation Guide

- **[Installation](getting-started/installation.md)**: Set up Python, `uv`, and dependencies in under 2 minutes.
- **[Quickstart Guide](getting-started/quickstart.md)**: Run your first experiment step-by-step.
- **[How-To Guides](how-to/index.md)**: Task-oriented recipes for common scenarios (custom datasets, missing data, scaling, offline tracking).
- **[Project Tour](getting-started/project-tour.md)**: Walk through every file and folder in the repository.
- **[Architecture](architecture/overview.md)**: Understand how the 5 layers and the `Orchestrator` work.
- **[YAML Configuration](configuration/yaml-schema.md)**: Full reference for all configuration options.
- **[Transformers Reference](pipelines/transformers.md)**: See before & after examples for all preprocessing steps.
- **[MLflow Tracking](observability/mlflow.md)**: How to view your experiment results in the MLflow UI.
- **[Troubleshooting & FAQ](developer-guide/troubleshooting.md)**: Quick solutions for common errors.
