# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    requires_python="3.9",
)

PYANSYS_VARS = PYANSYS_ADVANCED_VARS = dict(
    product_name="product",
    library_name="library",
    __product_name_slug="product",
    __library_name_slug="library",
    __project_name_slug="pyproduct-library",
    requires_python="3.9",
)

PYANSYS_OPENAPI_VARS = dict(
    product_name="product",
    library_name="library",
    __product_name_slug="product",
    __library_name_slug="library",
    __project_name_slug="pyproduct-library-openapi",
    requires_python="3.9",
)

PYACE_VARS = dict(
    project_name="my_company",
    library_name="library",
    ci_cd_platform="GitHub",
    copyright="My Company",
    enable_docker="Yes",
    __project_name_slug = "project",
    requires_python="3.9",
)

DOC_PROJECT_VARS = dict(
    project_name="doc-project",
    __project_name_slug = "doc-project",
    logo="Ansys",
    logo_color="black",
    requires_python="3.9",
)

SOLUTION_VARS = dict(
    __solution_name_slug="solution",
    __project_name_slug="solution",
    dash_ui="default",
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
    "AUTHORS",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CONTRIBUTORS.md",
    "examples/README.md",
    "doc/changelog.d/changelog_template.jinja",
    "doc/Makefile",
    "doc/make.bat",
    "doc/.vale.ini",
    "doc/styles/.gitignore",
    "doc/styles/config/vocabularies/ANSYS/accept.txt",
    "doc/styles/config/vocabularies/ANSYS/reject.txt",
    "doc/source/getting_started/index.rst",
    "doc/source/changelog.rst",
    "doc/source/conf.py",
    "doc/source/examples.rst",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
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
 [".github/dependabot.yml", ".github/labeler.yml", ".github/labels.yml", ".github/workflows/label.yml", ".github/workflows/ci_cd.yml", "doc/changelog.d/changelog_template.jinja", ".pre-commit-config.yaml", "azure-pipeline.yml", "tox.ini"]]

# Structure for pyansys projects
PYANSYS_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
]
[PYANSYS_STRUCTURE.remove(file) for file in [".github/dependabot.yml", ".github/labeler.yml", ".github/labels.yml", ".github/workflows/label.yml", ".github/workflows/ci_cd.yml", "doc/changelog.d/changelog_template.jinja", "azure-pipeline.yml", "tox.ini"]]

# Structure for pyansys-advanced projects
PYANSYS_ADVANCED_STRUCTURE = deepcopy(PYCOMMON_STRUCTURE) + [
    f"src/ansys/{PYANSYS_VARS['__product_name_slug']}/{PYANSYS_VARS['__library_name_slug']}/__init__.py",
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
    "docker/compose.yaml",
    "docker/Dockerfile",
    "docker/Docker.md",
    ".dockerignore",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "tests/test_server.py",
    "tests/conftest.py"
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
    "docker/compose.yaml",
    "docker/Dockerfile",
    "docker/Docker.md",
    ".dockerignore",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "tests/test_server.py",
    "tests/conftest.py"
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
    "docker/compose.yaml",
    "docker/Dockerfile",
    "docker/Docker.md",
    ".dockerignore",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "protobufs/pingserver.proto",
    "tests/test_server.py",
    "tests/conftest.py",
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
    "docker/compose.yaml",
    "docker/Dockerfile",
    "docker/Docker.md",
    ".dockerignore"
]
[PYACE_PKG_STRUCTURE.remove(file) for file in
 ["azure-pipeline.yml", ".coveragerc", "requirements_build.txt", "requirements_doc.txt",
  "requirements_tests.txt"]]

PYANSYS_OPENAPI_STRUCTURE = [
    "AUTHORS",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CONTRIBUTORS.md",
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
    "doc/changelog.d/changelog_template.jinja",
    "doc/styles/.gitignore",
    "doc/styles/config/vocabularies/ANSYS/accept.txt",
    "doc/styles/config/vocabularies/ANSYS/reject.txt",
    "doc/source/getting_started/index.rst",
    "doc/source/changelog.rst",
    "doc/source/conf.py",
    "doc/source/examples.rst",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
    "doc/source/_templates/README.md",
    "examples/README.md",
    ".github/dependabot.yml",
    ".github/labeler.yml",
    ".github/labels.yml",
    ".github/workflows/ci_cd.yml",
    ".github/workflows/label.yml",
    ".gitignore",
    "LICENSE",
    "README.rst",
    ".pre-commit-config.yaml",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "tox.ini",
]

