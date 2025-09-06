from pydantic import BaseModel, ConfigDict, Extra
from humps import camelize

class RequestBase(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=camelize,
        populate_by_name=True,
        validate_assignment=True,
        extra=Extra.forbid,
    )

class ResponseBase(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=camelize,
        populate_by_name=True,
        validate_assignment=True,
        extra=Extra.ignore,
        from_attributes=True
    )

