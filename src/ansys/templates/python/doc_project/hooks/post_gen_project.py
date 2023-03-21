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
    "doc/.vale.ini",
    "doc/styles/.gitignore",
    "doc/styles/Vocab/ANSYS/accept.txt",
    "doc/styles/Vocab/ANSYS/reject.txt",
    "doc/source/conf.py",
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
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Get baked project location path
    project_path = Path(os.getcwd())

    # Move all requirements files into a requirements/ directory
    os.mkdir(project_path / "requirements")
    requirements_files = [
            f"requirements_{name}.txt" for name in ["build", "doc"]
    ]
    for file in requirements_files:
        shutil.move(str(project_path / file), str(project_path / "requirements"))

    # Apply isort with desired config
    isort_config = isort.settings.Config(
        line_length="{{ cookiecutter.__max_linelength }}",
        profile="black",
    )
    filepaths_list = [
        project_path / "doc" / "source" / "conf.py",
    ]
    for filepath in filepaths_list:
        isort.api.sort_file(filepath, config=isort_config)

    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
