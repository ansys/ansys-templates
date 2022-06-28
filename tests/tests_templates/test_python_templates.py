from copy import deepcopy
import json

import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH, TEMPLATE_PATH_FINDER
from ansys.templates.testing import assert_project_structure, assert_template_baking_process
from ansys.templates.utils import keep_files

PYCOMMON_VARS = dict(
    __project_name_slug="common"
)

PYBASIC_VARS = dict(
    project_name="pybasic",
    __project_name_slug="pybasic",
    short_description="A basic Python Package",
    repository_url="https://platform.domain/organization/pybasic",
    requires_python="3.7",
)

PYANSYS_VARS = PYANSYS_ADVANCED_VARS = dict(
    product_name="product",
    library_name="library",
    __product_name_slug="product",
    __library_name_slug="library",
    __project_name_slug="pyproduct-library",
    requires_python="3.7",
)

PYANSYS_OPENAPI_VARS = dict(
    product_name="product",
    library_name="library",
    __product_name_slug="product",
    __library_name_slug="library",
    __project_name_slug="pyproduct-library-openapi",
    requires_python="3.7",
)

PYACE_VARS = dict(
    project_name="my_company",
    library_name="library",
    ci_cd_platform="GitHub",
    copyright="My Company",
    enable_docker="Yes",
    __project_name_slug = "project",
    requires_python="3.7",
)

DOC_PROJECT_VARS = dict(
    project_name="doc-project",
    __project_name_slug = "doc-project",
    logo="Ansys",
    logo_color="black",
    requires_python="3.7",
)


PYCOMMON_STRUCTURE = [
    ".coveragerc",
    ".flake8",
    ".github/dependabot.yml",
    ".github/labeler.yml",
    ".github/labels.yml",
    ".github/workflows/ci_cd.yml",
    ".github/workflows/label.yml",
    ".gitattributes",
    ".gitignore",
    ".pre-commit-config.yaml",
    "azure-pipeline.yml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "examples/README.md",
    "doc/Makefile",
    "doc/make.bat",
    "doc/.vale.ini",
    "doc/styles/.gitignore",
    "doc/styles/Vocab/ANSYS/accept.txt",
    "doc/styles/Vocab/ANSYS/reject.txt",
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
[PYBASIC_STRUCTURE.remove(file) for file in
 [".github/dependabot.yml", ".github/labeler.yml", ".github/labels.yml", ".github/workflows/label.yml", ".github/workflows/ci_cd.yml", ".pre-commit-config.yaml", "azure-pipeline.yml", "tox.ini"]]

# Structure for pyansys projects
PYANSYS_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
]
[PYANSYS_STRUCTURE.remove(file) for file in [".github/dependabot.yml", ".github/labeler.yml", ".github/labels.yml", ".github/workflows/label.yml", ".github/workflows/ci_cd.yml", "azure-pipeline.yml", "tox.ini"]]

