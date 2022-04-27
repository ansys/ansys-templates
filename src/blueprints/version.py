# Copyright (c) 2022, My Company. Unauthorised use, distribution or duplication is prohibited

"""
my_company.

library
"""

from flask import Blueprint, jsonify

from _version import __version__

blueprint = Blueprint("api_version", __name__, url_prefix="/api/version")


@blueprint.route("/")
def get_version():
    """Get current version."""
    return jsonify({"version": __version__})
