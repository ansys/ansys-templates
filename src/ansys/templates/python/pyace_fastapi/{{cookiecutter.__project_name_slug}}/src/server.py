{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
from fastapi import FastAPI

from _version import __version__
from observability.logger import Logger

logger = Logger.init("{{ cookiecutter.__project_name_slug }}")

tags_metadata = [
    {
        "name": "{{ cookiecutter.library_name }}",
        "description": "{{ cookiecutter.short_description }}",
    },
]
app = FastAPI(
    title="{{ cookiecutter.project_name }} {{ cookiecutter.library_name }} Application",
    openapi_tags=tags_metadata,
    debug=False,
)


@app.get("/health")
async def health():
    """Check integrity of the server."""
    return "The {{ cookiecutter.library_name }} API server is healthy."


@app.get("/version")
async def version():
    """Check current version."""
    return {"version": __version__}
