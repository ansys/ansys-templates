"""Command Line Interface for PyAnsys Templates."""

import os

import click

from ansys.templates import AVAILABLE_TEMPLATES_AND_DESCRIPTION, __version__
from ansys.templates.paths import TEMPLATE_PATH_FINDER
from ansys.templates.utils import bake_template


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
    bake_template(TEMPLATE_PATH_FINDER["pybasic"], os.getcwd(), overwrite_if_exists=True)


@new.command()
def pyansys():
    """Create a PyAnsys Python Package project."""
    bake_template(TEMPLATE_PATH_FINDER["pyansys"], os.getcwd(), overwrite_if_exists=True)


@new.command()
def pyansys_advanced():
    """Create an advanced PyAnsys Python Package project."""
    bake_template(TEMPLATE_PATH_FINDER["pyansys_advanced"], os.getcwd(), overwrite_if_exists=True)
