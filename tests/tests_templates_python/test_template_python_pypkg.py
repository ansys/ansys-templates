from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_PYPKG_PATH
from ansys.templates.testing import assert_template_renders_properly


def test_template_python_pypkg(tmpdir):

    # Main variables for the template
    cookiecutter_vars = dict(
        project_name = "Dummy Project",
        __project_name_slug = "dummy-project",
        version = "0.1.dev0",
        __version = "0.1.dev0",
        __pkg_name = "dummy-project",
        __pkg_namespace = "dummy_project",
        requires_python = "3.7",
        __requires_python = "3.7",
        repository_url = "https://platform.domain/organization/dummy-project",
        __repository_url = "https://platform.domain/organization/dummy-project",
        max_linelength = "100",
        __max_linelength = "100",
    )

    # Assert no errors were raised during template rendering process
    assert_template_renders_properly(
        PYTHON_TEMPLATES_PYPKG_PATH, tmpdir, cookiecutter_vars
    )
