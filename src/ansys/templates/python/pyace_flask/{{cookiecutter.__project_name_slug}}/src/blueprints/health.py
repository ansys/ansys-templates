{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}
"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""

from flask import Blueprint, jsonify

from observability.logger import Logger

blueprint = Blueprint("health_check", __name__, url_prefix="/api/health")

logger = Logger.init("{{ cookiecutter.__project_name_slug }}")


@blueprint.route("/")
def health_check():
    """Check health status."""
    logger.info("Health check")
    return jsonify({"status": "ok"})
