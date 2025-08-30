from typing import Type, Any
from typing_extensions import Annotated, Doc

from fastapi import FastAPI

# local imports
from .exception import rest_exception_handler, HTTPException, GlobalExceptionMiddleware
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
    team_name: Annotated[
        str,
        Doc("The name of the team who owns the service. It will be added to the generated OpenAPI."),
    ],
    team_url: Annotated[
        str,
        Doc("The URL for support questions. It will be added to the generated OpenAPI."),
    ],
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

    return app