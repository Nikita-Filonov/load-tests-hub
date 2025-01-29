from reports.locust.schema.report import LocustReport
from reports.locust.schema.stats_history import LocustStatsHistory
from reports.metrics.controllers.results_history.base import get_results_history_payload
from reports.metrics.schema.method_results import ShortMethodResult
from reports.metrics.schema.results_history.method_results_history import CreateMethodResultsHistoryRequest


def get_method_results_history_payload(
        report: LocustReport,
        method_results: list[ShortMethodResult]
) -> list[CreateMethodResultsHistoryRequest]:
    requests: list[CreateMethodResultsHistoryRequest] = []
    for result in method_results:
        stats = list[LocustStatsHistory](filter(lambda s: s.method == result.method, report.stats_history.root))

        requests.append(
            CreateMethodResultsHistoryRequest(
                results=[get_results_history_payload(history) for history in stats],
                method_result_id=result.id
            )
        )

    return requests
