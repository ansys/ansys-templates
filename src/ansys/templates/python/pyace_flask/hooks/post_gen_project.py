"""Post-processing script for cleaning the raw rendered project."""
import os
import shutil
from pathlib import Path

import isort

from ansys.templates.utils import keep_files

ALLOWED_BUILD_SYSTEMS = ["flit", "poetry", "setuptools"]
"""A list of all allowed build systems by the template."""

DESIRED_STRUCTURE = [
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
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "README.rst",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
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
    "tests/test_metadata.py",
    "tests/test_server.py",
    "tests/conftest.py",
    "tox.ini",
    "docker-compose.yml",
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Get baked project location path
    project_path = Path(os.getcwd())

    # Get the desired build system
    build_system = "{{ cookiecutter.build_system }}"

    # Move all requirements files into a requirements/ directory
    os.mkdir(project_path / "requirements")
    requirements_files = [
        f"requirements_{name}.txt" for name in ["build", "doc", "tests"]
    ]
    for file in requirements_files:
        shutil.move(str(project_path / file), str(project_path / "requirements"))

    # Apply isort with desired config
    isort_config = isort.settings.Config(
        line_length="{{ cookiecutter.__max_linelength }}",
        profile="black",
    )
    filepaths_list = [
        project_path / "doc/source/conf.py",
    ]
    for filepath in filepaths_list:
        isort.api.sort_file(filepath, isort_config)

    # Remove ci/cd non-desired  files
    ci_cd = "{{ cookiecutter.ci_cd_platform }}"
    if ci_cd == 'GitHub':
        DESIRED_STRUCTURE.append(".github/workflows/ci_cd.yml")
    if ci_cd == 'Azure DevOps':
        DESIRED_STRUCTURE.append("azure-pipeline.yml")

    # Remove docker non desired files
    enable_docker = "{{ cookiecutter.enable_docker }}"
    if enable_docker == 'Yes':
        DESIRED_STRUCTURE.append("docker/Dockerfile")
        DESIRED_STRUCTURE.append("docker/README.md")


    # Remove non-desired files
    if build_system == "setuptools":
        DESIRED_STRUCTURE.append("setup.py")

    keep_files(DESIRED_STRUCTURE)


if __name__ == "__main__":
    main()
