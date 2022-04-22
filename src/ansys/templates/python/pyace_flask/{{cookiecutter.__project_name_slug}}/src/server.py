{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
import argparse

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from blueprints.health import blueprint as health_endpoint
from blueprints.version import blueprint as version_endpoint
from observability.logger import Logger

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"


SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "{{ cookiecutter.project_name }} {{ cookiecutter.library_name }} Api"},
)

logger = Logger.init("{{ cookiecutter.__project_name_slug }}")


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    CORS(app, resources=r"/api/*")
    app.config["CORS_HEADERS"] = "Content-Type"
    app.register_blueprint(version_endpoint)
    app.register_blueprint(health_endpoint)
    app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


def serve(app, address, port, middleware=None):
    """Serve the application."""
    if middleware is not None:
        middleware(app)

    logger.info("{{ cookiecutter.project_name }} {{ cookiecutter.library_name }} Server starting...")
    app.run(host=address, port=port)


if __name__ == "__main__":
    app = create_app()
    logger.info("server.py main : parsing arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", help="Set server address", default="0.0.0.0")
    parser.add_argument("-p", "--port", type=int, help="Set server port", default=5000)
    args = parser.parse_args()
    serve(app=app, address=args.address, port=args.port)
