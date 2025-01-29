from reports.locust.schema.report import LocustReport
from reports.metrics.controllers.results_history.base import get_results_history_payload
from reports.metrics.schema.results_history.load_test_results_history import CreateLoadTestResultsHistoryRequest


def get_load_test_results_history_payload(
        load_test_result_id: int,
        report: LocustReport
) -> CreateLoadTestResultsHistoryRequest:
    return CreateLoadTestResultsHistoryRequest(
        results=[
            get_results_history_payload(history)
            for history in report.stats_history_aggregated.root
        ],
        load_test_result_id=load_test_result_id
    )
