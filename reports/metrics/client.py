from clients.http.client import HTTPClient
from logger import get_logger
from reports.metrics.schema.exception_results import CreateExceptionResultsRequest
from reports.metrics.schema.load_test_results import CreateLoadTestResultRequest, CreateLoadTestResultResponse
from reports.metrics.schema.method_results import CreateMethodResultsRequest, CreateMethodResultsResponse
from reports.metrics.schema.ratio_results import CreateRatioResultRequest
from reports.metrics.schema.results_history.load_test_results_history import CreateLoadTestResultsHistoryRequest
from reports.metrics.schema.results_history.method_results_history import CreateMethodResultsHistoryRequest
from reports.metrics.schema.scenarios import UpdateScenarioRequest
from settings import settings


class LoadTestingMetricsHTTPClient(HTTPClient):

    async def create_load_test_result(self, request: CreateLoadTestResultRequest) -> CreateLoadTestResultResponse:
        response = await self.post(
            '/api/v1/load-test-results',
            json=request.model_dump(by_alias=True, mode='json')
        )
        return CreateLoadTestResultResponse(**response.json())

    async def create_method_results(self, request: CreateMethodResultsRequest) -> CreateMethodResultsResponse:
        response = await self.post(
            '/api/v1/method-results',
            json=request.model_dump(by_alias=True, mode='json')
        )
        return CreateMethodResultsResponse(**response.json())

    async def create_method_results_history(self, request: CreateMethodResultsHistoryRequest):
        await self.post(
            '/api/v1/method-results-history',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_load_test_results_history(self, request: CreateLoadTestResultsHistoryRequest):
        await self.post(
            '/api/v1/load-test-results-history',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_ratio_results(self, request: CreateRatioResultRequest):
        await self.post(
            '/api/v1/ratio-results',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def create_exception_results(self, request: CreateExceptionResultsRequest):
        await self.post(
            '/api/v1/exception-results',
            json=request.model_dump(by_alias=True, mode='json')
        )

    async def update_scenario(self, scenario_id: int, request: UpdateScenarioRequest):
        await self.patch(
            f'/api/v1/scenarios/{scenario_id}',
            json=request.model_dump(by_alias=True, mode='json')
        )


def get_load_testing_metrics_http_client():
    logger = get_logger('LOAD_TESTING_METRICS_HTTP_CLIENT')

    return LoadTestingMetricsHTTPClient(
        logger=logger,
        config=settings.load_testing_metrics_http_client
    )
