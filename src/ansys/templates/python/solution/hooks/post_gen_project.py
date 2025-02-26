from ansys.templates.utils import keep_files, rename_files
import shutil
import os

DESIRED_STRUCTURE = [
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
    "lock_files/awc/poetry.lock",
    "lock_files/dash/poetry.lock",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/datamodel/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/logic/assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/logic/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/portal_assets/application.svg",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/portal_assets/description.json",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/portal_assets/project.svg",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/method_assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/definition.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/first_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/second_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/__init__.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/main.py",
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
"""A list holding all desired files to be included in the project."""

UI_STRUCTURE = [
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/css/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/images/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/images/solution-workflow-sketch.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/logos/ansys_solutions_logo_black.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/logos/ansys_solutions_logo_white.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/about_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/first_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/second_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/app.py",
]


AWC_UI_STRUCTURE = [
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/css/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/images/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/images/solution-workflow-sketch.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/logos/ansys_solutions_logo_black.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/logos/ansys_solutions_logo_white.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/assets/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/components/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/pages/about_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/pages/first_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/pages/second_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/pages/page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui-awc/app.py",
]

# Add UI structure to desired structure if applicable
if "{{ cookiecutter.__frontend_type }}" == "dash":
    DESIRED_STRUCTURE = DESIRED_STRUCTURE + UI_STRUCTURE
elif "{{ cookiecutter.__frontend_type }}" == "awc-dash":
    DESIRED_STRUCTURE = DESIRED_STRUCTURE + AWC_UI_STRUCTURE
if "{{ cookiecutter.__frontend_type }}" != "dash":
    DESIRED_STRUCTURE.remove("poetry.lock")


def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)
    if "{{ cookiecutter.__frontend_type }}" == "awc-dash":
        combined_structure = list(zip(AWC_UI_STRUCTURE, UI_STRUCTURE))
        rename_files(combined_structure)
        shutil.copy(os.path.join("lock_files", "awc", "poetry.lock"), ".")
    elif "{{ cookiecutter.__frontend_type }}" == "dash":
        shutil.copy(os.path.join("lock_files", "dash", "poetry.lock"), ".")
    shutil.rmtree("lock_files")

if __name__ == "__main__":
    main()
