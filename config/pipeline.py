from pydantic import BaseModel


class PipelineConfig(BaseModel):
    is_trigger: bool = False
    ci_job_url: str | None = None
    ci_project_url: str | None = None
    ci_pipeline_url: str | None = None
    ci_project_version: str | None = None

    @property
    def ci_project_version_url(self) -> str:
        return f"{self.ci_project_url}/-/tags/{self.ci_project_version}"
