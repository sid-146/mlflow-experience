# Data Ingestion & Splitting

The data layer (`src.core.handler.data`) provides resilient data reading, path resolution, and deterministic dataset splitting.

---

## 1. Dynamic Path Resolution

Datasets can be specified in configuration files using relative paths, absolute paths, or paths relative to the repository root. `DataLoader._resolve_path` implements a fallback resolution strategy:

```python
def _resolve_path(self, path: str) -> str:
    if os.path.isabs(path):
        return path

    cwd_path = Path(os.getcwd()) / path
    if cwd_path.exists():
        return str(cwd_path)

    repo_root = Path(__file__).resolve().parents[4]
    repo_path = repo_root / path
    if repo_path.exists():
        return str(repo_path)

    return str(path)
```

This ensures that running `main.py` from different working directories or CI/CD pipelines will correctly locate datasets.

---

## 2. Supported Data Formats

The `DataLoader` reads files into Pandas DataFrames using format handlers:

| Extension / Type | Underlying Reader | Implementation |
| :--- | :--- | :--- |
| `csv` | `pd.read_csv` | High-performance CSV parsing |
| `excel` / `xlsx` | `pd.read_excel` | OpenPyXL / xlrd parsing |
| `json` | `pd.read_json` | JSON tabular records reader |

---

## 3. Train-Test Splitting

Splitting is decoupled from data transformation to prevent information leakage:

- If a `test` dataset is defined in the configuration, `DataLoader` loads both files independently.
- If only `train` is defined, `DataSplitter` executes `sklearn.model_selection.train_test_split`:

```python
class DataSplitter:
    def __init__(self, context: RunContext):
        self.context = context
        self.test_size = context.dataset.train_test_split or 0.2
        self.random_state = context.dataset.random_state

    def split(self, X, y) -> Tuple:
        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
        )
```
