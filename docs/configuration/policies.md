# Pydantic Validation & Policies

The configuration layer in `mlflow-experience` does not merely pass raw dictionaries to code; it relies on **Pydantic v2** models (`src.core.context.policies` and `src.core.context.contexts`) to guarantee type correctness, check constraints, and cast step parameters.

---

## The Dynamic Casting Mechanism

When the root context is initialized:

```python
class PreprocessingContext(BaseModel):
    name: str
    type: PreprocessingRegistry
    params: Any = Field(default_factory=dict)

    def cast_params(self):
        policy_class = self.type.policy_class
        if policy_class is not None:
            self.params = policy_class(**self.params)
        return self
```

During validation, the `RunContext` executes `cast_all_preprocessing_params()`, converting raw dictionary trees into strongly-typed policy objects.

---

## Policy Classes

### `RenamePolicy`
Enforces that column mappings are non-empty:
```python
class RenamePolicy(BaseModel):
    mapping: Dict[str, str]

    @field_validator("mapping")
    def validate_mapping(cls, v):
        if not v:
            raise ValueError("Rename mapping cannot be empty")
        return v
```

---

### `TypeCastPolicy`
Specifies data types and optional date formats:
```python
class TypeCastConfig(BaseModel):
    name: str
    dtype: str
    format: Optional[str] = None

class TypeCastPolicy(BaseModel):
    columns: List[TypeCastConfig]
```

---

### `MissingValuePolicy`
Constrains imputation strategies to supported values:
```python
class MissingValueConfig(BaseModel):
    name: str
    strategy: Literal["mean", "median", "mode", "constant"]
    fill_value: Optional[Any] = None

class MissingValuePolicy(BaseModel):
    columns: List[MissingValueConfig]
```

---

### `EncodingPolicy`
Governs categorical transformations and ordinal rank ordering:
```python
class EncodingConfig(BaseModel):
    name: str
    strategy: Literal["one_hot", "label", "target", "ordinal"]
    order: Optional[List[str]] = None

class EncodingPolicy(BaseModel):
    columns: List[EncodingConfig]
```

---

### `ScalingPolicy`
Governs numerical feature transformations:
```python
class ScalingConfig(BaseModel):
    name: str
    strategy: Literal["standard", "minmax", "robust"]
    params: Optional[Dict[str, Any]] = None

class ScalingPolicy(BaseModel):
    columns: List[ScalingConfig]
```
