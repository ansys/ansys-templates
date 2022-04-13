from ansys.templates.paths import TEMPLATE_PATH_FINDER
from ansys.templates.testing import assert_project_structure, assert_template_baking_process

PROJECT_NAME = "pybasic"
PROJECT_NAME_SLUG = "pybasic"
VERSION = "0.1.dev0"
SHORT_DESCRIPTION = "A basic Python Package"
REPOSITORY_URL = f"https://platform.domain/organization/{PROJECT_NAME_SLUG}"
REQUIRES_PYTHON = "3.7"
MAX_LINELENGTH = "100"

EXPECTED_STRUCTURE = [
    ".coveragerc",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "doc/Makefile",
    "doc/make.bat",
    "doc/source/conf.py",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
    "doc/source/_templates/sidebar-nav-bs.html",
    "doc/source/_templates/README.md",
    "examples/README.md",
    ".flake8",
    ".gitignore",
    "LICENSE",
    "pyproject.toml",
    "README.rst",
    "requirements_build.txt",
    "requirements_doc.txt",
    "requirements_tests.txt",
    "setup.py",
    f"src/{PROJECT_NAME_SLUG}/__init__.py",
    "tests/test_metadata.py",
]

def test_template_python_pybasic(tmp_path):

    # Main variables for the template
    cookiecutter_vars = dict(
        project_name=PROJECT_NAME,
        version=VERSION,
        short_description=SHORT_DESCRIPTION,
        repository_url=REPOSITORY_URL,
        requires_python=REQUIRES_PYTHON,
        max_linelength=MAX_LINELENGTH,
    )

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(TEMPLATE_PATH_FINDER["pybasic"], tmp_path, cookiecutter_vars)

    # Get temporary testing output project directory path
    project_path = tmp_path.joinpath(PROJECT_NAME_SLUG)

    # Check all common files are included in baked project
    assert_project_structure(EXPECTED_STRUCTURE, project_path)
