# mlflow-experience

This project describes the construction of a highly automated and scalable Machine Learning Operations (MLOps) pipeline designed to train and evaluate predictive models using a comprehensive, configuration-driven framework. The core goal is to remove manual intervention from the machine learning lifecycle, allowing users to define complex experiments—from data loading to final model evaluation—simply by adjusting a YAML configuration file. This architecture ensures reproducibility and traceability, centralizing control within a robust `Orchestrator` class.

The system operates through a highly structured, multi-stage pipeline. Data ingestion begins by loading and splitting the raw data. This is followed by mandatory feature preparation, which is split into two highly modular stages: the **Preprocessing Pipeline** (handling tasks like renaming columns, imputing missing values, and encoding categories) and the **Feature Engineering Pipeline** (where domain-specific logic, such as creating statistical aggregates or temporal metrics, are added). These stages dynamically transform the raw data into a clean, numerical feature vector ready for the model.

By consolidating all steps into a single, cohesive scikit-learn `Pipeline` object, the system guarantees sequential data integrity. Furthermore, the architecture tackles advanced engineering challenges—like dynamically assembling pipeline components and implementing best practices for model evaluation, such as calculating cross-validation scores. This design makes the system incredibly resilient, allowing new model types, features, and preprocessing rules to be integrated simply by adding new components to the central configuration, without altering the underlying execution logic.

execute using following

```bash
py -m main --config configs\mvp.yaml --logging-level DEBUG
```
