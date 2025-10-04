from pydantic import Field

from common.model import ResponseBase

# local imports
from ..enum import ObjectEnum


class ObjectCountResponse(ResponseBase):
    object_type: ObjectEnum = Field(title="Object type")
    object_count: int = Field(title="Number of times found in the image")