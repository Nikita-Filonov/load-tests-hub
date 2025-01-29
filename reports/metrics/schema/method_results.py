from pydantic import BaseModel, Field, ConfigDict

from reports.metrics.schema.metrics.base import MetricsSchema
from reports.metrics.schema.metrics.content_length import ContentLengthSchema


class ShortMethodResult(BaseModel):
    id: int
    method: str


class CreateMethodResult(MetricsSchema, ContentLengthSchema):
    model_config = ConfigDict(populate_by_name=True)

    method: str
    protocol: str
    service_id: int = Field(alias="serviceId")
    scenario_id: int = Field(alias="scenarioId")


class CreateMethodResultsRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    results: list[CreateMethodResult]
    load_test_result_id: int = Field(alias="loadTestResultId")


class CreateMethodResultsResponse(BaseModel):
    results: list[ShortMethodResult]
