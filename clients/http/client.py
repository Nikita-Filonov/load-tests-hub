import asyncio
from abc import ABC
from logging import Logger
from typing import Optional, Any

from httpx import AsyncClient, Response, URL, Headers, QueryParams, Timeout

from clients.http.event_hooks.logger_event_hook import HTTPLoggerEventHook
from settings import HTTPClientConfig

URLType = URL | str


class HTTPClient(ABC):
    retry_statuses: list[int] = [500, 503, 504]

    def __init__(self, config: HTTPClientConfig, logger: Logger) -> None:
        logger_event_hook = HTTPLoggerEventHook(logger=logger)

        self.client = AsyncClient(
            base_url=config.client_url,
            timeout=Timeout(timeout=config.timeout),
            event_hooks={
                'request': [logger_event_hook.log_request],
                'response': [logger_event_hook.log_response]
            }
        )
        self.logger = logger
        self.config = config

    async def send_with_retries(
            self,
            method: str,
            url: URLType,
            json: Optional[Any] = None,
            params: Optional[QueryParams] = None,
            headers: Optional[Headers] = None
    ) -> Response:
        response: Response | None = None

        attempt = 0
        while attempt < self.config.retries:
            response = await self.client.request(
                method,
                url=url,
                json=json,
                params=params,
                headers=headers
            )
            status_code = response.status_code

            if status_code not in self.retry_statuses:
                return response

            self.logger.error(
                f'{method} {response.request.url} - Unexpected status {status_code}, retrying'
            )

            attempt += 1

            await asyncio.sleep(self.config.retry_delay)

        return response

    async def post(self, url: URLType, json: Optional[Any] = None) -> Response:
        return await self.send_with_retries("POST", url=url, json=json)

    async def patch(self, url: URLType, json: Optional[Any] = None) -> Response:
        return await self.send_with_retries("PATCH", url=url, json=json)
