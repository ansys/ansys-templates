"""Post-processing script for cleaning the raw rendered project."""
import os
from pathlib import Path

from ansys.templates.utils import keep_files

ALLOWED_BUILD_SYSTEMS = ["flit"]
"""A list of all allowed build systems by the template."""

DESIRED_STRUCTURE = [
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
    "yaml/{{ cookiecutter.yaml_file_name }}",
    "pom.xml"
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""

    # Get baked project location path
    project_path = Path(os.getcwd())

    # Get the desired build system
    build_system = "{{ cookiecutter.build_system }}"

    keep_files(DESIRED_STRUCTURE)


if __name__ == "__main__":
    main()
