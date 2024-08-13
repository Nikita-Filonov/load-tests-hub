from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HistoryResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    datetime: datetime
    number_of_users: int = Field(alias="numberOfUsers")
    requests_per_second: float = Field(alias="requestsPerSecond")
    failures_per_second: float = Field(alias="failuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    response_time_percentile_95: float = Field(alias="responseTimePercentile95")


class CreateHistoryResultsRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    results: list[HistoryResult]
    load_test_result_id: int = Field(alias="loadTestResultId")
