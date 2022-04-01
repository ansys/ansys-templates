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
            f"  {template.replace('_', '-')}" + " " * (18 - len(template)) + f"{description[:45]}"
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
