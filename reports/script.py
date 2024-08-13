import asyncio

from reports.locust.controllers import get_locust_report_summary, get_locust_report_stats
from reports.metrics.client import get_load_testing_metrics_http_client
from reports.metrics.controllers import send_load_testing_metrics


async def main():
    stats = get_locust_report_stats()
    summary = get_locust_report_summary()

    load_testing_metrics_client = get_load_testing_metrics_http_client()

    await send_load_testing_metrics(load_testing_metrics_client, stats, summary)


if __name__ == '__main__':
    asyncio.run(main())
