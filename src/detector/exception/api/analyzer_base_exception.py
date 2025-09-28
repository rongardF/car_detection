from http import HTTPStatus

from common.exception import HTTPException


# base exception to group and catch unhandled detector related exceptions
class AnalyzerException(HTTPException):
    status = HTTPStatus.INTERNAL_SERVER_ERROR
