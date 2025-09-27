from typing import Type, Any
from typing_extensions import Annotated, Doc

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# local imports
from .middleware import GlobalExceptionMiddleware
from .exception import rest_exception_handler, HTTPException
from .router import docs
from .initializer import Initializer


def create_fastapi_app(
    *,
    initializer: Annotated[
        Type[Initializer],
        Doc("A `Lifespan` context manager handler extended from Initializer."),
    ],
    title: Annotated[
        str,
        Doc("The title of the API. It will be added to the generated OpenAPI."),
    ],
    description: Annotated[
        str,
        Doc("A description of the API (supports Markdown). It will be added to the generated OpenAPI."),
    ],
    version: Annotated[
        str,
        Doc("A version of the API (supports Markdown). It will be added to the generated OpenAPI."),
    ],
    summary: Annotated[
        str,
        Doc("A summary of the API (supports Markdown). It will be added to the generated OpenAPI."),
    ] = str(),
    team_name: Annotated[
        str,
        Doc("The name of the team who owns the service. It will be added to the generated OpenAPI."),
    ] = str(),
    team_url: Annotated[
        str,
        Doc("The URL for support questions. It will be added to the generated OpenAPI."),
    ] = str(),
    **fastapi_configs: Annotated[
        Any,
        Doc(
            """
            Any extra configurations provided by FastAPI
            (see https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI).
            """
        ),
    ],
) -> FastAPI:
    """
    Returns a FastAPI instance with basic set of endpoints and middleware required by
    platform to perform logging, collect metrics and generate OpenAPI documentation.
    """
    fastapi_configs.pop("redoc_url", None)
    fastapi_configs.pop("contact", None)

    app = FastAPI(
        redoc_url=None,
        lifespan=initializer,
        title=title,
        description=description,
        contact={"name": team_name, "url": team_url},
        exception_handlers={HTTPException: rest_exception_handler},
        **fastapi_configs,
    )

    # Required endpoints
    app.include_router(docs.router)

    # Required middleware
    # app.add_middleware(LoggingMiddleware)  # This is the most inner middleware right before the router.
    app.add_middleware(GlobalExceptionMiddleware)
    # app.add_middleware(HTTPSRedirectMiddleware)
    # TODO: add 'CORSMiddleware' to avoid CORS errors on FE side

    # Add security schemas to work with HTTPS/authentication
    def _custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=title,
            version=version,
            summary=summary,
            description=description,
            contact={"name": team_name, "url": team_url},
            routes=app.routes,
        )
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}

        if "securitySchemes" not in openapi_schema["components"]:
            openapi_schema["components"]["securitySchemes"] = {}

        openapi_schema["components"]["securitySchemes"].update({
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
            "APIKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
            },
        })
        if "schemas" not in openapi_schema["components"]:
            openapi_schema["components"]["schemas"] = {}
        
        # add global security method (all endpoints require this)
        # openapi_schema["security"] = [{"BearerAuth": []}, {"APIKeyAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    # app.openapi = _custom_openapi

    return app