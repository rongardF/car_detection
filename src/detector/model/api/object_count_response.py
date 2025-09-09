from pydantic import Field

from common.model import ResponseBase

# local imports
from ...model.enum import ObjectEnum


class ObjectCountResponse(ResponseBase):
    objects: dict[str, int] = Field(title="Objects count", default_factory=lambda:{}, examples=[{"car":5,"bus":2}])
