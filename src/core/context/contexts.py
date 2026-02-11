from typing import Literal, Dict, Union, List

from pydantic import BaseModel, field_validator, errors, model_validator

from src.core.context.policies import (
    SourcePolicy,
    SchemaPolicy,
    TypeCastPolicy,
    MissingValuePolicy,
    FilterPolicy,
    OutliersPolicy,
)
from src.core.constants.constants import (
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


class CleaningContext(BaseModel):
    trim_string: bool
    lowercase: bool
    categorical: Dict[str, Dict[str, str]]
    numeric: Dict[str, Dict[Union[str, int, float], Union[str, int, float]]]


class PreprocessingContext(BaseModel):
    schema: SchemaPolicy
    type_cast: Dict[str, TypeCastPolicy]
    missing_values: Dict[str, MissingValuePolicy]
    cleaning: CleaningContext
    filter: Dict[str, FilterPolicy]
    outliers: Dict[str, OutliersPolicy]
    categorical: Dict[
        str, Dict[str, Dict[str, Union[str, List[str]]]]
    ]  # Todo: Fixed this


# ############## Run Context ##################
class RunContext(BaseModel):
    project: ProjectContext
    data: DataContext
    experiment: ExperimentContext
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
