# Configuration Examples

Below are complete, production-ready configuration examples included with the repository.

---

## 1. Logistic Regression Baseline (`configs/mvp.yaml`)

This configuration runs a linear classifier on telecom churn data, including renaming, missing value imputation, ordinal/one-hot encoding, and scaling.

```yaml
project:
  name: customer_churn_prediction
  owner: data_science_team
  environment: production
  description: Predict customer churn for telecom users

mlflow:
  experiment_name: customer_churn_experiments
  experiment_id: NA
  track_params: true
  track_metrics: true
  track_artifacts:
    - feature_config
    - preprocessing_objects
    - model
  tags:
    project: churn
    stage: production
    owner: data_science_team

dataset:
  dataset_name: telecom_churn_v1
  random_state: 52
  train_test_split: 0.2
  train:
    type: csv
    path: data/raw/churn_train.csv
    id_column: CustomerID
    target_column: Churn
    positive_class: 1

preprocessing:
  - name: rename_columns
    type: rename
    params:
      mapping:
        CustomerID: customer_id
        Usage Frequency: usage_frequency
        Support Calls: support_calls
        Payment Delay: payment_delay
        Subscription Type: subscription_type
        Contract Length: contract_length
        Total Spend: total_spend
        Last Interaction: last_interaction

  - name: cast_types
    type: type_cast
    params:
      columns:
        - name: Age
          dtype: int
        - name: Gender
          dtype: str
        - name: Tenure
          dtype: int

  - name: handle_missing
    type: missing
    params:
      columns:
        - name: Age
          strategy: mean
        - name: Gender
          strategy: mode

  - name: encode_features
    type: encoding
    params:
      columns:
        - name: Gender
          strategy: ordinal
          order: ['Male', 'Female']
        - name: contract_length
          strategy: ordinal
          order: ['Monthly', 'Quarterly', 'Annual']
        - name: subscription_type
          strategy: one_hot

  - name: scale_features
    type: scaling
    params:
      columns:
        - name: Age
          strategy: standard
        - name: total_spend
          strategy: minmax

model:
  type: logistic_regression
  task: 'binary:classification'
  hyperparameters:
    C: 1.0
    max_iter: 250
    solver: saga

training:
  objective: binary:logistic

evaluation:
  metrics:
    - accuracy
    - f1
```

---

## 2. XGBoost Gradient Boosting (`configs/mvp_xgboost.yaml`)

This configuration switches the model family to XGBoost with specialized tree hyperparameters:

```yaml
# Same project, mlflow, dataset, and preprocessing sections as mvp.yaml...
model:
  type: xgboost
  task: 'xgboost:classification'
  hyperparameters:
    n_estimators: 1000
    learning_rate: 0.001
    max_depth: 10
    random_state: 42

training:
  objective: xgboost:binary:classification

evaluation:
  metrics:
    - accuracy
    - f1
```
