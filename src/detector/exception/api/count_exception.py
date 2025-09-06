from http import HTTPStatus
from typing import Any

# local imports
from .analyzer_base_exception import AnalyzerException


# base exception to group and catch all count analysis related exceptions
class CountBadRequestException(AnalyzerException):
    status = HTTPStatus.BAD_REQUEST

    def __init__(self, detail: Any = "count_endpoint_raised_an_exception"):
        super().__init__(detail=detail)


class MaskInvalidException(CountBadRequestException):
    def __init__(self, detail: Any = "frame_mask_has_invalid_values"):
        super().__init__(detail=detail)


class FileInvalidException(CountBadRequestException):
    def __init__(self, detail: Any = "file_type_not_allowed"):
        super().__init__(detail=detail)