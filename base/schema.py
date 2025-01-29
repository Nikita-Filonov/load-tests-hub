import csv
from typing import Self

from pydantic import BaseModel, FilePath, RootModel


class JSONSchema(BaseModel):
    @classmethod
    def from_json(cls, file: FilePath) -> Self:
        return cls.model_validate_json(file.read_text())


class CSVRootSchema(RootModel):
    @classmethod
    def from_csv(cls, file: FilePath) -> Self:
        reader = csv.DictReader(file.open())
        return cls.model_validate(reader)
