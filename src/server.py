# Copyright (c) 2022, My Company. Unauthorised use, distribution or duplication is prohibited


"""
my_company.

library
"""
from fastapi import FastAPI

from _version import __version__
from observability.logger import Logger

logger = Logger.init("project")

tags_metadata = [
    {
        "name": "library",
        "description": "A my_company Python project for my_company library",
    },
]
app = FastAPI(
    title="my_company library Application",
    openapi_tags=tags_metadata,
    debug=False,
)


@app.get("/health")
async def health():
    """Check integrity of the server."""
    return "The library API server is healthy."


@app.get("/version")
async def version():
    """Check current version."""
    return {"version": __version__}
