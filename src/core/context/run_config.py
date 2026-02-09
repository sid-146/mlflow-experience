from typing import Literal

from pydantic import BaseModel, field_validator, errors


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


class RunContext(BaseModel):
    project: ProjectContext
