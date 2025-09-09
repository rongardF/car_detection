from http import HTTPStatus
from typing import Any

# local imports
from .analyzer_base_exception import AnalyzerException


# base exception to group and catch all configure endpoint bad request related exceptions
class ConfigureBadRequestException(AnalyzerException):
    status = HTTPStatus.BAD_REQUEST

    def __init__(self, detail: Any = "configure_endpoint_bad_request"):
        super().__init__(detail=detail)


# base exception to group and catch all configure endpoint not found related exceptions
class ConfigureNotFoundException(AnalyzerException):
    status = HTTPStatus.NOT_FOUND

    def __init__(self, detail: Any = "configure_endpoint_entity_not_found"):
        super().__init__(detail=detail)