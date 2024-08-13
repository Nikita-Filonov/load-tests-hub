import time
from typing import Any, Callable

import grpc
from grpc_interceptor import ClientInterceptor
from grpc_interceptor.client import ClientInterceptorReturnType
from locust.env import Environment


class GRPCInterceptor(ClientInterceptor):
    def __init__(self, environment: Environment):
        self.environment = environment

    def intercept(
            self,
            method: Callable,
            request_or_iterator: Any,
            call_details: grpc.aio.ClientCallDetails,
    ) -> ClientInterceptorReturnType:
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            response_length = response.result().ByteSize()
        except grpc.RpcError as e:
            exception = e

        self.environment.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )

        return response
