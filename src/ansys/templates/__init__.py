"""
PyAnsys Templates.

A collection of interactive templates for building Python projects from scratch
according to PyAnsys guidelines.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

AVAILABLE_TEMPLATES_AND_DESCRIPTION = {
    "doc-project": "Create a documentation project using Sphinx.",
    "pybasic": "Create a basic Python Package.",
    "pyansys": "Create a PyAnsys Python Package project.",
    "pyansys-advanced": "Create an advanced PyAnsys Python Package project.",
    "pyansys-openapi_client": "Create an OpenAPI Client Package project.",
    "pyace": "Create a Python project for any method developers.",
    "pyace-flask": "Create a Flask project initialized for any developer.",
    "pyace-grpc": "Create gRPC project initialized for any developer.",
    "pyace-fast": "Create a FastAPI project initialized for any developer.",
}
"""A list holding all available templates names."""
