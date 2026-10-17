# Troubleshooting & FAQ

Quick solutions for common errors encountered during development.

---

## 1. MLflow Connection Error (`ConnectionRefusedError`)

### Error Symptom
```text
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /api/2.0/mlflow/experiments/get-by-name
```

### Why It Happens
The pipeline is trying to connect to an MLflow tracking server at `http://localhost:5000`, but no server is listening on that port.

### How to Fix

**Option A: Start the local MLflow server with uv**
```bash
uv run mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --port 5000
```

**Option B: Start the Docker stack**
```bash
docker compose up -d
```

**Option C: Track directly to local disk without a server**
Edit your YAML configuration to log directly to a local folder:
```yaml
mlflow:
  tracking_uri: file:./mlruns
```

---

## 2. Pydantic `ValidationError`

### Error Symptom
```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for MissingValueConfig
strategy
  Input should be 'mean', 'median', 'mode' or 'constant' [type=literal_error, input_value='average', input_type=str]
```

### Why It Happens
You used an unsupported strategy name or misspelled a parameter in your YAML file.

### How to Fix
Look at the error message: it tells you the exact field (`strategy`) and the valid allowed values (`'mean', 'median', 'mode' or 'constant'`). Update your YAML file accordingly.

---

## 3. `KeyError` on Column Names

### Error Symptom
```text
KeyError: 'Total Spend'
```

### Why It Happens
You renamed a column in an early preprocessing step, but referenced the **old** column name in a later step (e.g. imputation, scaling, or encoding).

### How to Fix
Remember that steps run in sequential order. If you rename `"Total Spend"` to `total_spend`, all subsequent steps must use `total_spend`:

```yaml
preprocessing:
  - name: rename_columns
    type: rename
    params:
      mapping:
        "Total Spend": total_spend

  - name: scale_features
    type: scaling
    params:
      columns:
        - name: total_spend  # <--- Use the new renamed name here!
          strategy: minmax
```

---

## 4. `FileNotFoundError` When Loading Data

### Error Symptom
```text
FileNotFoundError: File not found on given path: data/raw/churn_train.csv
```

### Why It Happens
The file path specified in `dataset.train.path` cannot be found relative to your current working directory or repository root.

### How to Fix
1. Verify that the file exists:
   ```bash
   ls data/raw/
   ```
2. Paths are resolved relative to the repository root. Ensure the path in YAML is `data/raw/filename.csv`.

---

## 5. Model Not Configured Error

### Error Symptom
```text
ValueError: Given model : my_custom_model is not configured yet.
```

### Why It Happens
You specified a `model.type` in YAML that has not been mapped in `src/core/constants/registry.py`.

### How to Fix
See the [Adding a New Model Guide](extending-models.md) to register your model class in `ModelType`.

---

## 6. Windows PowerShell Script Execution Error

### Error Symptom
```text
.\.venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

### Why It Happens
Windows PowerShell restricts script execution by default.

### How to Fix
You don't need to activate the virtual environment if you use `uv run`:
```bash
uv run python -m main --config configs/mvp.yaml
```

Or enable local script execution for your user account:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
