from pydantic import BaseModel, ConfigDict, Field

from reports.metrics.schema.ratio_results import RatioResult


class Scenario(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    file: str
    service: str
    ratio_total: list[RatioResult] = Field(alias="ratioTotal")
    ratio_per_class: list[RatioResult] = Field(alias="ratioPerClass")


class CreateScenarioRequest(BaseModel):
    scenario: Scenario
