from flask import Flask, request, abort
from flask_restx import Api, Namespace, Resource
from pydantic import ValidationError

from src import ApplicationContainer
from src.services import Processor


def init_api(app: Flask, container: ApplicationContainer) -> None:
    # create API based on Flask app
    api = Api(
        app=app,
        title="Detector API",
        description="Car detector and counter API",
        doc="/documentation",
    )

    # process URL prefix (if provided)
    route_prefix = container.environment().route_prefix
    if route_prefix and not route_prefix.startswith("/"):
        route_prefix = f"/{route_prefix}"

    @api.route(f"{route_prefix}/detect_and_count", methods=['POST'])
    class Detector(Resource):
        def __init__(
            self,
            api: Api,
            processor: Processor = container.processor(),
            *args,
            **kwargs,
        ):
            super().__init__(api, *args, **kwargs)
            self._processor = processor

        def post(self):
            try:
                image_base64 = request.json.get("image_base64")
                parameters = request.json.get("parameters")

                num, inferred_image_base64 = self._processor.process(
                    image_base64=image_base64,
                    parameters_dict=parameters
                )

            except ValidationError as error:
                abort(400, description="Invalid request arguments.")
            except Exception as error:
                abort(501, description=str(error))

            return {
                "number_of_cars": num,
                "inferred_image": inferred_image_base64
            }
