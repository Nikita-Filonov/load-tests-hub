from config.metrics import ScenarioConfig
from reports.locust.schema.report import LocustReport
from reports.metrics.schema.ratio_results import RatioResult
from reports.metrics.schema.scenarios import UpdateScenarioRequest
from settings import settings


def get_scenario_payload(report: LocustReport, scenario: ScenarioConfig) -> UpdateScenarioRequest:
    return UpdateScenarioRequest(
        name=settings.scenario.scenario_normalized,
        file=settings.scenario.value,
        version=settings.scenario.version,
        ratio_total=RatioResult.from_locust_ratio(report.ratios.total),
        ratio_per_class=RatioResult.from_locust_ratio(report.ratios.per_class),
        number_of_users=scenario.number_of_users,
        runtime_duration=scenario.runtime_duration
    )
