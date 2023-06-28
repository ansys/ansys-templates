from ansys.templates.utils import keep_files

DESIRED_STRUCTURE = [
    ".coveragerc",
    ".flake8",
    ".gitattributes",
    ".gitignore",
    ".pre-commit-config.yaml",
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
    "LICENSE",
    "pyproject.toml",
    "README.rst",
    "requirements_build.txt",
    "requirements_doc.txt",
    "requirements_tests.txt",
    "setup.py",
    "src/ansys/{{ cookiecutter.__product_name_slug }}/{{ cookiecutter.__library_name_slug }}/__init__.py",
    "tests/test_metadata.py",
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
