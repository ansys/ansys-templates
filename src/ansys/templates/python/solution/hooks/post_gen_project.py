from ansys.templates.utils import keep_files


DESIRED_STRUCTURE = [
    ".flake8",
    ".gitattributes",
    ".gitignore",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "pyproject.toml",
    "README.rst",
    "tox.ini",
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
