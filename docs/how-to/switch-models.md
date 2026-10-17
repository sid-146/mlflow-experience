# How to Switch and Tune Models

This guide shows you how to change model algorithms (e.g. from Logistic Regression to XGBoost) and tune their hyperparameters simply by editing your YAML configuration.

---

## The Scenario

You ran a baseline experiment with Logistic Regression, but now you want to test whether a gradient boosted decision tree (XGBoost) achieves higher accuracy or F1 score.

---

## Step 1: Switch to XGBoost in YAML

Find the `model` block in your configuration file and change `type` from `logistic_regression` to `xgboost`:

```yaml
# Before: Logistic Regression
model:
  type: logistic_regression
  task: 'binary:classification'
  hyperparameters:
    C: 1.0
    max_iter: 250
    solver: saga
```

```yaml
# After: XGBoost Classifier
model:
  type: xgboost
  task: 'xgboost:classification'
  hyperparameters:
    n_estimators: 500       # Number of boosting trees
    learning_rate: 0.05     # Shrinkage step size
    max_depth: 6            # Maximum tree depth
    subsample: 0.8          # Fraction of samples to train each tree
    random_state: 42
```

Also update the training objective:

```yaml
training:
  objective: xgboost:binary:classification
```

---

## Step 2: Common Hyperparameters to Tune

### For Logistic Regression (`type: logistic_regression`)
| Parameter | Default | Typical Values | What It Does |
| :--- | :--- | :--- | :--- |
| `C` | `1.0` | `0.01`, `0.1`, `1.0`, `10.0` | Inverse of regularization strength. Smaller values = stronger regularization. |
| `max_iter` | `100` | `200`, `500`, `1000` | Maximum solver iterations for convergence. |
| `solver` | `'lbfgs'` | `'lbfgs'`, `'saga'`, `'liblinear'` | Optimization algorithm (`saga` is recommended for large datasets). |

### For XGBoost (`type: xgboost`)
| Parameter | Default | Typical Values | What It Does |
| :--- | :--- | :--- | :--- |
| `n_estimators`| `100` | `100`, `300`, `1000` | Number of gradient boosted trees to build. |
| `learning_rate`| `0.3` | `0.01`, `0.05`, `0.1` | Step size shrinkage used to prevent overfitting. |
| `max_depth` | `6` | `3`, `6`, `10` | Maximum depth of a tree. Higher values capture complex patterns but risk overfitting. |
| `subsample` | `1.0` | `0.7`, `0.8`, `1.0` | Subsample ratio of the training instances. |

---

## Step 3: Run the New Model

```bash
uv run python -m main --config configs/mvp_xgboost.yaml --logging-level INFO
```

---

## Step 4: Compare Models Side-by-Side in MLflow

1. Open the MLflow UI at [http://localhost:5000](http://localhost:5000).
2. Open your experiment (e.g. `customer_churn_experiments`).
3. Check the checkboxes next to both your Logistic Regression run and your XGBoost run.
4. Click the **Compare** button at the top of the table.
5. Review the side-by-side comparison of **Accuracy**, **F1 Score**, and **Hyperparameters** to pick the winning model!
