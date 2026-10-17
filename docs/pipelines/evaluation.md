# Model Evaluation

This document explains how model performance is evaluated and recorded in `mlflow-experience`.

---

## 1. Evaluation Stages

The `Orchestrator` performs evaluation at two distinct points during a run:

1. **Training Evaluation (In-Sample)**:
   Immediately after fitting the pipeline on the training split, `orchestrator.train()` predicts on $X_{train}$ and evaluates against $y_{train}$. This lets you check if the model is underfitting or overfitting.
2. **Testing Evaluation (Out-of-Sample)**:
   In `orchestrator.test()`, the pipeline predicts on the held-out test split $X_{test}$ and evaluates against true $y_{test}$. This provides the unbiased estimate of generalization performance.

---

## 2. Supported Metrics

Currently, evaluation calculates:
- **Accuracy**: Proportion of correct predictions over total predictions.
- **F1 Score**: Harmonic mean of precision and recall.

In your console output, evaluation results are formatted cleanly:

```text
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 146 : --- Starting Evaluation (on provided dataset) ---
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 158 : | Accuracy  : 0.8425
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 158 : | F1 Score  : 0.8110
INFO : 2026-10-14 23:28:18 : orchestrator.py : [evaluate] : 160 : --- Evaluation Complete ---
```

---

## 3. Configuration in YAML

In your experiment YAML, specify which metrics you want tracked:

```yaml
evaluation:
  metrics:
    - accuracy
    - f1
```

---

## 4. How to Add More Metrics

To add more metrics (such as Precision, Recall, or ROC-AUC), update `evaluate()` in `src/orchestrator.py`:

```python
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

metrics = {
    "Accuracy": accuracy_score(y_true, y_pred),
    "F1 Score": f1_score(y_true, y_pred),
    "Precision": precision_score(y_true, y_pred, zero_division=0),
    "Recall": recall_score(y_true, y_pred, zero_division=0),
}

for metric_name, score in metrics.items():
    console.info(f"| {metric_name:<10}: {score:.4f}")
```
