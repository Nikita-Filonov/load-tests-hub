from reports.metrics.schema.metrics.number_of_requests import NumberOfRequestsSchema
from reports.metrics.schema.metrics.percentiles import PercentilesSchema
from reports.metrics.schema.metrics.requests_per_second import RequestsPerSecondSchema
from reports.metrics.schema.metrics.response_times import ResponseTimesSchema


class MetricsSchema(
    PercentilesSchema,
    ResponseTimesSchema,
    NumberOfRequestsSchema,
    RequestsPerSecondSchema,
):
    ...
