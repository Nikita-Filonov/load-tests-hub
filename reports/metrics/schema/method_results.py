from pydantic import BaseModel, Field, ConfigDict


class MethodResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    method: str
    service: str
    scenario: str
    protocol: str
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
    number_of_requests: int = Field(alias="numberOfRequests")
    number_of_failures: int = Field(alias="numberOfFailures")
    total_response_time: float = Field(alias="totalResponseTime")
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")


class CreateMethodResultsRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    results: list[MethodResult]
    load_test_result_id: int = Field(alias="loadTestResultId")
