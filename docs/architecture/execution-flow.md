# End-to-End Execution Flow

This document details the complete end-to-end data and control flow when an experiment is executed via `main.py`.

---

## Detailed Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant CLI as main.py
    participant Loader as config_loader
    participant Context as RunContext (Pydantic)
    participant Orch as Orchestrator
    participant Tracker as MLflowTracker
    participant DLoader as DataLoader
    participant DSplit as DataSplitter
    participant Prep as PreprocessingPipeline
    participant MBuild as ModelBuilder
    participant Pipe as sklearn.Pipeline

    User->>CLI: python -m main --config configs/mvp.yaml
    CLI->>Loader: config_loader("configs/mvp.yaml")
    Loader-->>CLI: config dict
    CLI->>Context: RunContext.from_yaml_dict(config)
    Context-->>CLI: validated context object
    CLI->>Orch: with Orchestrator(context) as orchestrator
    Orch->>Orch: __enter__()

    CLI->>Orch: orchestrator.build()
    Orch->>Tracker: start_run()
    Tracker->>Tracker: set_experiment() & create_run()
    Orch->>DLoader: load_data()
    DLoader->>DLoader: _load_train_data() -> (X, y)
    Orch->>DSplit: split(X, y)
    DSplit-->>Orch: (X_train, X_test, y_train, y_test)

    Orch->>Prep: build()
    Prep->>Prep: instantiate transformers from registry
    Prep-->>Orch: [(step_name, transformer_instance), ...]

    Orch->>MBuild: build()
    MBuild->>MBuild: instantiate estimator with hyperparameters
    MBuild-->>Orch: [(task, model_instance)]

    Orch->>Pipe: Pipeline(pipeline_steps)

    CLI->>Orch: orchestrator.train()
    Orch->>Pipe: fit(X_train, y_train)
    Pipe-->>Orch: fitted pipeline
    Orch->>Pipe: predict(X_train)
    Orch->>Orch: evaluate(y_train, y_train_pred)

    CLI->>Orch: orchestrator.test()
    Orch->>Pipe: predict(X_test)
    Orch->>Orch: evaluate(y_test, y_test_pred)

    CLI->>Orch: context manager exit
    Orch->>Orch: __exit__()
    Orch->>Tracker: log_artifact(log_filepath)
    Tracker-->>Orch: log artifact stored in S3/MinIO
```

---

## State Isolation & Leakage Prevention

One of the most critical aspects of this execution sequence is **strict temporal ordering**:

1. **Splitting Occurs Before Fitting**: The raw data is split into $X_{train}, y_{train}$ and $X_{test}, y_{test}$ before any transformer is instantiated or fitted.
2. **Transformers Fit Only on Training Split**: When `pipeline.fit(X_train, y_train)` executes, transformers compute statistics (such as feature means, standard deviations, or category frequencies) strictly using the training observations.
3. **Deterministic Evaluation**: During testing (`pipeline.predict(X_test)`), Scikit-Learn applies only the `.transform()` methods, projecting test samples into the exact feature space learned during training.
