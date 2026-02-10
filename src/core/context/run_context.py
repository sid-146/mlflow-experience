from typing import Literal

from pydantic import BaseModel, field_validator, errors

from src.core.constants.file_types import FILE_TYPES


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


class SourceContext(BaseModel):
    type: FILE_TYPES
    path: str


class DataContext(BaseModel):
    name: str
    source: SourceContext


class ExperimentContext(BaseModel):
    objective: str
    # baseline_run_id:str
    # promoted_from_experiment: bool
    notes: str


class HandleMissingValues(BaseModel):
    

class PreprocessingContext(BaseModel):
    missing_values: 

class RunContext(BaseModel):
    project: ProjectContext
