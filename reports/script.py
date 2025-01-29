import asyncio

from reports.locust.controllers import get_locust_report
from reports.metrics.client import get_load_testing_metrics_http_client
from reports.metrics.controllers.base import send_load_testing_metrics


async def main():
    locust_report = get_locust_report()

    load_testing_metrics_client = get_load_testing_metrics_http_client()

    await send_load_testing_metrics(load_testing_metrics_client, locust_report)


if __name__ == '__main__':
    asyncio.run(main())
