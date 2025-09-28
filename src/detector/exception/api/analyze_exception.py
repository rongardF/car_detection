from http import HTTPStatus
from typing import Any

# local imports
from .analyzer_base_exception import AnalyzerException


# base exception to group and catch all analyze endpoint bad request related exceptions
class AnalyzeBadRequestException(AnalyzerException):
    status = HTTPStatus.BAD_REQUEST

    def __init__(self, detail: Any = "analyze_endpoint_bad_request"):
        super().__init__(detail=detail)


class MaskInvalidException(AnalyzeBadRequestException):
    def __init__(self, detail: Any = "frame_mask_has_invalid_values"):
        super().__init__(detail=detail)


class FileInvalidException(AnalyzeBadRequestException):
    def __init__(self, detail: Any = "file_type_not_allowed"):
        super().__init__(detail=detail)


# base exception to group and catch all analyze endpoint not found related exceptions
class AnalyzeNotFoundException(AnalyzerException):
    status = HTTPStatus.NOT_FOUND

    def __init__(self, detail: Any = "analyze_endpoint_entity_not_found"):
        super().__init__(detail=detail)