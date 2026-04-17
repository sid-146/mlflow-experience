from enum import Enum
from typing import List, Dict, Optional, Any

from pydantic import BaseModel, Field, model_validator

from src.core.constants.registry import PreprocessingType
from src.core.context.policies import (
    DatasetPolicy,
    ScalingPolicy,
    EncodingPolicy,
    MissingValuePolicy,
    TypeCastPolicy,
    RenamePolicy,
)


# ==============================
# ENUMS (Optional but recommended)
# Todo: Move to registry
# ==============================
class ModelType(str, Enum):
    logistic_regression = "logistic_regression"
    random_forest = "random_forest"


class MissingValueStrategy(str, Enum):
    mean = "mean"
    median = "median"
    most_frequent = "most_frequent"


class EncodingStrategy(str, Enum):
    one_hot = "one_hot"
    label = "label"


class ScalingStrategy(str, Enum):
    standard = "standard"
    minmax = "minmax"


# ==============================
# PROJECT
# ==============================
class ProjectContext(BaseModel):
    name: str
    owner: str
    environment: str
    description: Optional[str] = None


# ==============================
# MLFLOW
# ==============================
class MlFlowContext(BaseModel):
    experiment_name: str
    experiment_id: Optional[str] = None
    # Todo: This is needed as not able to set backend uri in mlflow server command in compose.yaml
    # need to find solution
    tracking_uri: Optional[str] = None
    track_params: bool = True
    track_metrics: bool = True
    track_artifacts: List[str] = []
    tags: Dict[str, str] = {}


# ==============================
# Dataset Context
# ==============================
class DataContext(BaseModel):
    dataset_name: str
    random_state: int = Field(..., ge=0)
    train_test_split: Optional[float] = None

    train: DatasetPolicy
    test: Optional[DatasetPolicy] = None


# ==============================
# PREPROCESSING
# ==============================
class PreprocessingContext(BaseModel):
    name: str
    type: str
    params: Any = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def cast_params(self):
        """
        Convert raw params into typed models based on type
        """
        model = getattr(PreprocessingType, self.type, None)
        if model is None:
            raise ValueError(f"Unsupported preprocessing type: {self.type}")

        self.params = model(**self.params)
        return self


# ==============================
# FEATURES
# ==============================
class FeatureContext(BaseModel):
    scaling: Optional[ScalingStrategy] = None


# ==============================
# MODEL
# ==============================
class ModelContext(BaseModel):
    type: ModelType
    hyperparameters: Dict[str, Any] = {}


# ==============================
# TRAINING
# ==============================
class TrainingContext(BaseModel):
    objective: str


# ==============================
# EVALUATION
# ==============================
class EvaluationContext(BaseModel):
    metrics: List[str]


# ==============================
# ROOT CONTEXT
# ==============================
class RunContext(BaseModel):
    project: ProjectContext
    mlflow: MlFlowContext
    dataset: DataContext
    preprocessing: List[PreprocessingContext]
    features: FeatureContext
    model: ModelContext
    training: TrainingContext
    evaluation: EvaluationContext

    @classmethod
    def from_yaml_dict(cls, config: dict) -> "RunContext":
        """
        Entry point for converting YAML → strongly typed config
        """
        return cls.model_validate(config)

    @model_validator(mode="after")
    def cast_all_preprocessing_params(self):
        for step in self.preprocessing:
            step.cast_params()
        return self
