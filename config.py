from enum import Enum
from typing import Self

from pydantic import Field, HttpUrl, FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Scenario(str, Enum):
    USERS_SERVICE_MAIN_SCENARIO = 'scenarios/users_service/main_scenario/locust.conf'

    @property
    def service(self) -> str:
        try:
            return self.split('/')[1]
        except IndexError:
            raise IndexError(f'Unable to exclude service from scenario file "{self.value}"')

    @property
    def scenario(self) -> str:
        try:
            return self.split('/')[2]
        except IndexError:
            raise IndexError(f'Unable to exclude scenario from scenario file "{self.value}"')


class HTTPClientConfig(BaseSettings):
    url: HttpUrl = Field(env="URL")
    timeout: float = Field(default=120.0, env="TIMEOUT")
    retries: int = Field(default=5, env="RETRIES")
    retry_delay: float = Field(default=3.0, env="RETRY_DELAY")

    @property
    def client_url(self) -> str:
        return str(self.url)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    scenario: Scenario = Field(default=Scenario.USERS_SERVICE_MAIN_SCENARIO, env="SCENARIO")

    ci_pipeline_url: str | None = Field(default=None, env="CI_PIPELINE_URL")
    trigger_ci_pipeline_url: str | None = Field(default=None, env="TRIGGER_CI_PIPELINE_URL")
    trigger_ci_project_title: str | None = Field(default=None, env="TRIGGER_CI_PROJECT_TITLE")
    trigger_ci_project_version: str | None = Field(default=None, env="TRIGGER_CI_PROJECT_VERSION")

    number_of_users_for_scenario: int = Field(default=800, env="NUMBER_OF_USERS_FOR_SCENARIO")

    json_stats_report_file: FilePath
    json_summary_report_file: FilePath

    load_testing_metrics_http_client: HTTPClientConfig

    @classmethod
    def setup(cls) -> Self:
        json_stats_report_file = DirectoryPath("stats.json")
        json_summary_report_file = DirectoryPath("summary.json")

        json_stats_report_file.touch(exist_ok=True)
        json_summary_report_file.touch(exist_ok=True)

        return Settings(
            json_stats_report_file=json_stats_report_file,
            json_summary_report_file=json_summary_report_file
        )


settings = Settings.setup()
