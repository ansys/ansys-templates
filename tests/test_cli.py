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

from click.testing import CliRunner
import pytest

from ansys.templates import AVAILABLE_TEMPLATES_AND_DESCRIPTION, __version__
from ansys.templates.cli import main


def test_cli_main_group():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0

    assert "Ansys tool for creating new Ansys projects." in result.output

    assert "list     List all available templates names." in result.output
    assert "new      Create a new project from desired template." in result.output
    assert "version  Display current version" in result.output


def test_cli_main_list_command():
    runner = CliRunner()
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0

    assert "Available templates in ansys-templates are:" in result.output

    for template, description in AVAILABLE_TEMPLATES_AND_DESCRIPTION.items():
        assert f"{template.replace('_', '-')}: {description}" in result.output


def test_cli_main_new_group():
    runner = CliRunner()
    result = runner.invoke(main, ["new", "--help"])
    assert result.exit_code == 0

    assert "Create a new project from desired template." in result.output

    for template, description in AVAILABLE_TEMPLATES_AND_DESCRIPTION.items():
        expected_output = (
            f"  {template.replace('_', '-')}" + " " * (24 - len(template)) + f"{description[:40]}"
        )
        assert expected_output in result.output


def test_cli_main_version_command():
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0

    assert f"ansys-templates {__version__}" in result.output


@pytest.mark.parametrize("template", AVAILABLE_TEMPLATES_AND_DESCRIPTION.keys())
def test_cli_main_new(template):
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(main, ["new", template.replace("_", "-")])
        assert result.exit_code == 0
