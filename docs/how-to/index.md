# How-To Guides

Welcome to the **How-To Guides**! These task-oriented recipes provide step-by-step instructions for common real-world development workflows with `mlflow-experience`.

---

## Quick Finder: What Do You Want to Do?

| Goal | Guide | Quick Summary |
| :--- | :--- | :--- |
| **Train on my own data** | [Custom Dataset](custom-dataset.md) | Plug in a new CSV, Excel, or JSON file and set target/ID columns. |
| **Handle missing values** | [Handle Missing Data](handle-missing-data.md) | Impute columns with mean, median, mode, or constants without data leakage. |
| **Convert text to numbers** | [Categorical Encoding](categorical-encoding.md) | Use one-hot or ordinal encoding for categorical features. |
| **Scale numeric features** | [Scaling Strategies](scaling-strategies.md) | Normalize features with StandardScaler, MinMaxScaler, or RobustScaler. |
| **Fix dirty labels or filter rows** | [Clean & Filter](clean-and-filter.md) | Map typos/acronyms and remove invalid rows with query conditions. |
| **Change ML algorithms** | [Switch Models](switch-models.md) | Toggle between Logistic Regression and XGBoost, and tune hyperparameters. |
| **Run without Docker** | [Offline MLflow](offline-mlflow.md) | Track experiments with a local SQLite file (`sqlite:///mlflow.db`). |

---

## Guides by Category

### 1. Data Ingestion & Sanitization
- [**Train on Your Own Dataset**](custom-dataset.md): How to configure file paths, set primary key IDs, specify targets, and provide pre-split train/test datasets.
- [**Clean Values and Filter Rows**](clean-and-filter.md): How to replace messy category labels and filter erroneous rows using query conditions.

### 2. Feature Engineering & Preprocessing
- [**Handle Missing Data**](handle-missing-data.md): How to apply column-specific imputation strategies without leaking test statistics.
- [**Encode Categorical Features**](categorical-encoding.md): How to handle nominal and ordinal features with unknown value tolerance.
- [**Scale Numerical Features**](scaling-strategies.md): When and how to apply Standard, Min-Max, or Robust scaling.

### 3. Model Training & Experiment Tracking
- [**Switch Models & Tune Hyperparameters**](switch-models.md): How to move from baseline linear models to XGBoost, adjust parameters, and compare metrics.
- [**Run MLflow Without Docker**](offline-mlflow.md): How to track experiments, parameters, and artifacts locally via SQLite or local filesystem.
