from config import settings
from reports.locust.schema import RootLocustSummary, LocustStats
from reports.metrics.client import LoadTestingMetricsHTTPClient
from reports.metrics.schema.history_results import CreateHistoryResultsRequest, HistoryResult
from reports.metrics.schema.load_test_results import CreateLoadTestResultRequest, LoadTestResultDetails
from reports.metrics.schema.method_results import CreateMethodResultsRequest, MethodResult
from reports.metrics.schema.ratio_results import CreateRatioResultRequest, RatioResult
from reports.metrics.schema.scenarios import CreateScenarioRequest, Scenario


def get_load_test_result_payload(
        stats: LocustStats,
        summary: RootLocustSummary
) -> CreateLoadTestResultRequest:
    return CreateLoadTestResultRequest(
        service=settings.scenario.service,
        scenario=settings.scenario.name,
        started_at=stats.start_time,
        finished_at=stats.end_time,
        total_requests=summary.total_requests,
        total_failures=summary.total_failures,
        number_of_users=settings.number_of_users_for_scenario,
        max_response_time=summary.max_response_time,
        min_response_time=summary.min_response_time,
        average_response_time=summary.average_response_time,
        trigger_ci_pipeline_url=settings.trigger_ci_pipeline_url,
        trigger_ci_project_title=settings.trigger_ci_project_title,
        total_failures_per_second=summary.total_failures_per_second,
        total_requests_per_second=summary.total_requests_per_second,
        trigger_ci_project_version=settings.trigger_ci_project_version,
        load_tests_ci_pipeline_url=settings.ci_pipeline_url,
    )


def get_method_results_payload(
        load_test_results_id: int,
        summary: RootLocustSummary
) -> CreateMethodResultsRequest:
    return CreateMethodResultsRequest(
        results=[
            MethodResult(
                method=result.name,
                service=settings.scenario.service,
                scenario=settings.scenario.name,
                protocol=result.method,
                max_response_time=result.max_response_time,
                min_response_time=result.min_response_time,
                number_of_requests=result.num_requests,
                number_of_failures=result.num_failures,
                total_response_time=result.total_response_time,
                requests_per_second=result.requests_per_second,
                failures_per_second=result.failures_per_second,
                average_response_time=result.average_response_time,
            )
            for result in summary.root
        ],
        load_test_result_id=load_test_results_id
    )


def get_history_results_payload(
        load_test_results_id: int,
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
        load_test_result_id=load_test_results_id
    )


def get_ratio_result_payload(load_test_results_id: int, stats: LocustStats) -> CreateRatioResultRequest:
    return CreateRatioResultRequest(
        ratio_total=RatioResult.from_ratio_dict(stats.ratio['total']),
        ratio_per_class=RatioResult.from_ratio_dict(stats.ratio['per_class']),
        load_test_result_id=load_test_results_id
    )


def get_scenario_payload(stats: LocustStats) -> CreateScenarioRequest:
    return CreateScenarioRequest(
        scenario=Scenario(
            name=settings.scenario.name,
            file=settings.scenario.value,
            service=settings.scenario.service,
            ratio_total=RatioResult.from_ratio_dict(stats.ratio['total']),
            ratio_per_class=RatioResult.from_ratio_dict(stats.ratio['per_class']),
        )
    )


async def send_load_testing_metrics(
        client: LoadTestingMetricsHTTPClient,
        stats: LocustStats,
        summary: RootLocustSummary
) -> LoadTestResultDetails:
    scenario_payload = get_scenario_payload(stats=stats)
    await client.create_scenario(scenario_payload)

    load_test_result_payload = get_load_test_result_payload(stats=stats, summary=summary)
    load_test_result = await client.create_load_test_result(load_test_result_payload)

    method_results_payload = get_method_results_payload(
        summary=summary,
        load_test_results_id=load_test_result.details.id,
    )
    await client.create_method_results(method_results_payload)

    history_results_payload = get_history_results_payload(
        stats=stats,
        load_test_results_id=load_test_result.details.id,
    )
    await client.create_history_results(history_results_payload)

    ratio_result_payload = get_ratio_result_payload(
        stats=stats,
        load_test_results_id=load_test_result.details.id,
    )
    await client.create_ratio_results(ratio_result_payload)

    return load_test_result.details
