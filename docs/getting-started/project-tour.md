# Project Tour

This guide gives you a clear map of the repository so you know exactly where everything lives and what each file does.

---

## High-Level Directory Layout

```text
mlflow-experience/
├── configs/            # Experiment YAML files
├── data/raw/           # Datasets (CSV, Excel, etc.)
├── docs/               # Documentation website source files
├── src/                # Core Python package
│   ├── orchestrator.py # Central conductor of the pipeline
│   └── core/           # Submodules (context, handlers, pipelines, trackers, logging)
├── main.py             # Entrypoint script with CLI argument parser
├── compose.yaml        # Docker Compose configuration for MLflow tracking stack
├── Dockerfile          # Container build file
├── mkdocs.yml          # Documentation site configuration
├── pyproject.toml      # Project metadata & dependencies managed by uv
└── uv.lock             # Deterministic dependency lockfile
```

---

## Key Files & Directories

### 1. Root Files
- **`main.py`**: The CLI entrypoint. It parses the `--config` and `--logging-level` flags, loads the configuration, and executes the `Orchestrator`.
- **`compose.yaml`**: Defines Docker services for running the full MLflow tracking stack (PostgreSQL database, MinIO S3 object storage, and MLflow server).
- **`pyproject.toml` & `uv.lock`**: Managed by `uv`. Defines pinned dependencies including `mlflow`, `scikit-learn`, `pydantic`, `pandas`, `xgboost`, and `mkdocs`.
- **`mkdocs.yml`**: Configures the documentation website theme, plugins, and navigation structure.

---

### 2. `configs/` — Experiment Definitions
All experiments are declared in YAML. You never need to hardcode feature names or model types in Python.
- **`configs/mvp.yaml`**: The working baseline configuration. Trains a Logistic Regression model on customer churn.
- **`configs/mvp_xgboost.yaml`**: Same preprocessing, but trains an XGBoost classifier with custom tree hyperparameters.
- **`configs/preprocessing.yaml`**: A comprehensive reference demonstrating advanced preprocessing (binning, filtering, outlier clipping, etc.).

---

### 3. `data/raw/` — Datasets
Stores the raw tabular data files:
- **`churn_train.csv`**: 400,000+ records of telecom customer behaviors with churn labels.
- **`churn_test.csv`**: Holdout test set.

---

### 4. `src/` — Source Code

#### `src/orchestrator.py`
The most important file in the project. The `Orchestrator` is a Python context manager (`with Orchestrator(...) as orch:`). It connects all components:
1. `build()`: Loads data, splits into train/test, builds transformers, and builds the Scikit-Learn `Pipeline`.
2. `train()`: Fits the pipeline on the training split and calculates training metrics.
3. `test()`: Predicts on the test split and calculates holdout metrics.
4. `__exit__()`: Automatically uploads the runtime log file to MLflow artifacts.

#### `src/core/context/`
Manages configuration schemas and data validation via Pydantic v2:
- **`contexts.py`**: Defines the `RunContext` root model and sub-contexts (`ProjectContext`, `MlFlowContext`, `DataContext`, `PreprocessingContext`, `ModelContext`, `EvaluationContext`).
- **`policies.py`**: Defines column-level policies (`RenamePolicy`, `TypeCastPolicy`, `MissingValuePolicy`, `EncodingPolicy`, `ScalingPolicy`, `DatasetPolicy`).

#### `src/core/constants/`
Lookup registries that connect YAML strings to Python classes:
- **`registry.py`**: Maps strings to transformer classes (`PreprocessingRegistry`) and model classes (`ModelType`).
- **`constants.py`**: Literal types for supported file formats (`csv`, `parquet`, `excel`) and imputation strategies.

#### `src/core/handler/`
Handles I/O:
- **`config/loader.py`**: Loads and parses YAML files via `yaml.safe_load`.
- **`data/loader.py`**: Finds and reads data files into Pandas DataFrames, dropping target columns to produce `X` and `y`.
- **`data/splitter.py`**: Wraps Scikit-Learn's `train_test_split` to safely partition `X` and `y`.

#### `src/core/pipelines/`
Constructs the Scikit-Learn pipeline:
- **`preprocessing.py`**: Iterates through the steps in `context.preprocessing` and instantiates matching transformer instances.
- **`transformers.py`**: Contains custom Scikit-Learn transformers (`RenameColumnsTransformer`, `MissingValueTransformer`, `CleaningTransformer`, `FilterTransformer`, `ScalingTransformer`, `EncodingTransformer`).
- **`model_builder.py`**: Instantiates the model estimator (e.g. `LogisticRegression` or `XGBClassifier`) with the user's hyperparameters.
- **`evaluation.py`**: Helper for computing accuracy, F1 score, and other metrics.

#### `src/core/trackers/`
- **`mlflow_tracker.py`**: Wrapper around the MLflow client. Handles creating experiments, starting runs, logging parameters, metrics, models, and artifacts.

#### `src/core/logging/` & `src/core/logs/`
- **`logger.py`**: Sets up two logging handlers: colorized output to your terminal, and persistent timestamped log files saved in `src/core/logs/`.
