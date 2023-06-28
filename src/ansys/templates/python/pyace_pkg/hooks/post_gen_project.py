"""Post-processing script for cleaning the raw rendered project."""
import os
import shutil
from pathlib import Path

import isort

from ansys.templates.utils import keep_files

DESIRED_STRUCTURE = [
    "AUTHORS",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CONTRIBUTORS.md",
    "doc/Makefile",
    "doc/make.bat",
    "doc/.vale.ini",
    "doc/styles/.gitignore",
    "doc/styles/Vocab/ANSYS/accept.txt",
    "doc/styles/Vocab/ANSYS/reject.txt",
    "doc/source/conf.py",
    "doc/source/index.rst",
    "doc/source/_static/README.md",
    "doc/source/_templates/README.md",
    "examples/README.md",
    ".flake8",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "README.rst",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_tests.txt",
    "setup.py",
    "src/__init__.py",
    "src/logger.py",
    "src/main.py",
    "tests/test_metadata.py",
    "tox.ini",
    "tests/__init__.py",
    "tests/conftest.py"
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Get baked project location path
    project_path = Path(os.getcwd())

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
        DESIRED_STRUCTURE.extend(
            [
                ".github/dependabot.yml",
                ".github/labeler.yml",
                ".github/labels.yml",
                ".github/workflows/ci_cd.yml",
                ".github/workflows/label.yml",
            ]
        )
    if ci_cd == 'Azure DevOps':
        DESIRED_STRUCTURE.append("azure-pipeline.yml")

    # Remove docker non desired files
    enable_docker = "{{ cookiecutter.enable_docker }}"
    if enable_docker == 'Yes':
        DESIRED_STRUCTURE.append("docker/compose.yaml")
        DESIRED_STRUCTURE.append("docker/Dockerfile")
        DESIRED_STRUCTURE.append("docker/Docker.md")
        DESIRED_STRUCTURE.append(".dockerignore")

    # Remove non-desired files
    keep_files(DESIRED_STRUCTURE)


if __name__ == "__main__":
    main()
