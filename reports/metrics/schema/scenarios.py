from pydantic import BaseModel, ConfigDict, Field

from reports.metrics.schema.ratio_results import RatioResult


class Scenario(BaseModel):
    id: int


class UpdateScenarioRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    file: str
    version: str
    ratio_total: list[RatioResult] = Field(alias="ratioTotal")
    ratio_per_class: list[RatioResult] = Field(alias="ratioPerClass")
    number_of_users: int = Field(alias="numberOfUsers")
    runtime_duration: str = Field(alias="runtimeDuration")
