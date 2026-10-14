# Architectural Blueprint

The architecture of `mlflow-experience` is designed around three core principles:

1. **Modularity**: Components are independently testable and easily replaceable.
2. **Configurability**: Experiment logic is declarative and specified through versioned YAML documents.
3. **Observability**: Execution events, parameters, metrics, and models are automatically tracked.

---

## The 5 Architectural Layers

The system follows a strict layered pattern, isolating concerns across five distinct tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Layer 5: Orchestration & Execution (The Conductor)                     │
│ Orchestrator context manager: build() -> train() -> test() -> exit()   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ coordinates
┌──────────────────────────────────▼─────────────────────────────────────┐
│ Layer 4: Transformation & ML Logic (The Engine)                        │
│ PreprocessingPipeline (Transformers) + ModelBuilder (Estimator)        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ operates on
┌──────────────────────────────────▼─────────────────────────────────────┐
│ Layer 3: Data Management & Ingestion (The I/O Layer)                   │
│ DataLoader (CSV, Excel, JSON) + DataSplitter (train_test_split)        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ consumes
┌──────────────────────────────────▼─────────────────────────────────────┐
│ Layer 2: Configuration & Validation (The Brain)                        │
│ config_loader (YAML) -> RunContext & Pydantic Policies                 │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ instrumented with
┌──────────────────────────────────▼─────────────────────────────────────┐
│ Layer 1: Infrastructure & Observability (The Foundation)               │
│ MLflowTracker (Runs, Params, Metrics, Artifacts) + Colored Logger      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Layer 1: Infrastructure & Observability

- **Primary Component**: `MLflowTracker` (`src.core.trackers.mlflow_tracker`) and `console` logger (`src.core.logging.logger`).
- **Responsibility**: Manages the connection to external tracking systems (e.g. MLflow on PostgreSQL + MinIO S3). Handles experiment initialization, run creation, parameter logging, metric capture, and file artifact streaming upon completion.

### Layer 2: Configuration & Validation

- **Primary Component**: `config_loader` (`src.core.handler.config.loader`) and `RunContext` (`src.core.context.contexts`).
- **Responsibility**: Loads YAML files and enforces strict Pydantic v2 schemas. Translates untyped nested dictionaries into strongly-typed policy objects (`RenamePolicy`, `TypeCastPolicy`, `MissingValuePolicy`, `EncodingPolicy`, `ScalingPolicy`).

### Layer 3: Data Management & Ingestion

- **Primary Component**: `DataLoader` (`src.core.handler.data.loader`) and `DataSplitter` (`src.core.handler.data.splitter`).
- **Responsibility**: Resolves file paths (absolute, relative, repository root), dispatches the appropriate reader for the file format (`csv`, `excel`, `json`), and executes train-test splits before any feature transformations take place.

### Layer 4: Transformation & ML Logic

- **Primary Component**: `PreprocessingPipeline` (`src.core.pipelines.preprocessing`), `transformers.py`, and `ModelBuilder` (`src.core.pipelines.model_builder`).
- **Responsibility**: Instantiates Scikit-Learn transformers and estimator classes based on the validated configuration. Assembles these components into a unified, sequential `sklearn.pipeline.Pipeline`.

### Layer 5: Orchestration & Execution

- **Primary Component**: `Orchestrator` (`src.orchestrator`).
- **Responsibility**: Serves as the high-level conductor. Controls the execution order (`build()`, `train()`, `test()`, `evaluate()`), ensures data integrity, and finalizes run artifacts via the context manager protocol (`__enter__` / `__exit__`).
