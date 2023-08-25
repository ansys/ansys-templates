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
from ansys.templates.paths import (
    PYTHON_TEMPLATES_OSL_SOLUTION_PATH,
    PYTHON_TEMPLATES_SOLUTION_PATH,
    TEMPLATE_PATH_FINDER,
)
from ansys.templates.utils import bake_template, load_inputs_from_configuration_file


def create_project(template, no_input=False, extra_context={}):
    """Create Python project based on a given template.

    Parameters
    ----------
    template : str
        Name of the template to be used as basis for the project

    """
    bake_template(TEMPLATE_PATH_FINDER[template], os.getcwd(), overwrite_if_exists=True, no_input=no_input, extra_context=extra_context)


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
@click.option('-s', '--solution-name', type=str, help="Name of the solution in the definition.")
@click.option('-d', '--solution-display-name', type=str, help="Name of the solution in the user interface.")
@click.option("-u", "--with-dash-ui", is_flag=True, flag_value="1", help="With Dash UI")
@click.option('-a', '--application-archive', type=click.Path(), help="Path to the optiSLang application archive.")
def solution(_from, solution_name, solution_display_name, with_dash_ui, application_archive):
    """[Ansys Internal Use Only] Create a solution based on SAF."""
    if _from == 'owa':
        template = "osl-solution"
        extra_context = load_inputs_from_configuration_file(PYTHON_TEMPLATES_OSL_SOLUTION_PATH)
        no_input = True if application_archive else False
        if application_archive:
            extra_context["optiSLang_application_archive"] = application_archive
    else:
        template = "solution"
        extra_context = load_inputs_from_configuration_file(PYTHON_TEMPLATES_SOLUTION_PATH)
        no_input = True if solution_name or solution_display_name or with_dash_ui else False
        if solution_name:
            extra_context["solution_name"] = solution_name
        if solution_display_name:
            extra_context["solution_display_name"] = solution_display_name
        if with_dash_ui:
            extra_context["with_dash_ui"] = "yes"

    create_project(template, no_input=no_input, extra_context=extra_context)
