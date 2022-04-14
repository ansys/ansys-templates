from copy import deepcopy

import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH, TEMPLATE_PATH_FINDER
from ansys.templates.testing import assert_project_structure, assert_template_baking_process
from ansys.templates.utils import keep_files

PYCOMMON_VARS = dict(
    __project_name_slug = "common"
)

PYBASIC_VARS = dict(
    project_name = "pybasic",
    __project_name_slug = "pybasic",
    short_description = "A basic Python Package",
    repository_url = "https://platform.domain/organization/pybasic",
    requires_python = "3.7",
)

PYANSYS_VARS = PYANSYS_ADVANCED_VARS = dict(
    product_name = "product",
    library_name = "library",
    __product_name_slug = "product",
    __library_name_slug = "library",
    __project_name_slug = "pyproduct-library",
    requires_python = "3.7",
)


PYCOMMON_STRUCTURE = [
    ".coveragerc",
    ".flake8",
    ".github/workflows/ci_cd.yml",
    ".gitignore",
    ".pre-commit-config.yaml",
    "azure-pipelines.yml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "examples/README.md",
    "doc/Makefile",
    "doc/make.bat",
    "doc/source/conf.py",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
    "doc/source/_templates/sidebar-nav-bs.html",
    "doc/source/_templates/README.md",
    "LICENSE",
    "pyproject.toml",
    "README.rst",
    "setup.py",
    "requirements_build.txt",
    "requirements_doc.txt",
    "requirements_tests.txt",
    "tests/test_metadata.py",
    "tox.ini",
]

# Structure for pybasic projects
PYBASIC_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/{PYBASIC_VARS['project_name']}/__init__.py",
]
[PYBASIC_STRUCTURE.remove(file) for file in [".github/workflows/ci_cd.yml", ".pre-commit-config.yaml", "azure-pipelines.yml", "tox.ini"]]

# Structure for pyansys projects
PYANSYS_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
]
[PYANSYS_STRUCTURE.remove(file) for file in [".github/workflows/ci_cd.yml", "azure-pipelines.yml", "tox.ini"]]

# Structure for pyansys-advanced projects
PYANSYS_ADVANCED_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
]
[PYANSYS_ADVANCED_STRUCTURE.remove(file) for file in ["azure-pipelines.yml", "setup.py", ".coveragerc", "requirements_build.txt", "requirements_doc.txt", "requirements_tests.txt"]]

# A dictionary relating templates name with their variables and structure
TEMPLATES_VARIABLES_AND_STRUCTURE = {
    "common": [PYCOMMON_VARS, PYCOMMON_STRUCTURE],
    "pybasic": [PYBASIC_VARS, PYBASIC_STRUCTURE],
    "pyansys": [PYANSYS_VARS, PYANSYS_STRUCTURE],
    "pyansys_advanced": [PYANSYS_ADVANCED_VARS, PYANSYS_ADVANCED_STRUCTURE],
}


@pytest.mark.parametrize("build_system", ["flit", "poetry", "setuptools"])
@pytest.mark.parametrize("template", TEMPLATES_VARIABLES_AND_STRUCTURE)
def test_template_python(tmp_path, build_system, template):
    # Collect variables and expected structure
    VARIABLES, EXPECTED_STRUCTURE = TEMPLATES_VARIABLES_AND_STRUCTURE[template]

    # Collect some additional information
    template_path, outdir_name = (
        (TEMPLATE_PATH_FINDER[template], VARIABLES["__project_name_slug"])
        if template != "common" else (PYTHON_TEMPLATES_COMMON_PATH, "common")
    )
    project_path = tmp_path.joinpath(outdir_name)

    # Update variables if required
    if template == "pyansys_advanced":
        VARIABLES["build_system"] = build_system

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(template_path, tmp_path, VARIABLES)

    # The pyansys-advanced template does not ship with some files included in
    # the common/ directory
    if template == "pyansys_advanced" and build_system == "setuptools":
        EXPECTED_STRUCTURE.append("setup.py")
    elif template == "common":
        keep_files(EXPECTED_STRUCTURE, project_path)

    # Check that all common files are included in baked project
    assert_project_structure(EXPECTED_STRUCTURE, project_path)
