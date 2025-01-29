from pydantic import BaseModel

from base.schema import JSONSchema


class TaskSet(BaseModel):
    ratio: float
    tasks: dict[str, 'TaskSet'] | None = None


class LocustRatios(JSONSchema):
    total: dict[str, TaskSet]
    per_class: dict[str, TaskSet]
