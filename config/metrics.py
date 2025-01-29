from pydantic import BaseModel

from config.scenarios import Scenario


class ScenarioConfig(BaseModel):
    id: int
    number_of_users: int
    runtime_duration: str


class ServiceConfig(BaseModel):
    id: int
    scenarios: dict[str, ScenarioConfig]

    def get_scenario(self, scenario: Scenario) -> ScenarioConfig:
        try:
            return self.scenarios[f'{scenario.scenario}_{scenario.version}']
        except KeyError:
            raise KeyError(
                f'Scenario "{scenario.scenario}" of version "{scenario.version}" '
                f'is not supported for sending metrics'
            )


class MetricsConfig(BaseModel):
    services: dict[str, ServiceConfig]

    def get_service(self, scenario: Scenario) -> ServiceConfig:
        try:
            return self.services[scenario.service]
        except KeyError:
            raise KeyError(f'Service "{scenario.service}" is not supported for sending metrics')
