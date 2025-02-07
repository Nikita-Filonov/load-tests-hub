from reports.locust.schema.report import LocustReport
from reports.metrics.schema.load_test_results import CreateLoadTestResultRequest
from settings import settings


def get_load_test_result_payload(
        report: LocustReport,
        service_id: int,
        scenario_id: int,
) -> CreateLoadTestResultRequest:
    stats = report.stats_aggregated.first

    return CreateLoadTestResultRequest(
        service_id=service_id,
        started_at=report.start_time,
        finished_at=report.end_time,
        scenario_id=scenario_id,
        number_of_users=settings.seeders.number_of_users,
        max_response_time=stats.max_response_time,
        min_response_time=stats.min_response_time,
        number_of_requests=stats.number_of_requests,
        number_of_failures=stats.number_of_failures,
        trigger_ci_job_url=settings.trigger_pipeline.ci_job_url,
        failures_per_second=stats.failures_per_second,
        requests_per_second=stats.requests_per_second,
        median_response_time=stats.median_response_time,
        load_tests_ci_job_url=settings.load_tests_pipeline.ci_job_url,
        average_response_time=stats.average_response_time,
        trigger_ci_pipeline_url=settings.trigger_pipeline.ci_pipeline_url,
        trigger_ci_project_version=settings.trigger_pipeline.ci_project_version,
        load_tests_ci_pipeline_url=settings.load_tests_pipeline.ci_pipeline_url,
        response_time_percentile_50=stats.response_time_percentile_50,
        response_time_percentile_60=stats.response_time_percentile_60,
        response_time_percentile_70=stats.response_time_percentile_70,
        response_time_percentile_80=stats.response_time_percentile_80,
        response_time_percentile_90=stats.response_time_percentile_90,
        response_time_percentile_95=stats.response_time_percentile_95,
        response_time_percentile_99=stats.response_time_percentile_99,
        response_time_percentile_100=stats.response_time_percentile_100
    )
