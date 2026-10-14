# Contributing to mlflow-experience

Thank you for your interest in contributing to `mlflow-experience`! We welcome contributions from the community—whether it's reporting a bug, proposing an architectural enhancement, adding new custom transformers, or improving documentation.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Environment Setup](#development-environment-setup)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Message Conventions](#commit-message-conventions)
- [Code Quality & Architectural Standards](#code-quality--architectural-standards)
  - [Pydantic v2 Policy Enforcement](#pydantic-v2-policy-enforcement)
  - [Scikit-Learn Transformer Guidelines](#scikit-learn-transformer-guidelines)
  - [Logging Over Print](#logging-over-print)
- [Verification & Testing](#verification--testing)
- [Documentation Guidelines](#documentation-guidelines)

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please treat all contributors with respect, empathy, and professional courtesy.

---

## How to Contribute

### Reporting Bugs

Before creating an issue, search the issue tracker to ensure the bug hasn't already been reported.

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

4. **(Optional) Local MLflow Stack:**
   If your changes involve tracking or artifact uploads, start the local tracking services:
   ```bash
   docker compose up -d
   ```
   Access the MLflow UI at [http://localhost:5000](http://localhost:5000).

---

## Development Workflow

### Branching Strategy

Use descriptive branch prefixes:
- `feature/` for new functionality (e.g., `feature/random-forest-support`, `feature/outlier-transformer`)
- `bugfix/` or `fix/` for bug fixes (e.g., `fix/data-loader-path-resolution`)
- `docs/` for documentation updates (e.g., `docs/add-dag-roadmap`)
- `refactor/` for code restructuring without changing behavior

### Commit Message Conventions

We follow Conventional Commits formatting:

```text
<type>(<scope>): <short description>

[optional body]
```

**Common Types:**
- `feat`: A new feature (e.g., `feat(transformers): add OutlierTransformer with quantile clipping`)
- `fix`: A bug fix (e.g., `fix(orchestrator): prevent test split data leak`)
- `docs`: Documentation updates (e.g., `docs(mkdocs): add transformer tutorial`)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `chore`: Maintenance tasks (e.g., `chore(deps): update uv.lock`)

---

## Code Quality & Architectural Standards

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

1. **Run the Logistic Regression pipeline:**
   ```bash
   uv run python -m main --config configs/mvp.yaml --logging-level DEBUG
   ```

2. **Run the XGBoost pipeline:**
   ```bash
   uv run python -m main --config configs/mvp_xgboost.yaml --logging-level INFO
   ```

3. **Verify Linting (`flake8`):**
   ```bash
   uv run flake8 .
   ```

4. **Verify Documentation Build:**
   ```bash
   uv run mkdocs build --strict
   ```
   Ensure no broken links or formatting errors exist.

---

## Documentation Guidelines

If you introduce a new feature or configuration setting:
- Update [README.md](README.md) with relevant usage examples.
- Add or update the corresponding Markdown page in `docs/` (`docs/configuration/`, `docs/pipelines/`, or `docs/developer-guide/`).
- Preview your changes locally:
  ```bash
  uv run mkdocs serve
  ```

---

## Questions & Getting Help

If you have questions or need guidance on implementation details, feel free to open a GitHub Discussion or submit a draft Pull Request.
