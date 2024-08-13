from datetime import datetime

from pydantic import BaseModel, RootModel, Field
from typing_extensions import TypedDict


class LocustSummary(BaseModel):
    name: str
    method: str
    start_time: float
    num_requests: int
    num_failures: int
    response_times: dict[str, int]
    num_reqs_per_sec: dict[str, int]
    num_fail_per_sec: dict[str, int]
    num_none_requests: int
    max_response_time: float
    min_response_time: float
    total_response_time: float
    last_request_timestamp: float

    @property
    def requests_per_second(self) -> float:
        if len(self.num_reqs_per_sec) == 0:
            return 0

        return self.num_requests / len(self.num_reqs_per_sec)

    @property
    def failures_per_second(self) -> float:
        if len(self.num_fail_per_sec) == 0:
            return 0

        return self.num_failures / len(self.num_fail_per_sec)

    @property
    def average_response_time(self) -> float:
        return self.total_response_time / self.num_requests


class RootLocustSummary(RootModel):
    root: list[LocustSummary]

    @property
    def methods(self) -> list[str]:
        return [summary.name for summary in self.root]

    @property
    def total_requests(self) -> int:
        return sum(summary.num_requests for summary in self.root)

    @property
    def total_failures(self) -> int:
        return sum(summary.num_failures for summary in self.root)

    @property
    def max_response_time(self) -> float:
        return max(summary.max_response_time for summary in self.root)

    @property
    def min_response_time(self) -> float:
        return max(summary.min_response_time for summary in self.root)

    @property
    def average_response_time(self) -> float:
        return sum(summary.average_response_time for summary in self.root) / len(self.root)

    @property
    def total_requests_per_second(self) -> float:
        return sum(summary.requests_per_second for summary in self.root)

    @property
    def total_failures_per_second(self) -> float:
        return sum(summary.failures_per_second for summary in self.root)


class LocustHistory(BaseModel):
    time: datetime
    user_count: int
    current_rps: float
    current_fail_per_sec: float
    total_avg_response_time: float
    response_time_percentile_95: float = Field(alias="response_time_percentile_0.95")


class LocustStatsRatioDict(TypedDict):
    total: dict
    per_class: dict


class LocustStats(BaseModel):
    start_time: datetime
    end_time: datetime
    history: list[LocustHistory]
    ratio: LocustStatsRatioDict
