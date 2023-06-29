"""Post-processing script for cleaning the raw rendered project."""
import os
import shutil
from pathlib import Path

import isort

from ansys.templates.utils import keep_files, remove_file

ALLOWED_BUILD_SYSTEMS = ["flit", "poetry", "setuptools"]
"""A list of all allowed build systems by the template."""

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
    ".github/dependabot.yml",
    ".github/labeler.yml",
    ".github/labels.yml",
    ".github/workflows/ci_cd.yml",
    ".github/workflows/label.yml",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "README.rst",
    "src/ansys/{{ cookiecutter.__product_name_slug }}/{{ cookiecutter.__library_name_slug }}/__init__.py",
    "tests/test_metadata.py",
    "tox.ini",
]
"""A list holding all desired files to be included in the project."""

def main():
    """Entry point of the script."""
    # Get baked project location path
    project_path = Path(os.getcwd())

    # Get the desired build system
    build_system = "{{ cookiecutter.build_system }}"

    # Move all requirements files into a requirements/ directory
    requirements_files = [
        f"requirements_{name}.txt" for name in ["build", "doc", "tests"]
    ]
    if build_system == "poetry":
        # Poetry required and extra dependencies are collected inside the
        # 'pyproject.toml' file. Thus, there is no need to have requirements
        # files
        for file in requirements_files:
            remove_file(file, project_path)
    else:
        os.mkdir(project_path / "requirements")
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

    # Remove non-desired files
    if build_system == "setuptools":
        DESIRED_STRUCTURE.append("setup.py")
    keep_files(DESIRED_STRUCTURE)


if __name__ == "__main__":
    main()
