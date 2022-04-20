"""Command Line Interface for PyAnsys Templates."""

import os

import click

from ansys.templates import AVAILABLE_TEMPLATES_AND_DESCRIPTION, __version__
from ansys.templates.paths import TEMPLATE_PATH_FINDER
from ansys.templates.utils import bake_template


def create_project(template):
    """Create Python project based on a given template.

    Parameters
    ----------
    template : str
        Name of the template to be used as basis for the project

    """
    bake_template(TEMPLATE_PATH_FINDER[template], os.getcwd(), overwrite_if_exists=True)


@click.group()
def main():
    """Ansys tool for creating new Ansys projects."""
    pass


@main.command()
def list():
    """List all available templates names."""
    print("Available templates in ansys-templates are:\n")
    for template_name, description in AVAILABLE_TEMPLATES_AND_DESCRIPTION.items():
        print(f"{template_name.replace('_', '-')}: {description}")


@main.command()
def version():
    """Display current version."""
    print(f"ansys-templates {__version__}")


@main.group()
def new():
    """Create a new project from desired template."""
    pass


@new.command()
def pybasic():
    """Create a basic Python Package."""
    create_project("pybasic")


@new.command()
def pyansys():
    """Create a PyAnsys Python Package project."""
    create_project("pyansys")


@new.command()
def pyansys_advanced():
    """Create an advanced PyAnsys Python Package project."""
    create_project("pyansys_advanced")


@new.command()
def pyace():
    """Create a Python project for any method developers."""
    create_project("pyace")


@new.command()
def pyace_fast():
    """Create a FastAPI project initialized for any developer."""
    create_project("pyace-fast")


@new.command()
def pyace_flask():
    """Create a Flask project initialized for any developer."""
    create_project("pyace-flask")


@new.command()
def pyace_grpc():
    """Create gRPC project initialized for any developer."""
    create_project("pyace-grpc")
