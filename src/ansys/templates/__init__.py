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
    "pybasic": "Create a basic Python Package.",
    "pyansys": "Create a PyAnsys Python Package project.",
    "pyansys_advanced": "Create an advanced PyAnsys Python Package project.",
}
"""A list holding all available templates names."""
