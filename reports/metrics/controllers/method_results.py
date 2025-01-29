from reports.locust.schema.report import LocustReport
from reports.metrics.schema.method_results import CreateMethodResultsRequest, CreateMethodResult


def get_method_results_payload(
        report: LocustReport,
        service_id: int,
        scenario_id: int,
        load_test_result_id: int,
) -> CreateMethodResultsRequest:
    return CreateMethodResultsRequest(
        results=[
            CreateMethodResult(
                method=result.method,
                protocol=result.protocol,
                service_id=service_id,
                scenario_id=scenario_id,
                max_response_time=result.max_response_time,
                min_response_time=result.min_response_time,
                number_of_requests=result.number_of_requests,
                number_of_failures=result.number_of_failures,
                requests_per_second=result.requests_per_second,
                failures_per_second=result.failures_per_second,
                median_response_time=result.median_response_time,
                average_response_time=result.average_response_time,
                average_content_length=result.average_content_length,
                response_time_percentile_50=result.response_time_percentile_50,
                response_time_percentile_60=result.response_time_percentile_60,
                response_time_percentile_70=result.response_time_percentile_70,
                response_time_percentile_80=result.response_time_percentile_80,
                response_time_percentile_90=result.response_time_percentile_90,
                response_time_percentile_95=result.response_time_percentile_95,
                response_time_percentile_99=result.response_time_percentile_99,
                response_time_percentile_100=result.response_time_percentile_100
            )
            for result in report.stats.root
        ],
        load_test_result_id=load_test_result_id
    )
