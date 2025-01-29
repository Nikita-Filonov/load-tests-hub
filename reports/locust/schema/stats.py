from typing import Self

from pydantic import Field, FilePath

from base.schema import CSVRootSchema
from reports.locust.schema.metrics.base import LocustStatsMetrics


class LocustStats(LocustStatsMetrics):
    method: str = Field(alias="Name")
    protocol: str = Field(alias="Type")
    min_response_time: float = Field(alias="Min Response Time")
    max_response_time: float = Field(alias="Max Response Time")
    number_of_requests: int = Field(alias="Request Count")
    number_of_failures: int = Field(alias="Failure Count")
    median_response_time: float = Field(alias="Median Response Time")
    average_response_time: float = Field(alias="Average Response Time")
    average_content_length: float = Field(alias="Average Content Size")


class LocustStatsList(CSVRootSchema):
    root: list[LocustStats]

    @property
    def methods(self) -> list[str]:
        return [summary.method for summary in self.root]

    @classmethod
    def from_csv(cls, file: FilePath) -> Self:
        result = super().from_csv(file)
        return cls.model_validate(filter(lambda s: s.method != "Aggregated", result.root))


class LocustStatsAggregatedList(CSVRootSchema):
    root: list[LocustStats]

    @property
    def first(self) -> LocustStats:
        if not self.root:
            raise ValueError("No aggregated stats available. The root list is empty")

        return self.root[0]

    @classmethod
    def from_csv(cls, file: FilePath) -> Self:
        result = super().from_csv(file)
        return cls.model_validate(filter(lambda s: s.method == "Aggregated", result.root))
