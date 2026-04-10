from typing import Literal

from pydantic import BaseModel, field_validator, errors, model_validator

from core.context.policies import (
    CategoricalMissingPolicy,
    NumericMissingPolicy,
    SourcePolicy,
)
from core.constants.constants import (
    FILE_TYPES,
    CATEGORICAL_MISSING_STRATEGY,
    NUMERIC_MISSING_STRATEGY,
)


class ProjectContext(BaseModel):
    name: str
    owner: str
    env: Literal["prod", "dev", "test"]

    @field_validator("env", mode="before")
    def check_env(value: str) -> str:
        if "prod" in value.lower():
            return "prod"
        elif "dev" in value.lower():
            return "dev"
        elif "test" in value.lower():
            return "test"
        else:
            raise errors.PydanticUserError(
                "Invalid value passed. It should 'prod', 'dev' or 'test'."
            )


class DataContext(BaseModel):
    name: str
    source: SourcePolicy


class ExperimentContext(BaseModel):
    objective: str
    # baseline_run_id:str
    # promoted_from_experiment: bool
    notes: str


class HandleMissingValues(BaseModel):
    numeric: NumericMissingPolicy
    categorical: CategoricalMissingPolicy


class PreprocessingContext(BaseModel):
    missing_values: HandleMissingValues


class MlFlowContext(BaseModel):
    experiment_name: str
    experiment_id: str


class RunContext(BaseModel):
    project: ProjectContext
    data: DataContext
    experiment: ExperimentContext
    mlflow: MlFlowContext
    # preprocessing: PreprocessingContext

    @classmethod
    def populate(cls, config):
        obj = cls(
            project=ProjectContext(
                name=config["project"]["name"],
                owner=config["project"]["owner"],
                env=config["project"]["environment"],
            ),
            data=DataContext(
                name=config["data"]["dataset_name"],
                source=SourcePolicy(
                    type=config["data"]["source"]["type"],
                    path=config["data"]["source"]["path"],
                ),
            ),
            experiment=ExperimentContext(
                objective=config["experiment"]["objective"],
                notes=config["experiment"]["notes"],
            ),
        )
        return obj
