from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_PYPKG_PATH, PYTHON_TEMPLATES_COMMON_PATH
from ansys.templates.testing import assert_template_baking_process, assert_filepath_in_baked_project
from ansys.templates.utils import bake_template


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


def test_template_python_pypkg(tmpdir, python_common_files):

    # Main variables for the template
    cookiecutter_vars = dict(
        product_name = PRODUCT_NAME,
        library_name = LIBRARY_NAME,
        version = VERSION,
        short_description = SHORT_DESCRIPTION,
        repository_url = REPOSITORY_URL,
        requires_python = REQUIRES_PYTHON,
        max_linelength = MAX_LINELENGTH,
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(
        PYTHON_TEMPLATES_PYPKG_PATH, Path(tmpdir), cookiecutter_vars
    )

    # Get temporary testing output project directory path
    project_dirpath = Path(tmpdir) / PROJECT_NAME_SLUG

    # Expected additional files
    basedir_files = [Path(file) for file in ["setup.py"]]
    src_files = [
        Path(f"src/ansys/{PRODUCT_NAME_SLUG}/{LIBRARY_NAME_SLUG}/__init__.py")
    ]


    ## Collect all expected files
    all_expected_baked_files = (
        python_common_files + basedir_files + src_files
    )

    ## Check all common files are included in baked project
    for filepath in all_expected_baked_files:
        assert_filepath_in_baked_project(filepath, project_dirpath)
