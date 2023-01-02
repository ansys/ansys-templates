# Copyright (c) 2023, My Company. Unauthorised use, distribution or duplication is prohibited

"""
my_company.

library
"""

from flask import Blueprint, jsonify

from observability.logger import Logger

blueprint = Blueprint("health_check", __name__, url_prefix="/api/health")

logger = Logger.init("project")


@blueprint.route("/")
def health_check():
    """Check health status."""
    logger.info("Health check")
    return jsonify({"status": "ok"})
