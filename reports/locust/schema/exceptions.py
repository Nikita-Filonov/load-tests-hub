from pydantic import Field, BaseModel

from base.schema import CSVRootSchema


class LocustExceptions(BaseModel):
    count: int = Field(alias="Count")
    message: str = Field(alias="Message")
    traceback: str = Field(alias="Traceback")


class LocustExceptionsList(CSVRootSchema):
    root: list[LocustExceptions]
