# Quickstart Guide

This guide walks you through running your first machine learning experiment and viewing the results.

---

## Step 1: Check the Sample Data

The repository includes a ready-to-use customer churn dataset in `data/raw/`:
- `data/raw/churn_train.csv`: Training dataset containing 400,000+ customer records.
- `data/raw/churn_test.csv`: Holdout testing dataset.

Columns in this dataset include:
- `CustomerID`: Customer identifier.
- `Age`, `Gender`, `Tenure`: Demographics.
- `Usage Frequency`, `Support Calls`, `Payment Delay`: Usage statistics.
- `Subscription Type`, `Contract Length`, `Total Spend`: Account features.
- `Churn`: The target column (`1` = churned, `0` = retained).

---

## Step 2: Inspect the Configuration

Take a look at `configs/mvp.yaml`. It defines:
1. **Experiment Name**: `customer_churn_experiments`
2. **Data**: Loads `data/raw/churn_train.csv`, marks `Churn` as target, and splits 20% for testing.
3. **Preprocessing**:
   - Renames columns to lowercase snake_case.
   - Casts `Age`, `Gender`, and `Tenure` types.
   - Imputes missing `Age` with the mean and missing `Gender` with the mode.
   - Encodes `Gender` and `Contract Length` ordinally, and `Subscription Type` via one-hot encoding.
   - Standardizes `Age` and min-max scales `Total Spend`.
4. **Model**: Fits a `LogisticRegression` classifier with `max_iter: 250`.
5. **Evaluation**: Computes `accuracy` and `f1` score.

---

## Step 3: Run the Experiment

Run the pipeline using `main.py`:

=== "Using uv"
    ```bash
    uv run python -m main --config configs/mvp.yaml --logging-level DEBUG
    ```

=== "Using active virtual environment"
    ```bash
    python -m main --config configs/mvp.yaml --logging-level DEBUG
    ```

### CLI Options Explained
- `--config` (*required*): Path to the YAML file.
- `--logging-level` (*optional*, default: `INFO`):
  - Use `DEBUG` if you want to see detailed step-by-step diagnostic logs.
  - Use `INFO` for standard progress logs.
  - Use `WARNING` or `ERROR` for quiet execution.

---

## Step 4: Read the Console Logs

When you run the command, you will see color-coded logs showing progress:

```text
DEBUG: 2026-10-14 23:28:15 : main.py : [run] : 11 : Reading data from config
INFO : 2026-10-14 23:28:15 : orchestrator.py : [build] : 52 : Starting pipeline build for model : customer_churn_experiments
DEBUG: 2026-10-14 23:28:15 : loader.py : [_load_train_data] : 78 : Training dataset shape : (400000, 11)
INFO : 2026-10-14 23:28:15 : orchestrator.py : [build] : 71 : No test dataset provided, proceeding with train-test split.
INFO : 2026-10-14 23:28:16 : orchestrator.py : [build] : 82 : Building preprocessing pipeline...
INFO : 2026-10-14 23:28:16 : orchestrator.py : [build] : 102 : Pipeline instance created. Pipeline ready for training and testing...
INFO : 2026-10-14 23:28:18 : orchestrator.py : [train] : 121 : Training completed, pipeline fitted with training dataset.
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 146 : --- Starting Evaluation (on provided dataset) ---
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 158 : | Accuracy  : 0.8425
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 158 : | F1 Score  : 0.8110
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 160 : --- Evaluation Complete ---
```

---

## Step 5: Check Your Run in MLflow

1. Open [http://localhost:5000](http://localhost:5000) in your browser.
2. Click on the experiment `customer_churn_experiments` in the left sidebar.
3. You will see your run listed with:
   - **Metrics**: Accuracy, F1 score.
   - **Artifacts**: Look inside the `logs/` folder in the MLflow UI to view the exact log file for that execution!

---

## Step 6: Try XGBoost

To train an XGBoost model instead of Logistic Regression, simply pass the XGBoost configuration:

```bash
uv run python -m main --config configs/mvp_xgboost.yaml --logging-level INFO
```

Notice that you didn't have to rewrite a single line of Python code—the pipeline handled the model change automatically through configuration.
