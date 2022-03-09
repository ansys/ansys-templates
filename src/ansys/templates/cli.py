"""Command Line Interface for PyAnsys Templates."""

import click
from cookiecutter.main import cookiecutter

from ansys.templates.paths import PYPKG_TEMPLATE_PATH


@click.group()
def main():
    """An Ansys tool for creating Python projects."""
    pass


@main.group()
def new():
    """Create a new project from desired template."""
    pass


@new.command()
def pypkg():
    """Create a Python package template according to PyAnsys guidelines."""
    cookiecutter(str(PYPKG_TEMPLATE_PATH))
