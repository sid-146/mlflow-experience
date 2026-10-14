# Dual Logging Subsystem

The logging architecture (`src.core.logging.logger`) provides dual-stream observability: real-time ANSI-colorized terminal logs and persistent timestamped log files.

---

## 1. Handlers & Formats

The module initializes two handlers:

```python
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(filepath, mode="a")
```

### Colorized Console Formatting
A custom `ColoredFormatter` maps log levels to ANSI color escapes:
- `DEBUG`: Blue (`\033[94m`)
- `INFO`: Green (`\033[92m`)
- `WARNING`: Yellow (`\033[93m`)
- `ERROR`: Red (`\033[91m`)
- `CRITICAL`: Magenta (`\033[95m`)

### Timestamped File Logging
Log files are created under `src/core/logs/` with timestamps:
```text
logs_YYYY_MM_DD_HH_MM.log
```

---

## 2. Automatic Artifact Upload

When the pipeline finishes, the `Orchestrator.__exit__` method retrieves the path of the active file handler and uploads it to MLflow as a run artifact:

```python
def __exit__(self, exc_type, exc, tb):
    self.mlflow_tracker.log_artifact(
        console.handlers[1].baseFilename,
        f"logs/{self.mlflow_tracker.run.info.run_name}.log",
    )
```

This guarantees an unbroken audit trail for every experiment run.
