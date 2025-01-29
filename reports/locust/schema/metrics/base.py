from reports.locust.schema.metrics.percentiles import LocustStatsPercentiles
from reports.locust.schema.metrics.requests_per_second import LocustStatsRequestsPerSecond


class LocustStatsMetrics(LocustStatsPercentiles, LocustStatsRequestsPerSecond):
    ...
