from abc import ABC, abstractmethod
from typing import Type

import grpc
import grpc.experimental.gevent as grpc_gevent
from locust import SequentialTaskSet, events
from locust.env import Environment
from locust.exception import LocustError

from clients.grpc.interceptor import GRPCInterceptor
from reports.locust.controllers import dump_locust_report_stats

grpc_gevent.init_gevent()


class GRPCStub(ABC):
    @abstractmethod
    def __init__(self, channel: grpc.Channel):
        pass


class GRPCTaskSet(SequentialTaskSet):
    stub: GRPCStub
    stub_class: Type[GRPCStub]

    channel: grpc.Channel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for attr_value, attr_name in ((self.user.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self.channel = grpc.secure_channel(self.user.host, credentials=grpc.ssl_channel_credentials())

        interceptor = GRPCInterceptor(environment=self.user.environment)
        self.channel = grpc.intercept_channel(self.channel, interceptor)

        self.stub = self.stub_class(self.channel)

    def on_stop(self):
        self.channel.close()


@events.test_stop.add_listener
def on_test_stop(environment: Environment, **kwargs):
    dump_locust_report_stats(environment)
