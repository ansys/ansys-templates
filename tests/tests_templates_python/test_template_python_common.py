from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH
from ansys.templates.testing import (
    assert_files_in_baked_project,
    assert_template_baking_process,
)

PROJECT_NAME_SLUG = "python-common"
VERSION = "0.1.dev0"
SHORT_DESCRIPTION = "Python common project"
PKG_NAME = f"{PROJECT_NAME_SLUG}"
PKG_NAMESPACE = f"{PROJECT_NAME_SLUG.replace('-', '_')}"
REQUIRES_PYTHON = "3.7"
REPOSITORY_URL = f"https://platform.domain/organization/{PROJECT_NAME_SLUG}"
MAX_LINELENGTH = "100"


def test_template_python_common(tmp_path, python_common_files):

    # Main variables for of the common template
    cookiecutter_vars = {
        "__project_name_slug": PROJECT_NAME_SLUG,
        "__version": VERSION,
        "__short_description": SHORT_DESCRIPTION,
        "__pkg_name": PKG_NAME,
        "__pkg_namespace": PKG_NAMESPACE,
        "__requires_python": REQUIRES_PYTHON,
        "__repository_url": REPOSITORY_URL,
        "__max_linelength": MAX_LINELENGTH,
    }

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(
        PYTHON_TEMPLATES_COMMON_PATH, tmp_path, cookiecutter_vars
    )

    # Get temporary testing output project directory path
    project_path = tmp_path / PROJECT_NAME_SLUG

    # Check all common files are included in baked project
    assert_files_in_baked_project(python_common_files, project_path)
