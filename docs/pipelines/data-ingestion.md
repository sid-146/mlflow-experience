# Data Ingestion & Splitting

This section explains how data is loaded from disk, separated into features and target labels, and split into training and test sets.

---

## 1. Where Does the Data Come From?

In your YAML configuration, you specify the data source under `dataset.train`:

```yaml
dataset:
  dataset_name: telecom_churn_v1
  random_state: 42
  train_test_split: 0.2
  train:
    type: csv
    path: data/raw/churn_train.csv
    id_column: CustomerID
    target_column: Churn
```

---

## 2. Smart Path Finding

You don't need to worry about path mismatches when running the command from different directories. `DataLoader` resolves paths in this order:

1. **Absolute path**: If given an absolute path (e.g. `C:\data\train.csv`), it uses it directly.
2. **Current working directory**: Checks relative to where you ran the command from (`os.getcwd()`).
3. **Repository root**: Looks up the directory tree to find the file inside the project root.

---

## 3. Supported File Formats

The `DataLoader` reads files into Pandas DataFrames using format readers registered in `DATA_READER_FUNCTIONS`:

| Format | Extension in YAML | Pandas Reader Function |
| :--- | :--- | :--- |
| CSV | `csv` | `pd.read_csv` |
| Excel | `excel` or `xlsx` | `pd.read_excel` |
| JSON | `json` | `pd.read_json` |

---

## 4. Separating Features and Target ($X$ and $y$)

When data is loaded:
1. The target column (`target_column`) is identified.
2. `self.y` is created by taking that single target column:
   ```python
   self.y = self.data[target_column]
   ```
3. `self.X` is created by dropping the target column:
   ```python
   self.X = self.data.drop(target_column, axis=1)
   ```

---

## 5. Train-Test Splitting

`DataSplitter` partitions the dataset before any preprocessing happens:

- If you provide a dedicated `dataset.test` file in your YAML, both files are loaded directly.
- If you only provide `dataset.train`, `DataSplitter` calls Scikit-Learn's `train_test_split`:
  ```python
  x_train, x_test, y_train, y_test = train_test_split(
      X, y,
      test_size=context.dataset.train_test_split or 0.2,
      random_state=context.dataset.random_state or 42
  )
  ```

This ensures that the test split remains completely untouched until final evaluation.
