from datetime import datetime, timezone

from locust.env import Environment
from locust.runners import STATE_STOPPED, STATE_STOPPING, MasterRunner
from locust.user.inspectuser import get_ratio

from config import settings
from reports.locust.schema import RootLocustSummary, LocustStats, LocustStatsRatioDict


def get_locust_report_stats() -> LocustStats:
    summary = settings.json_stats_report_file.read_text()
    return LocustStats.model_validate_json(summary)


def dump_locust_report_stats(environment: Environment) -> LocustStats:
    stats = environment.stats

    start_time = datetime.fromtimestamp(stats.start_time, timezone.utc)
    end_time = start_time

    if end_ts := stats.last_request_timestamp:
        end_time = datetime.fromtimestamp(end_ts, timezone.utc)

    user_spawned = (
        environment.runner.reported_user_classes_count
        if isinstance(environment.runner, MasterRunner)
        else environment.runner.user_classes_count
    )

    if environment.runner.state in [STATE_STOPPED, STATE_STOPPING]:
        user_spawned = environment.runner.final_user_classes_count

    stats = LocustStats(
        start_time=start_time,
        end_time=end_time,
        history=stats.history,
        ratio=LocustStatsRatioDict(
            total=get_ratio(environment.user_classes, user_spawned, True),
            per_class=get_ratio(environment.user_classes, user_spawned, False)
        )
    )

    settings.json_stats_report_file.write_text(data=stats.model_dump_json(by_alias=True))

    return stats


def get_locust_report_summary() -> RootLocustSummary:
    summary = settings.json_summary_report_file.read_text()
    return RootLocustSummary.model_validate_json(summary)
