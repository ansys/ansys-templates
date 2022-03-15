from ansys.templates.paths import TEMPLATE_PATH_FINDER
from ansys.templates.testing import assert_files_in_baked_project, assert_template_baking_process

PRODUCT_NAME = "Product"
PRODUCT_NAME_SLUG = PRODUCT_NAME.lower().replace(" ", "-").replace("_", "-")
LIBRARY_NAME = "Library"
LIBRARY_NAME_SLUG = LIBRARY_NAME.lower().replace(" ", "-").replace("_", "-")
PROJECT_NAME_SLUG = f"py{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
PKG_NAME = f"ansys-{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
PKG_NAMESPACE = PKG_NAME.replace("-", ".")
VERSION = "0.1.dev0"
SHORT_DESCRIPTION = f"A Python wrapper for Ansys {PRODUCT_NAME} {LIBRARY_NAME}"
REPOSITORY_URL = f"https://github.com/pyansys/{PROJECT_NAME_SLUG}"
REQUIRES_PYTHON = "3.7"
MAX_LINELENGTH = "100"


def test_template_python_pyansys(tmp_path, python_common_files):

    # Main variables for the template
    cookiecutter_vars = dict(
        product_name=PRODUCT_NAME,
        library_name=LIBRARY_NAME,
        version=VERSION,
        short_description=SHORT_DESCRIPTION,
        repository_url=REPOSITORY_URL,
        requires_python=REQUIRES_PYTHON,
        max_linelength=MAX_LINELENGTH,
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(TEMPLATE_PATH_FINDER["pyansys"], tmp_path, cookiecutter_vars)

    # Expected additional files
    basedir_files = ["setup.py"]
    src_files = [f"src/ansys/{PRODUCT_NAME_SLUG}/{LIBRARY_NAME_SLUG}/__init__.py"]
    all_expected_baked_files = python_common_files + basedir_files + src_files

    # Get temporary testing output project directory path
    project_path = tmp_path.joinpath(PROJECT_NAME_SLUG)

    # Check all common files are included in baked project
    assert_files_in_baked_project(all_expected_baked_files, project_path)
