# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
def doc_project():
    """Create a documentation project using Sphinx."""
    create_project("doc-project")


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
    create_project("pyansys-advanced")


@new.command()
def pyansys_openapi_client():
    """Create an OpenAPI Client Package project."""
    create_project("pyansys-openapi-client")


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

@new.command()
@click.option('-f',  '--from', '_from' , help='From existing optiSLang application archive (OWA).',
              type=click.Choice(['owa'], case_sensitive=False))
def solution(_from):
    """[Ansys Internal Use Only] Create a solution based on SAF."""
    if _from == 'owa':
        create_project("osl-solution")
    else:
        create_project("solution")
