from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


def _to_pascal(field_name):
    cc = ''.join(x.capitalize() or '_' for x in field_name.split('_'))
    return cc[0].lower() + cc[1:]


class BaseResponse(BaseModel):
    class Config:
        alias_generator = _to_pascal
        extra = "forbid"  # fail if we encounter some new field


class Output(BaseResponse):
    type: str = ""
    url: str = ""


class JobStatus(BaseResponse):
    transaction_time: datetime = None
    request: str = ""
    requires_access_token: bool = False
    output: list[Output] = None
    error: list[Any] = None
    job_id: int = Field(0, alias='JobID')

    def output_map(self) -> dict[str, str]:
        return {o.type: o.url for o in self.output}

    @property
    def is_error(self):
        return len(self.error) > 0

    @property
    def is_empty(self):
        return len(self.output) == 0
