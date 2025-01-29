from reports.locust.schema.report import LocustReport
from reports.metrics.schema.exception_results import CreateExceptionResultsRequest, ExceptionResult


def get_exception_results_payload(
        load_test_result_id: int,
        report: LocustReport
) -> CreateExceptionResultsRequest:
    return CreateExceptionResultsRequest(
        results=[
            ExceptionResult(
                message=exception.message,
                details=exception.traceback,
                number_of_exceptions=exception.count,
            )
            for exception in report.exceptions.root
        ],
        load_test_result_id=load_test_result_id
    )
