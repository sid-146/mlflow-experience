# Architectural Roadmap

This document outlines key technical evolution milestones for `mlflow-experience`.

---

## 1. Directed Acyclic Graph (DAG) Pipeline Engine

### The Problem

Linear Scikit-Learn pipelines force every step to execute in a single strict sequence ($Step_1 \to Step_2 \to Step_3$). Real-world data science projects require branching flows:

- Separate numeric and text pipelines that execute independently and merge downstream.
- Parallel transformer paths.

### Target Architecture

A DAG engine that:

1. Accepts explicit node dependencies in YAML:
    ```yaml
    pipeline:
        nodes:
            - name: clean
              type: cleaning
            - name: num_scaling
              type: scaling
              depends_on: [clean]
            - name: cat_encoding
              type: encoding
              depends_on: [clean]
            - name: merge
              type: merge
              depends_on: [num_scaling, cat_encoding]
    ```
2. Resolves execution order dynamically using **Topological Sorting** (Kahn's algorithm or DFS).
3. Detects and prevents circular graph cycles at build time.

---

## 2. Nested MLflow Runs & Automatic Node Decorators

### The Problem

Currently, the entire pipeline is tracked within a single MLflow run. Debugging failures in specific transformation steps requires reading text logs.

### Target Architecture

Introduce hierarchical parent-child runs:

```text
pipeline_run (Parent)
 ├── clean (Child Run)
 ├── handle_missing (Child Run)
 ├── encode_features (Child Run)
 ├── scale_features (Child Run)
 └── model_fit (Child Run)
```

By wrapping transformer execution in a `@track_node` decorator, each step automatically records:

- Input/output row and column shapes.
- Step execution duration in milliseconds.
- Step parameters and missing-value counts.

---

## 3. Feature Engineering Factory

Formalize the placeholder in `src.core.pipelines.features` into a configurable feature factory:

- **Statistical Aggregations**: Group-by operations (mean, std, min, max, count).
- **Interactions**: Automated ratio, difference, and polynomial feature generation.
- **Temporal Transformations**: Cyclical Sine/Cosine encoding of calendar dates and rolling window metrics.
