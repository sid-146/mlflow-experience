# Execution Flow

This document walks you step-by-step through what happens under the hood when you run:

```bash
uv run python -m main --config configs/mvp.yaml
```

---

## Step-by-Step Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant CLI as main.py
    participant Loader as config_loader
    participant Context as RunContext (Pydantic)
    participant Orch as Orchestrator
    participant MLflow as MLflowTracker
    participant Data as DataLoader & DataSplitter
    participant Pipeline as Scikit-Learn Pipeline

    User->>CLI: Run python -m main --config configs/mvp.yaml
    CLI->>Loader: Read and parse YAML file
    Loader-->>CLI: Return raw config dict
    CLI->>Context: RunContext.from_yaml_dict(config)
    Note over Context: Validate data types & cast step policies
    Context-->>CLI: Return strongly-typed RunContext
    CLI->>Orch: Start Orchestrator context manager
    
    Orch->>MLflow: start_run()
    Note over MLflow: Create/set experiment & open active run
    
    Orch->>Data: load_data() & split(X, y)
    Note over Data: Partition into train & test splits
    Data-->>Orch: Return X_train, y_train, X_test, y_test
    
    Orch->>Pipeline: Assemble Pipeline(preprocessing_steps + model_step)
    
    Orch->>Pipeline: fit(X_train, y_train)
    Note over Pipeline: Transformers calculate means, medians, categories
    Note over Pipeline: Model learns coefficients/trees
    
    Orch->>Pipeline: predict(X_test)
    Note over Pipeline: Transformers apply learned rules to test set
    Pipeline-->>Orch: Return y_pred
    
    Orch->>Orch: evaluate(y_test, y_pred)
    Note over Orch: Calculate Accuracy & F1 score
    
    Orch->>MLflow: Upload session log artifact on exit
    MLflow-->>User: Run finished & logged to MLflow UI
```

---

## Why Splitting First Matters (Preventing Data Leakage)

**Data Leakage** is one of the most common and costly mistakes in machine learning. It happens when information from your test set accidentally leaks into the training process. 

For example:
- If you compute the **mean of a column** across the *entire* dataset before splitting, the training data now has knowledge of the test set's distribution.
- If you fit a **MinMaxScaler** on all rows, the minimum and maximum values will include test rows.

In `mlflow-experience`, data leakage is impossible by design:
1. **The split happens first**: `DataLoader` loads the data, and `DataSplitter` immediately splits it into training and testing sets.
2. **Transformers only see the training set**: When `pipeline.fit(X_train, y_train)` is called, Scikit-Learn only computes statistics (like means, standard deviations, or category mappings) on $X_{train}$.
3. **The test set is transformed blindly**: When `pipeline.predict(X_test)` runs, Scikit-Learn calls `.transform()` on each step, applying the rules learned during training without recalculating anything.
