from enum import Enum
from typing import List, Dict, Optional, Any

from pydantic import BaseModel, Field

from src.core.context.policies import DatasetPolicy


# ==============================
# ENUMS (Optional but recommended)
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
    track_params: bool = True
    track_metrics: bool = True
    track_artifacts: List[str] = []
    tags: Dict[str, str] = {}


# ==============================
# DATA
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
    missing_values: Optional[MissingValueStrategy] = None
    categorical_encoding: Optional[EncodingStrategy] = None


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
    preprocessing: PreprocessingContext
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
