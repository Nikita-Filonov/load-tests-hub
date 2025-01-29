from reports.locust.schema.exceptions import LocustExceptionsList
from reports.locust.schema.ratios import LocustRatios
from reports.locust.schema.report import LocustReport
from reports.locust.schema.stats import LocustStatsList, LocustStatsAggregatedList
from reports.locust.schema.stats_history import LocustStatsHistoryList, LocustStatsHistoryAggregatedList
from settings import settings


def get_locust_report() -> LocustReport:
    return LocustReport(
        stats=LocustStatsList.from_csv(settings.reports.csv_locust_stats_file),
        stats_aggregated=LocustStatsAggregatedList.from_csv(settings.reports.csv_locust_stats_file),

        stats_history=LocustStatsHistoryList.from_csv(settings.reports.csv_locust_stats_history_file),
        stats_history_aggregated=LocustStatsHistoryAggregatedList.from_csv(
            settings.reports.csv_locust_stats_history_file
        ),

        ratios=LocustRatios.from_json(settings.reports.json_locust_ratio_file),
        exceptions=LocustExceptionsList.from_csv(settings.reports.csv_locust_exceptions_file),
    )
