from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH
from ansys.templates.testing import assert_files_in_baked_project, assert_template_baking_process

PROJECT_NAME_SLUG = "python-common"

def test_template_python_common(tmp_path, python_common_files):

    # Main variables for of the common template
    cookiecutter_vars = dict(
        __project_name_slug="python-common",
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(PYTHON_TEMPLATES_COMMON_PATH, tmp_path, cookiecutter_vars)

    # Get temporary testing output project directory path
    project_path = tmp_path / PROJECT_NAME_SLUG

    # Check all common files are included in baked project
    assert_files_in_baked_project(python_common_files, project_path)
