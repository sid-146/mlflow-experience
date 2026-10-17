# Model Building & Estimators

The `ModelBuilder` class (`src/core/pipelines/model_builder.py`) instantiates the machine learning algorithm that forms the final step of the Scikit-Learn pipeline.

---

## 1. Supported Model Families

Models are registered in the `ModelType` enum in `src/core/constants/registry.py`:

| YAML `type` | Python Class | Underlying Library |
| :--- | :--- | :--- |
| `logistic_regression` | `LogisticRegression` | Scikit-Learn |
| `xgboost` | `XGBClassifier` | XGBoost |

---

## 2. Dynamic Hyperparameter Forwarding

You can configure any constructor parameter supported by the model directly in YAML under `hyperparameters`.

### Example A: Logistic Regression

```yaml
model:
  type: logistic_regression
  task: 'binary:classification'
  hyperparameters:
    C: 1.0                # Inverse regularization strength
    max_iter: 250         # Maximum solver iterations
    solver: saga          # Algorithm to use for optimization problem
    random_state: 42
```

### Example B: XGBoost Classifier

```yaml
model:
  type: xgboost
  task: 'xgboost:classification'
  hyperparameters:
    n_estimators: 500     # Number of boosted trees
    learning_rate: 0.01   # Step size shrinkage
    max_depth: 6          # Maximum tree depth
    subsample: 0.8        # Subsample ratio of training instances
    random_state: 42
```

---

## 3. How It Is Added to the Pipeline

Inside `orchestrator.py`:

```python
# 1. Build model step
model_step = (
    self.model_builder.build()
)  # Returns [('binary:classification', model_instance)]

# 2. Append to pipeline steps
self.pipeline_steps.extend(model_step)

# 3. Create the unified Scikit-Learn Pipeline
self.pipeline = Pipeline(self.pipeline_steps)
```

Because the model is just the final step in the pipeline:
- Calling `pipeline.fit(X_train, y_train)` fits all preprocessing transformers first, then fits the model on the transformed features.
- Calling `pipeline.predict(X_test)` runs test data through all transformers first, then outputs predictions.
