# Contributing Guidelines

Thank you for your interest in contributing to `mlflow-experience`! We welcome contributions from the community—whether it's reporting a bug, proposing an architectural enhancement, adding new custom transformers, or improving documentation.

---

## How to Contribute

### Reporting Bugs

When opening a bug report, please include:
1. **Clear description**: What happened vs. what was expected.
2. **Environment details**: OS, Python version (`python --version`), and `uv` version (`uv --version`).
3. **Minimal reproducible configuration**: The YAML config file used.
4. **Execution logs**: Attach or paste the terminal traceback or the log file generated in `src/core/logs/`.

### Suggesting Enhancements

Feature requests are welcome! When proposing a new feature:
- Explain the **use case** and the problem it solves.
- Describe how it fits within the 5-layer architecture.
- If applicable, outline proposed changes to the YAML schema and Pydantic policies.

### Submitting Pull Requests

1. Fork the repository and clone your fork locally.
2. Create a new branch for your change (`git checkout -b feature/your-feature-name`).
3. Install dependencies and set up the environment with `uv sync`.
4. Make your changes adhering to project architectural standards.
5. Verify code quality, run sample configs, and ensure documentation builds cleanly.
6. Commit with clear, descriptive commit messages.
7. Push to your fork and submit a Pull Request to `main`.

---

## Development Environment Setup

This project uses [**uv**](https://docs.astral.sh/uv/) for high-speed, deterministic dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/mlflow-experience.git
   cd mlflow-experience
   ```

2. **Synchronize environment:**
   ```bash
   uv sync
   ```
   This automatically creates a `.venv` virtual environment and installs all locked dependencies from `uv.lock`.

3. **Verify the environment:**
   ```bash
   uv run python -m main --help
   ```

4. **Local MLflow Stack:**
   ```bash
   docker compose up -d
   ```
   Access the MLflow UI at [http://localhost:5000](http://localhost:5000).

---

## Code Quality Standards

### Pydantic v2 Policy Enforcement
- Any new YAML configuration field **must** be validated through a Pydantic model in `src/core/context/contexts.py` or `src/core/context/policies.py`.
- Enforce strict typing with field validators and literal types where applicable.
- Never pass raw, unvalidated dictionaries directly into business logic.

### Scikit-Learn Transformer Guidelines
When authoring custom transformers in `src/core/pipelines/transformers.py`:
1. **Inheritance**: Always inherit from `BaseEstimator` and `TransformerMixin`.
2. **State Learning**: Learn all parameters (means, medians, scales, categories) **only** during `fit(X, y=None)`.
3. **Data Immutability**: In `transform(X)`, avoid in-place mutations on the incoming DataFrame; use `X = X.copy()` when necessary.
4. **DataFrame Output**: Ensure transformers return Pandas DataFrames to preserve column names across stages (`set_config(transform_output="pandas")`).
5. **Registry Mapping**: Register new transformers in `PreprocessingRegistry` (`src/core/constants/registry.py`).

### Logging Over Print
- **Do not use `print()` statements** in library code.
- Import and use the centralized logger:
  ```python
  from src.core.logging.logger import console

  console.debug("Detailed diagnostic message")
  console.info("Milestone status update")
  console.warning("Recoverable issue detected")
  console.error("Critical step failure")
  ```

---

## Verification & Testing

Before submitting a Pull Request, verify your changes against the sample datasets:

```bash
# 1. Run the Logistic Regression pipeline
uv run python -m main --config configs/mvp.yaml --logging-level DEBUG

# 2. Run the XGBoost pipeline
uv run python -m main --config configs/mvp_xgboost.yaml --logging-level INFO

# 3. Verify Linting (flake8)
uv run flake8 .

# 4. Verify Documentation Build
uv run mkdocs build --strict
```