# Structure for pyansys-advanced projects
PYANSYS_ADVANCED_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
]
[PYANSYS_ADVANCED_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", "setup.py", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYACE_FLASK_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    "src/__init__.py",
    "src/_version.py",
    "src/server.py",
    "src/blueprints/__init__.py",
    "src/blueprints/health.py",
    "src/blueprints/version.py",
    "src/models/__init__.py",
    "src/observability/__init__.py",
    "src/observability/logger.py",
    "src/static/swagger.json",
    "docker/Dockerfile",
    "docker/README.md",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "tests/test_server.py",
    "tests/conftest.py",
    "docker-compose.yml",
]
[PYACE_FLASK_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYACE_FAST_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    "src/__init__.py",
    "src/_version.py",
    "src/server.py",
    "src/models/__init__.py",
    "src/observability/logger.py",
    "docker/Dockerfile",
    "docker/README.md",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "tests/test_server.py",
    "tests/conftest.py",
    "docker-compose.yml",
]
[PYACE_FAST_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYACE_GRPC_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    "src/__init__.py",
    "src/_version.py",
    "src/server.py",
    "src/client.py",
    "src/observability/logger.py",
    "src/services/__init__.py",
    "src/services/pinger.py",
    "src/stubs/__init__.py",
    "docker/Dockerfile",
    "docker/README.md",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "protobufs/pingserver.proto",
    "tests/test_server.py",
    "tests/conftest.py",
    "docker-compose.yml",
]
[PYACE_GRPC_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYACE_PKG_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    "src/__init__.py",
    "src/logger.py",
    "src/main.py",
    "tests/__init__.py",
    "tests/conftest.py",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "Dockerfile",
    "docker-compose.yaml",
]
[PYACE_PKG_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYANSYS_OPENAPI_STRUCTURE = [
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    ".flake8",
    ".github/workflows/build_and_test_library.yml",
    ".github/workflows/generate_library.yml",
    ".github/dependabot.yml",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    ".pre-commit-config.yaml",
    ".m2/settings.xml",
    "yaml/library.yaml",
    "pom.xml"
]

DOC_PROJECT_STRUCTURE = [
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "doc/Makefile",
    "doc/make.bat",
    "doc/.vale.ini",
    "doc/styles/.gitignore",
    "doc/styles/Vocab/ANSYS/accept.txt",
    "doc/styles/Vocab/ANSYS/reject.txt",
    "doc/source/conf.py",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
    "doc/source/_templates/sidebar-nav-bs.html",
    "doc/source/_templates/README.md",
    "examples/README.md",
    ".gitignore",
    "LICENSE",
    "README.rst",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
]

# A dictionary relating templates name with their variables and structure
TEMPLATES_VARIABLES_AND_STRUCTURE = {
    "common": [PYCOMMON_VARS, PYCOMMON_STRUCTURE],
    "pybasic": [PYBASIC_VARS, PYBASIC_STRUCTURE],
    "pyansys": [PYANSYS_VARS, PYANSYS_STRUCTURE],
    "pyansys-advanced": [PYANSYS_ADVANCED_VARS, PYANSYS_ADVANCED_STRUCTURE],
    "pyansys-openapi-client": [PYANSYS_OPENAPI_VARS, PYANSYS_OPENAPI_STRUCTURE],
    "pyace-flask": [PYACE_VARS, PYACE_FLASK_STRUCTURE],
    "pyace-grpc": [PYACE_VARS, PYACE_GRPC_STRUCTURE],
    "pyace-fast": [PYACE_VARS, PYACE_FAST_STRUCTURE],
    "pyace": [PYACE_VARS, PYACE_PKG_STRUCTURE],
    "doc-project": [DOC_PROJECT_VARS, DOC_PROJECT_STRUCTURE],
}


@pytest.mark.parametrize("build_system", ["flit", "poetry", "setuptools"])
@pytest.mark.parametrize("template", TEMPLATES_VARIABLES_AND_STRUCTURE)
def test_template_python(tmp_path, build_system, template):

    # Get the list of supported build systems for the template
    template_path = TEMPLATE_PATH_FINDER[template]
    with open(template_path / "cookiecutter.json", 'r', encoding="utf-8") as fp:
        config_json = json.load(fp)
    supported_build_systems = config_json.get("build_system", ["setuptools"])

    # Skip if template does not support a particular build system
    if build_system not in supported_build_systems:
        pytest.skip(f"Template {template} does not support {build_system}.")

    # Collect variables and expected structure
    VARIABLES, EXPECTED_STRUCTURE = TEMPLATES_VARIABLES_AND_STRUCTURE[template]

    # Collect some additional information
    template_path, outdir_name = (
        (TEMPLATE_PATH_FINDER[template], VARIABLES["__project_name_slug"])
        if template != "common" else (PYTHON_TEMPLATES_COMMON_PATH, "common")
    )
    project_path = tmp_path.joinpath(outdir_name)

    # Update variables if required
    if template == "pyansys-advanced":
        VARIABLES["build_system"] = build_system

    # Assert no errors were raised during template rendering process
    assert_template_baking_process(template_path, tmp_path, VARIABLES)

    # The pyansys-advanced template does not ship with some files included in
    # the common/ directory
    if template == "pyansys-advanced" and build_system == "setuptools":
        EXPECTED_STRUCTURE.append("setup.py")
    elif template == "common":
        keep_files(EXPECTED_STRUCTURE, project_path)

    # Check that all common files are included in baked project
    assert_project_structure(EXPECTED_STRUCTURE, project_path)
