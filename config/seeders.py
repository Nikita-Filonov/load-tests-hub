from pydantic import Field, BaseModel


class SeedersConfig(BaseModel):
    number_of_users: int = Field(
        default=500,
        description="Number of users which will be generated only for load testing scenario"
    )
