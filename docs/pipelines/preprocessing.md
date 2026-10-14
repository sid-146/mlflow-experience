# Preprocessing Engine

The `PreprocessingPipeline` (`src.core.pipelines.preprocessing`) compiles the declarative list of preprocessing steps into Scikit-Learn transformer instances.

---

## Assembly Logic

When `preprocessor.build()` is invoked by the `Orchestrator`:

1. It iterates through each `PreprocessingContext` in `context.preprocessing`.
2. Looks up the matching transformer class via `step.type.transformer_class` in `PreprocessingRegistry`.
3. Dynamically instantiates the transformer with its strongly-typed policy parameters:

```python
def _instantiate_transformer(self, transformer_class, params):
    if hasattr(params, "mapping"):  # RenamePolicy
        return transformer_class(mapping=params.mapping)
    elif hasattr(params, "columns"):  # MissingValuePolicy, EncodingPolicy, ScalingPolicy
        return transformer_class(params=params)
    else:
        try:
            return transformer_class(**params.dict())
        except (AttributeError, TypeError):
            return transformer_class(**params) if isinstance(params, dict) else transformer_class()
```

4. Appends a tuple of `(step.name, transformer_instance)` to `self.steps`.
5. Returns the completed list of steps to be included in the Scikit-Learn `Pipeline`.

---

## Registry Mapping

The `PreprocessingRegistry` enum maps YAML identifiers to their transformer implementations:

| YAML `type` | Enum Member | Policy Class | Transformer Class |
| :--- | :--- | :--- | :--- |
| `rename` | `rename_columns` | `RenamePolicy` | `RenameColumnsTransformer` |
| `type_cast` | `type_cast` | `TypeCastPolicy` | Custom Type Cast logic |
| `missing` | `missing_values` | `MissingValuePolicy` | `MissingValueTransformer` |
| `encoding` | `encoding` | `EncodingPolicy` | `EncodingTransformer` |
| `scaling` | `scaling` | `ScalingPolicy` | `ScalingTransformer` |
| `cleaning` | `cleaning` | — | `CleaningTransformer` |
| `filter` | `filter` | — | `FilterTransformer` |
