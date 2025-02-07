from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from reports.metrics.schema.metrics.base import MetricsSchema
from reports.metrics.schema.metrics.number_of_users import NumberOfUsersSchema
from reports.metrics.schema.scenarios import Scenario
from reports.metrics.schema.services import Service


class CreateLoadTestResultRequest(MetricsSchema, NumberOfUsersSchema):
    model_config = ConfigDict(populate_by_name=True)

    service_id: int = Field(alias="serviceId")
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    scenario_id: int = Field(alias="scenarioId")
    trigger_ci_job_url: str | None = Field(alias="triggerCIJobUrl")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_job_url: str | None = Field(alias="loadTestsCIJobUrl")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")


class LoadTestResultCompare(BaseModel):
    percent: float = Field(alias="compare")
    highlight: bool


class LoadTestResultSummaryCompare(BaseModel):
    compare_with_average: LoadTestResultCompare = Field(alias="compareWithAverage")
    compare_with_previous: LoadTestResultCompare = Field(alias="compareWithPrevious")


class LoadTestResultDetails(BaseModel):
    id: int

    compare: LoadTestResultSummaryCompare | None = None
    service: Service
    scenario: Scenario


class CreateLoadTestResultResponse(BaseModel):
    details: LoadTestResultDetails