# Structure for solution projects
SOLUTION_STRUCTURE = [
    ".devcontainer/devcontainer.json",
    ".github/workflows/build-release.yml",
    ".github/workflows/release-please.yml",
    ".github/workflows/label.yml",
    ".github/labeler.yml",
    ".github/labels.yml",
    ".vscode/launch.json",
    ".vscode/extensions.json",
    "deployments/dev/.env",
    "deployments/dev/compose-dev.yaml",
    "deployments/dev/Dockerfile-dev",
    "doc/changelog.d/changelog_template.jinja",
    "doc/source/_static/css/custom.css",
    "doc/source/_static/images/repository-banner.png",
    "doc/source/_templates/README.md",
    "doc/source/getting_started/index.rst",
    "doc/source/getting_started/desktop_installation.rst",
    "doc/source/getting_started/docker_installation.rst",
    "doc/source/user_guide/index.rst",
    "doc/source/changelog.rst",
    "doc/source/conf.py",
    "doc/source/examples.rst",
    "doc/source/index.rst",
    "doc/styles/config/vocabularies/ANSYS/accept.txt",
    "doc/styles/config/vocabularies/ANSYS/reject.txt",
    "doc/styles/.gitignore",
    "doc/.vale.ini",
    "doc/make.bat",
    "doc/Makefile",
    "examples/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/datamodel/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/logic/assets/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/logic/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/solution/method_assets/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/solution/definition.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/solution/first_step.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/solution/second_step.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/__init__.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/main.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/css/style.css",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/images/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/images/solution-workflow-sketch.png",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/logos/ansys_solutions_logo_black.png",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/logos/ansys_solutions_logo_white.png",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/assets/scripts/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/components/README.md",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/pages/about_page.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/pages/first_page.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/pages/second_page.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/pages/page.py",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/portal_assets/application.svg",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/portal_assets/project.svg",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/portal_assets/description.json",
    f"src/ansys/solutions/{SOLUTION_VARS['__solution_name_slug']}/ui/app.py",
    "telemetry/grafana/compose.yaml",
    "telemetry/grafana/_deploy/compose/collector/otel-collector-config.yaml",
    "telemetry/grafana/_deploy/compose/grafana/grafana-dashboard.json",
    "telemetry/grafana/_deploy/compose/grafana/grafana-dashboards.yml",
    "telemetry/grafana/_deploy/compose/grafana/grafana-datasources.yml",
    "telemetry/grafana/_deploy/compose/grafana/grafana.ini",
    "telemetry/grafana/_deploy/compose/loki/loki.yml",
    "telemetry/grafana/_deploy/compose/prometheus/prometheus.yml",
    "telemetry/tracelens/compose.yaml",
    "tests/common_test_files/README.md",
    "tests/integration/test_integration_dummy.py",
    "tests/unit/test_unit_dummy.py",
    "tests/conftest.py",
    ".env",
    ".codespell.ignore",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    "AUTHORS",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CODEOWNERS",
    "CONTRIBUTING.md",
    "CONTRIBUTORS.md",
    "LICENSE.rst",
    "poetry.lock",
    "pyproject.toml",
    "README.md",
    "setup_environment.py",
    "sonar-project.properties",
    "tox.ini",
    "release-please-config.json",
    "release-please-manifest.json"
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
    "solution": [SOLUTION_VARS, SOLUTION_STRUCTURE],
}


@pytest.mark.parametrize("build_system", ["flit", "poetry", "setuptools"])
@pytest.mark.parametrize("template", TEMPLATES_VARIABLES_AND_STRUCTURE)
def test_template_python(tmp_path, build_system, template):

    # Get the list of supported build systems for the template
    template_path = TEMPLATE_PATH_FINDER[template]
    with open(template_path / "cookiecutter.json", 'r', encoding="utf-8") as fp:
        config_json = json.load(fp)
    default_build_system = "setuptools" if template != "solution" else "poetry"
    supported_build_systems = config_json.get("build_system", [default_build_system])

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
