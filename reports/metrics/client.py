from config import settings
from logger import get_logger
from reports.metrics.schema.history_results import CreateHistoryResultsRequest
from reports.metrics.schema.load_test_results import CreateLoadTestResultRequest, CreateLoadTestResultResponse
from reports.metrics.schema.method_results import CreateMethodResultsRequest
from reports.metrics.schema.ratio_results import CreateRatioResultRequest
from reports.metrics.schema.scenarios import CreateScenarioRequest
from clients.http.client import HTTPClient


class LoadTestingMetricsHTTPClient(HTTPClient):

    async def create_load_test_result(self, request: CreateLoadTestResultRequest) -> CreateLoadTestResultResponse:
        response = await self.post(
            '/api/v1/load-test-results',
            json=request.model_dump(by_alias=True, mode='json')
        )
        return CreateLoadTestResultResponse(**response.json())

    async def create_method_results(self, request: CreateMethodResultsRequest):
        await self.post(
            '/api/v1/method-results',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_history_results(self, request: CreateHistoryResultsRequest):
        await self.post(
            '/api/v1/history-results',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_ratio_results(self, request: CreateRatioResultRequest):
        await self.post(
            '/api/v1/ratio-results',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_scenario(self, request: CreateScenarioRequest):
        await self.post(
            '/api/v1/scenarios',
            json=request.model_dump(by_alias=True, mode='json')
        )


def get_load_testing_metrics_http_client():
    logger = get_logger('LOAD_TESTING_METRICS_HTTP_CLIENT')

    return LoadTestingMetricsHTTPClient(
        logger=logger,
        config=settings.load_testing_metrics_http_client
    )
