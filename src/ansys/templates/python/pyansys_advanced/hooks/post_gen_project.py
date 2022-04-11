"""Post-processing script for cleaning the raw rendered project."""
import os
import shutil
from pathlib import Path

import isort

ALLOWED_BUILD_SYSTEMS = ["flit", "poetry", "setuptools"]
"""A list of all allowed build systems by the template."""


def main():
    """Entry point of the script."""
    # Get baked project location path
    project_path = Path(os.getcwd())

    # Get the desired build system
    build_system = "{{ cookiecutter.build_system }}"

    # Remove setup.py file if not required
    if build_system in ["flit", "poetry"]:
        setup_file = project_path / "setup.py"
        setup_file.unlink()

    # Remove .coveragerc as its content is specified in the pyproject.toml
    coveragerc_file = project_path / ".coveragerc"
    coveragerc_file.unlink()

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


if __name__ == "__main__":
    main()
