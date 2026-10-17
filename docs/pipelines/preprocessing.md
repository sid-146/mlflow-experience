# Preprocessing Pipeline

The `PreprocessingPipeline` class (`src/core/pipelines/preprocessing.py`) turns the list of steps in your YAML file into executable Scikit-Learn transformer instances.

---

## How It Works

1. The `Orchestrator` calls `preprocessor.build()`.
2. It loops over every step defined in your `preprocessing` YAML list.
3. For each step, it looks up the matching transformer class in `PreprocessingRegistry`.
4. It instantiates the transformer with the validated parameters.
5. It returns a list of `(name, transformer_instance)` tuples ready to be passed to Scikit-Learn's `Pipeline`:

```python
[
    ("rename_columns", RenameColumnsTransformer(...)),
    ("handle_missing", MissingValueTransformer(...)),
    ("encode_features", EncodingTransformer(...)),
    ("scale_features", ScalingTransformer(...)),
]
```

---

## The Registry Mapping

`PreprocessingRegistry` connects the string `type` in your YAML to the Python class:

| YAML `type` | Transformer Class | Policy Model |
| :--- | :--- | :--- |
| `rename` | `RenameColumnsTransformer` | `RenamePolicy` |
| `missing` | `MissingValueTransformer` | `MissingValuePolicy` |
| `encoding` | `EncodingTransformer` | `EncodingPolicy` |
| `scaling` | `ScalingTransformer` | `ScalingPolicy` |
| `cleaning` | `CleaningTransformer` | *(dict of replacements)* |
| `filter` | `FilterTransformer` | *(query condition string)* |

---

## Order of Execution

Steps execute in the exact order you define them in YAML. For example:

1. **Rename first**: Standardize column names (e.g. `"Total Spend"` $\to$ `total_spend`).
2. **Handle missing values**: Impute null values with mean, median, mode, or constant.
3. **Encode categories**: Convert string categories into numbers.
4. **Scale numeric features**: Apply standard scaling or min-max normalization.

!!! warning "Column Name Dependencies"
    If you rename a column in step 1, remember to use the **new** name in subsequent steps (such as imputation, encoding, and scaling)!
