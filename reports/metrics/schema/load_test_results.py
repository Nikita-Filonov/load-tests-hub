from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateLoadTestResultRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    service: str
    scenario: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_title: str | None = Field(alias="triggerCIProjectTitle")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures: int = Field(alias="totalFailures")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")


class LoadTestResultCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_total_requests_per_second: float = Field(alias="currentTotalRequestsPerSecond")
    average_total_requests_per_second: float = Field(alias="averageTotalRequestsPerSecond")
    previous_total_requests_per_second: float = Field(alias="previousTotalRequestsPerSecond")
    total_requests_per_second_compare_with_average: float = Field(
        alias="totalRequestsPerSecondCompareWithAverage"
    )
    total_requests_per_second_compare_with_previous: float = Field(
        alias="totalRequestsPerSecondCompareWithPrevious"
    )


class LoadTestResultDetails(BaseModel):
    id: int
    service: str
    scenario: str
    
    compare: LoadTestResultCompare | None = None


class CreateLoadTestResultResponse(BaseModel):
    details: LoadTestResultDetails
