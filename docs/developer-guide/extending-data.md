# Adding New Data Formats

By default, `mlflow-experience` reads `csv`, `excel`, and `json` files. Here is how to add support for other formats, like **Apache Parquet**.

---

## 1. Add the Format to `FILE_TYPES`

Open `src/core/constants/constants.py` and add the format string:

```python
# src/core/constants/constants.py

FILE_TYPES = Literal[
    "csv",
    "parquet",  # <--- Add this
    "excel",
    "xlsx",
    "json",
]
```

---

## 2. Register the Pandas Reader Function

Open `src/core/constants/registry.py` and `src/core/handler/data/loader.py`:

```python
# In src/core/constants/registry.py
DATA_READER_FUNCTIONS: Dict[str, Callable[[str], pd.DataFrame]] = {
    "csv": pd.read_csv,
    "excel": pd.read_excel,
    "json": pd.read_json,
    "parquet": pd.read_parquet,  # <--- Add this
}
```

Make sure the same entry is in `DataLoader.__init__` in `src/core/handler/data/loader.py`:

```python
self.DATA_READER_FUNCTIONS = {
    "csv": pd.read_csv,
    "excel": pd.read_excel,
    "json": pd.read_json,
    "parquet": pd.read_parquet,  # <--- Add this
}
```

---

## 3. Use It in Your Configuration

You can now use `.parquet` files in your YAML:

```yaml
dataset:
  train:
    type: parquet
    path: data/raw/churn_train.parquet
    id_column: CustomerID
    target_column: Churn
```
