from pydantic_settings import BaseSettings, SettingsConfigDict

from config.http_client import HTTPClientConfig
from config.metrics import MetricsConfig
from config.pipeline import PipelineConfig
from config.reports import ReportsConfig
from config.scenarios import Scenario
from config.seeders import SeedersConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    scenario: Scenario = Scenario.USER_SERVICE_USER_DETAILS_V2_0

    reports: ReportsConfig = ReportsConfig()
    metrics: MetricsConfig
    seeders: SeedersConfig = SeedersConfig()
    trigger_pipeline: PipelineConfig = PipelineConfig()
    load_tests_pipeline: PipelineConfig = PipelineConfig()

    load_testing_metrics_http_client: HTTPClientConfig


settings = Settings()
