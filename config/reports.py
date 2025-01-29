from pydantic import Field, BaseModel, FilePath, field_validator


class ReportsConfig(BaseModel):
    csv_locust_stats_file: FilePath = Field(default=FilePath("locust_stats.csv"), validate_default=True)
    json_locust_ratio_file: FilePath = Field(default=FilePath("locust_ratio.json"), validate_default=True)
    csv_locust_exceptions_file: FilePath = Field(default=FilePath("locust_exceptions.csv"), validate_default=True)
    csv_locust_stats_history_file: FilePath = Field(default=FilePath("locust_stats_history.csv"), validate_default=True)

    @field_validator(
        'csv_locust_stats_file',
        'json_locust_ratio_file',
        'csv_locust_exceptions_file',
        'csv_locust_stats_history_file',
        mode='before'
    )
    def validate_files(cls, file: FilePath) -> FilePath:
        file.touch(exist_ok=True)
        return file
