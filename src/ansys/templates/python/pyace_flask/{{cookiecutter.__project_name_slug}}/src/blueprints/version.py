{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}
"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""

from flask import Blueprint, jsonify

from _version import __version__

blueprint = Blueprint("api_version", __name__, url_prefix="/api/version")


@blueprint.route("/")
def get_version():
    """Get current version."""
    return jsonify({"version": __version__})
