# Pydantic Policies & Validation

To make development reliable and prevent silent runtime crashes, `mlflow-experience` validates all configuration settings using **Pydantic v2** (`src/core/context/contexts.py` and `src/core/context/policies.py`).

---

## Why Use Pydantic?

In traditional ML projects with YAML files, a simple typo (such as `strategy: meaan` or omitting a required column) would only fail deep inside Scikit-Learn code after 10 minutes of execution.

With Pydantic:
- **Instant Failure**: Your configuration is checked before any data is loaded or processed.
- **Helpful Error Messages**: It tells you the exact line, field name, and expected values if something is wrong.
- **Automatic Type Conversion**: String numbers are parsed into integers or floats automatically where appropriate.

---

## How It Works

When `main.py` runs, it calls:

```python
context = RunContext.from_yaml_dict(config)
```

1. Pydantic parses the dictionary against `RunContext`.
2. A model validator (`cast_all_preprocessing_params`) checks each step in `preprocessing`.
3. The step's `type` looks up the corresponding policy class from `PreprocessingRegistry.policy_class`.
4. The dictionary is instantiated into a strongly-typed policy object (e.g. `MissingValuePolicy`, `ScalingPolicy`, `EncodingPolicy`).

---

## Policy Reference

### `RenamePolicy`
Validates column rename mappings:
- `mapping` (*dict[str, str]*): Must not be empty.

### `MissingValuePolicy`
Validates missing value strategies:
- `strategy`: Must be one of `"mean"`, `"median"`, `"mode"`, or `"constant"`.
- `fill_value`: Required if `strategy: constant`.

### `EncodingPolicy`
Validates encoding configurations:
- `strategy`: Must be one of `"one_hot"`, `"ordinal"`, `"label"`, or `"target"`.
- `order`: A list of strings specifying the exact order for ordinal encoding (e.g. `['Low', 'Medium', 'High']`).

### `ScalingPolicy`
Validates scaling strategies:
- `strategy`: Must be one of `"standard"`, `"minmax"`, or `"robust"`.

---

## Example Error Output

If you provide an invalid strategy in your YAML:

```yaml
- name: bad_step
  type: missing
  params:
    columns:
      - name: age
        strategy: invalid_strategy
```

Pydantic immediately catches it:

```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for MissingValueConfig
strategy
  Input should be 'mean', 'median', 'mode' or 'constant' [type=literal_error, input_value='invalid_strategy', input_type=str]
```
