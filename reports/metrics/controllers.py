from config import settings
from reports.locust.schema import RootLocustSummary, LocustStats
from reports.metrics.client import LoadTestingMetricsHTTPClient
from reports.metrics.schema.exception_results import CreateExceptionResultsRequest, ExceptionResult
from reports.metrics.schema.history_results import CreateHistoryResultsRequest, HistoryResult
from reports.metrics.schema.load_test_results import CreateLoadTestResultRequest, LoadTestResultDetails
from reports.metrics.schema.method_results import CreateMethodResultsRequest, MethodResult
from reports.metrics.schema.ratio_results import CreateRatioResultRequest, RatioResult
from reports.metrics.schema.scenarios import UpdateScenarioRequest


def get_load_test_result_payload(
        stats: LocustStats,
        summary: RootLocustSummary,
        service_id: int,
        scenario_id: int,
) -> CreateLoadTestResultRequest:
    return CreateLoadTestResultRequest(
        service_id=service_id,
        started_at=stats.start_time,
        finished_at=stats.end_time,
        scenario_id=scenario_id,
        total_requests=summary.total_requests,
        total_failures=summary.total_failures,
        number_of_users=settings.number_of_users_for_scenario,
        max_response_time=summary.max_response_time,
        min_response_time=summary.min_response_time,
        trigger_ci_job_url=settings.trigger_ci_job_url,
        load_tests_ci_job_url=settings.ci_job_url,
        average_response_time=summary.average_response_time,
        trigger_ci_pipeline_url=settings.trigger_ci_pipeline_url,
        total_failures_per_second=summary.total_failures_per_second,
        total_requests_per_second=summary.total_requests_per_second,
        trigger_ci_project_version=settings.trigger_ci_project_version,
        load_tests_ci_pipeline_url=settings.ci_pipeline_url,
    )


def get_method_results_payload(
        summary: RootLocustSummary,
        service_id: int,
        scenario_id: int,
        load_test_result_id: int,
) -> CreateMethodResultsRequest:
    return CreateMethodResultsRequest(
        results=[
            MethodResult(
                method=result.name,
                protocol=result.method,
                service_id=service_id,
                scenario_id=scenario_id,
                max_response_time=result.max_response_time,
                min_response_time=result.min_response_time,
                number_of_requests=result.num_requests,
                number_of_failures=result.num_failures,
                total_response_time=result.total_response_time,
                requests_per_second=result.requests_per_second,
                failures_per_second=result.failures_per_second,
                average_response_time=result.average_response_time,
                average_content_length=result.average_content_length
            )
            for result in summary.root
        ],
        load_test_result_id=load_test_result_id
    )


def get_history_results_payload(
        load_test_result_id: int,
        stats: LocustStats,
) -> CreateHistoryResultsRequest:
    return CreateHistoryResultsRequest(
        results=[
            HistoryResult(
                datetime=history.time,
                number_of_users=history.user_count,
                requests_per_second=history.current_rps,
                failures_per_second=history.current_fail_per_sec,
                average_response_time=history.total_avg_response_time,
                response_time_percentile_95=history.response_time_percentile_95
            )
            for history in stats.history
        ],
        load_test_result_id=load_test_result_id
    )


def get_ratio_result_payload(load_test_result_id: int, stats: LocustStats) -> CreateRatioResultRequest:
    return CreateRatioResultRequest(
        ratio_total=RatioResult.from_ratio_dict(stats.ratio['total']),
        ratio_per_class=RatioResult.from_ratio_dict(stats.ratio['per_class']),
        load_test_result_id=load_test_result_id
    )


def get_exception_results_payload(
        load_test_result_id: int,
        stats: LocustStats
) -> CreateExceptionResultsRequest:
    return CreateExceptionResultsRequest(
        results=[
            ExceptionResult(
                message=exception.message,
                details=exception.traceback,
                number_of_exceptions=exception.count,
            )
            for exception in stats.exceptions
        ],
        load_test_result_id=load_test_result_id
    )


def get_scenario_payload(stats: LocustStats) -> UpdateScenarioRequest:
    return UpdateScenarioRequest(
        name=settings.scenario.scenario_normalized,
        file=settings.scenario.value,
        version=settings.scenario.version,
        ratio_total=RatioResult.from_ratio_dict(stats.ratio['total']),
        ratio_per_class=RatioResult.from_ratio_dict(stats.ratio['per_class']),
    )


async def send_load_testing_metrics(
        client: LoadTestingMetricsHTTPClient,
        stats: LocustStats,
        summary: RootLocustSummary
) -> LoadTestResultDetails:
    service = settings.metrics.get_service(settings.scenario)
    scenario = service.get_scenario(settings.scenario)

    scenario_payload = get_scenario_payload(stats=stats)
    await client.update_scenario(scenario.id, scenario_payload)

    load_test_result_payload = get_load_test_result_payload(
        stats=stats,
        summary=summary,
        service_id=service.id,
        scenario_id=scenario.id
    )
    load_test_result = await client.create_load_test_result(load_test_result_payload)

    method_results_payload = get_method_results_payload(
        summary=summary,
        service_id=service.id,
        scenario_id=scenario.id,
        load_test_result_id=load_test_result.details.id,
    )
    await client.create_method_results(method_results_payload)

    history_results_payload = get_history_results_payload(
        stats=stats,
        load_test_result_id=load_test_result.details.id,
    )
    await client.create_history_results(history_results_payload)

    ratio_result_payload = get_ratio_result_payload(
        stats=stats,
        load_test_result_id=load_test_result.details.id,
    )
    await client.create_ratio_results(ratio_result_payload)

    exception_results_payload = get_exception_results_payload(
        stats=stats,
        load_test_result_id=load_test_result.details.id
    )
    await client.create_exception_results(exception_results_payload)

    return load_test_result.details
