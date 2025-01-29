from pydantic import Field

from reports.metrics.schema.results_history.base import CreateResultsHistoryRequest


class CreateMethodResultsHistoryRequest(CreateResultsHistoryRequest):
    method_result_id: int = Field(alias="methodResultId")
