from pydantic import Field

from reports.metrics.schema.results_history.base import CreateResultsHistoryRequest


class CreateLoadTestResultsHistoryRequest(CreateResultsHistoryRequest):
    load_test_result_id: int = Field(alias="loadTestResultId")
