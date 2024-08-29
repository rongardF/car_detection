import logging
from waitress import serve
from flask import Flask

from src import ApplicationContainer
from src import init_api


if __name__ == "__main__":
    LOGGER = logging.getLogger("root")

    container = ApplicationContainer()
    app = Flask(__name__)
    init_api(app, container)

    if container.environment().debug_mode:
        # Note: code hot reload makes app run exit with code 3
        # which is considered by debugger as an exception.
        # Uncaught Exceptions has to be turned of in the debugger settings
        # in order to preserve sanity.
        # [Link](https://github.com/microsoft/debugpy/issues/1306)
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        serve(app, host="0.0.0.0", port=5000)