from pydantic import BaseModel, ConfigDict, Field


class RatioResult(BaseModel):
    name: str
    ratio: float
    tasks: list['RatioResult']

    @classmethod
    def from_ratio_dict(cls, ratio: dict) -> list['RatioResult']:
        return [
            RatioResult(
                name=key,
                ratio=value.get('ratio', 0.0),
                tasks=cls.from_ratio_dict(value.get('tasks', {}))
            )
            for key, value in ratio.items()
        ]


class CreateRatioResultRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ratio_total: list[RatioResult] = Field(alias="ratioTotal")
    ratio_per_class: list[RatioResult] = Field(alias="ratioPerClass")
    load_test_result_id: int = Field(alias="loadTestResultId")
