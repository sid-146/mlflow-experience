# Quickstart Guide

Get up and running with your first machine learning experiment in under two minutes.

---

## 1. Verify Dataset Availability

The project comes pre-packaged with sample datasets inside `data/raw/`:

- `data/raw/churn_train.csv`: Telecom customer churn training data.
- `data/raw/churn_test.csv`: Telecom customer churn holdout test data.

Verify that the training data exists:

=== "Windows (PowerShell)"
`powershell
    Test-Path data\raw\churn_train.csv
    `

=== "Linux / macOS"
`bash
    ls -lh data/raw/churn_train.csv
    `

---

## 2. Launching an Experiment

To execute an experiment, invoke the `main` module and supply a YAML configuration path:

```bash
python -m main --config configs/mvp.yaml --logging-level DEBUG
```

### CLI Arguments

| Parameter         | Type     | Required | Default  | Description                                                  |
| :---------------- | :------- | :------- | :------- | :----------------------------------------------------------- |
| `--config`        | `string` | **Yes**  | —        | Path to the YAML configuration file defining the experiment. |
| `--logging-level` | `string` | No       | `"INFO"` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).     |

---

## 3. Sample Execution Output

Upon running the pipeline, you will see structured, colorized terminal logs detailing each phase:

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

## 4. Inspecting Runs in MLflow

1. Navigate to [http://localhost:5000](http://localhost:5000) in your web browser.
2. Select the experiment named `customer_churn_experiments`.
3. View the newly logged run:
    - **Parameters**: Hyperparameters and model settings.
    - **Metrics**: Accuracy, F1 score.
    - **Artifacts**: Check the `logs/` directory in the artifact browser to inspect the full session execution log file.

---

## 5. Running with XGBoost

To train a gradient boosted tree model, switch to the XGBoost configuration:

```bash
python -m main --config configs/mvp_xgboost.yaml --logging-level INFO
```
