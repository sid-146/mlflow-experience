# Logging System

The platform includes a dual-stream logging system in `src/core/logging/logger.py`:
1. **Interactive Console Stream**: Real-time output formatted with ANSI color codes.
2. **Persistent File Stream**: Timestamped log files saved in `src/core/logs/`.

---

## 1. Colorized Terminal Output

The `ColoredFormatter` colors output by severity level so you can spot errors or milestones instantly:

| Level | Color | Meaning |
| :--- | :--- | :--- |
| `DEBUG` | **Blue** | Detailed internal diagnostic messages (data shapes, step creation). |
| `INFO` | **Green** | Major milestones (data loaded, training complete, evaluation scores). |
| `WARNING` | **Yellow** | Recoverable issues or fallbacks (e.g. using default split ratio). |
| `ERROR` | **Red** | Failures or exceptions (e.g. unconfigured model type). |
| `CRITICAL` | **Magenta** | Fatal crashes. |

---

## 2. Setting the Log Level

You control the console verbosity with the `--logging-level` command-line flag:

```bash
# Detailed step-by-step diagnostic logs
uv run python -m main --config configs/mvp.yaml --logging-level DEBUG

# Standard progress logs (default)
uv run python -m main --config configs/mvp.yaml --logging-level INFO

# Warnings and errors only
uv run python -m main --config configs/mvp.yaml --logging-level WARNING
```

---

## 3. Persistent File Logs

Every execution creates a timestamped log file in `src/core/logs/`:

```text
src/core/logs/
├── logs_2026_10_14_23_28.log
├── logs_2026_10_15_00_12.log
└── ...
```

Each log line records:
```text
YYYY-MM-DD HH:MM:SS : [LEVEL] : module_name : [function_name] : line_number : message
```

---

## 4. Automatic MLflow Upload

When the run finishes, the `Orchestrator.__exit__` method automatically takes the active log file from `src/core/logs/` and uploads it to MLflow under the `logs/` artifact folder:

```python
self.mlflow_tracker.log_artifact(
    console.handlers[1].baseFilename,
    f"logs/{self.mlflow_tracker.run.info.run_name}.log",
)
```

You can view the full log file directly from the MLflow web UI under the **Artifacts** tab!
