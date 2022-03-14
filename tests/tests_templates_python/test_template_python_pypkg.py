from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_PYPKG_PATH
from ansys.templates.testing import assert_template_baking_process, assert_file_in_baked_project


def test_template_python_pypkg(tmpdir, python_common_files):

    # Main variables for the template
    cookiecutter_vars = dict(
        __project_name = "Dummy Project",
        __project_name_slug = "dummy-project",
        __short_description = "A dummy project",
        __version = "0.1.dev0",
        __requires_python = "3.7",
        __repository_url = "https://platform.domain/organization/dummy-project",
        __max_linelength = "100",
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(
        PYTHON_TEMPLATES_PYPKG_PATH, tmpdir, cookiecutter_vars
    )

    # Assert files in baked project
    for filepath in python_common_files:
        assert_filepath_in_baked_project(
            filepath, Path(tmpdir) / "dummy-project"
        )
