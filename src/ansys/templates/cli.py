"""Command Line Interface for PyAnsys Templates."""

import click
from cookiecutter.main import cookiecutter

from ansys.templates import AVAILABLE_TEMPLATES_AND_DESCRIPTION, __version__
from ansys.templates.paths import PYPKG_TEMPLATE_PATH


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
def pypkg():
    """Create a Python package template according to PyAnsys guidelines."""
    cookiecutter(str(PYPKG_TEMPLATE_PATH))
