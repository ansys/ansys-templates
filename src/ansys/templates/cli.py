"""Command Line Interface for PyAnsys Templates."""

import os

import click
from cookiecutter.main import cookiecutter

from ansys.templates import AVAILABLE_TEMPLATES_AND_DESCRIPTION, __version__
from ansys.templates.paths import PYTHON_TEMPLATES_PYANSYS_PATH 
from ansys.templates.utils import bake_template


@click.group()
def main():
    """Ansys tool for creating Python projects."""
    pass


@main.command()
def list():
    """List all available templates names."""
    print("Available templates in ansys-templates are:\n")
    for template_name, description in AVAILABLE_TEMPLATES_AND_DESCRIPTION.items():
        print(f"{template_name}: {description}")


@main.command()
def version():
    """Display current version."""
    print(f"ansys-templates {__version__}")


@main.group()
def new():
    """Create a new project from desired template."""
    pass


@new.command()
def pyansys():
    """Create a Python package template according to PyAnsys guidelines."""
    bake_template(PYTHON_TEMPLATES_PYANSYS_PATH, os.getcwd())
