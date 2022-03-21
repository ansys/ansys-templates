import pytest

from ansys.templates.paths import TEMPLATE_PATH_FINDER
from ansys.templates.testing import assert_files_in_baked_project, assert_template_baking_process

PRODUCT_NAME = "Product"
PRODUCT_NAME_SLUG = PRODUCT_NAME.lower().replace(" ", "-")
LIBRARY_NAME = "Library"
LIBRARY_NAME_SLUG = LIBRARY_NAME.lower().replace(" ", "-")
PROJECT_NAME_SLUG = f"py{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
PKG_NAME = f"ansys-{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
PKG_NAMESPACE = PKG_NAME.replace("-", ".")
VERSION = "0.1.dev0"
SHORT_DESCRIPTION = f"A Python wrapper for Ansys {PRODUCT_NAME} {LIBRARY_NAME}"
REPOSITORY_URL = f"https://github.com/pyansys/{PROJECT_NAME_SLUG}"
REQUIRES_PYTHON = "3.7"
MAX_LINELENGTH = "100"


@pytest.mark.parametrize("build_system", ["flit", "poetry", "setuptools"])
def test_template_python_pyansys_advanced(tmp_path, python_common_files, build_system):

    # Remove the requirements files at base directory level as they are included
    # now under a common requirements/ directory
    new_python_common_files = python_common_files.copy()
    [
        new_python_common_files.remove(f"requirements_{name}.txt")
        for name in ["build", "doc", "tests"]
    ]

    # Main variables for the template
    cookiecutter_vars = dict(
        product_name=PRODUCT_NAME,
        library_name=LIBRARY_NAME,
        version=VERSION,
        short_description=SHORT_DESCRIPTION,
        repository_url=REPOSITORY_URL,
        requires_python=REQUIRES_PYTHON,
        build_system=build_system,
        max_linelength=MAX_LINELENGTH,
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(
        TEMPLATE_PATH_FINDER["pyansys_advanced"], tmp_path, cookiecutter_vars
    )

    # Expected additional files
    doc_files = [
        "doc/make.bat",
        "doc/Makefile",
        "doc/source/conf.py",
        "doc/source/index.rst",
        "doc/source/_static/README.md",
        "doc/source/_templates/README.md",
        "doc/source/_templates/sidebar-nav-bs.html",
    ]

    dot_files = [
        ".flake8",
        ".gitignore",
        ".pre-commit-config.yaml",
    ]

    github_files = [
        ".github/workflows/ci_cd.yml",
    ]

    requirements_files = [
        "requirements/requirements_tests.txt",
        "requirements/requirements_doc.txt",
        "requirements/requirements_build.txt",
    ]

    src_files = [
        f"src/ansys/{PRODUCT_NAME_SLUG}/{LIBRARY_NAME_SLUG}/__init__.py",
    ]

    tests_files = [
        "tests/test_metadata.py",
    ]

    basedir_files = [
        "LICENSE",
        "README.rst",
        "pyproject.toml" if build_system != "setuptools" else "setup.py",
        "tox.ini",
    ]

    all_expected_baked_files = (
        new_python_common_files
        + basedir_files
        + src_files
        + doc_files
        + tests_files
        + requirements_files
        + dot_files
        + github_files
    )

    # Get temporary testing output project directory path
    project_path = tmp_path.joinpath(PROJECT_NAME_SLUG)

    # Check all common files are included in baked project
    assert_files_in_baked_project(all_expected_baked_files, project_path)
