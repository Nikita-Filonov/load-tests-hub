from datetime import datetime

from pydantic import BaseModel, computed_field

from reports.locust.schema.exceptions import LocustExceptionsList
from reports.locust.schema.ratios import LocustRatios
from reports.locust.schema.stats import LocustStatsList, LocustStatsAggregatedList
from reports.locust.schema.stats_history import LocustStatsHistoryList, LocustStatsHistoryAggregatedList


class LocustReport(BaseModel):
    stats: LocustStatsList
    stats_aggregated: LocustStatsAggregatedList

    stats_history: LocustStatsHistoryList
    stats_history_aggregated: LocustStatsHistoryAggregatedList

    ratios: LocustRatios
    exceptions: LocustExceptionsList

    @computed_field
    @property
    def end_time(self) -> datetime:
        return max(self.stats_history_aggregated.timestamps)

    @computed_field
    @property
    def start_time(self) -> datetime:
        return min(self.stats_history_aggregated.timestamps)
