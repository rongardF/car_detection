from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.types import Receive, Scope, Send


class GlobalExceptionMiddleware:
    # more info about middlewares: https://www.starlette.io/middleware/ 
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # logger: VeriffLogger = scope["state"]["logger"]

        try:
            await self.app(scope, receive, send)
        except ValueError as err:
            response = JSONResponse(
                status_code=getattr(HTTPStatus.BAD_REQUEST, "value"),
                content={"errors": [getattr(HTTPStatus.BAD_REQUEST, "phrase")]},
            )
            await response(scope, receive, send)
        except Exception as err:  # pylint: disable=broad-exception-caught
            # logger.exception("unhandled_exception")
            response = JSONResponse(
                status_code=getattr(HTTPStatus.INTERNAL_SERVER_ERROR, "value"),
                content={"errors": [getattr(HTTPStatus.INTERNAL_SERVER_ERROR, "phrase")]},
            )
            await response(scope, receive, send)
