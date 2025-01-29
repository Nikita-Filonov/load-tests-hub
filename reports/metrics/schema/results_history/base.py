from datetime import datetime

from pydantic import BaseModel, ConfigDict

from reports.metrics.schema.metrics.base import MetricsSchema
from reports.metrics.schema.metrics.content_length import ContentLengthSchema
from reports.metrics.schema.metrics.number_of_users import NumberOfUsersSchema


class ResultsHistory(MetricsSchema, ContentLengthSchema, NumberOfUsersSchema):
    datetime: datetime


class CreateResultsHistoryRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    results: list[ResultsHistory]
