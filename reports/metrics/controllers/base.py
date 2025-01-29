from reports.locust.schema.report import LocustReport
from reports.metrics.client import LoadTestingMetricsHTTPClient
from reports.metrics.controllers.exception_results import get_exception_results_payload
from reports.metrics.controllers.load_test_results import get_load_test_result_payload
from reports.metrics.controllers.method_results import get_method_results_payload
from reports.metrics.controllers.ratio_results import get_ratio_result_payload
from reports.metrics.controllers.results_history.load_test_results_history import get_load_test_results_history_payload
from reports.metrics.controllers.results_history.method_results_history import get_method_results_history_payload
from reports.metrics.controllers.scenarios import get_scenario_payload
from reports.metrics.schema.load_test_results import LoadTestResultDetails
from settings import settings


async def send_load_testing_metrics(
        client: LoadTestingMetricsHTTPClient,
        report: LocustReport
) -> LoadTestResultDetails:
    service = settings.metrics.get_service(settings.scenario)
    scenario = service.get_scenario(settings.scenario)

    scenario_payload = get_scenario_payload(report=report, scenario=scenario)
    await client.update_scenario(scenario.id, scenario_payload)

    load_test_result_payload = get_load_test_result_payload(
        report=report,
        service_id=service.id,
        scenario_id=scenario.id
    )
    load_test_result = await client.create_load_test_result(load_test_result_payload)

    method_results_payload = get_method_results_payload(
        report=report,
        service_id=service.id,
        scenario_id=scenario.id,
        load_test_result_id=load_test_result.details.id,
    )
    method_results_response = await client.create_method_results(method_results_payload)

    method_results_history_payload = get_method_results_history_payload(
        report=report,
        method_results=method_results_response.results
    )
    for payload in method_results_history_payload:
        await client.create_method_results_history(payload)

    load_test_results_history_payload = get_load_test_results_history_payload(
        report=report,
        load_test_result_id=load_test_result.details.id,
    )
    await client.create_load_test_results_history(load_test_results_history_payload)

    ratio_result_payload = get_ratio_result_payload(
        report=report,
        load_test_result_id=load_test_result.details.id,
    )
    await client.create_ratio_results(ratio_result_payload)

    exception_results_payload = get_exception_results_payload(
        report=report,
        load_test_result_id=load_test_result.details.id
    )
    await client.create_exception_results(exception_results_payload)

    return load_test_result.details
