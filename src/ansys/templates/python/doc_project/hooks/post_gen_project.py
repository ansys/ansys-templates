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
    "doc/source/_templates/sidebar-nav-bs.html",
    "doc/source/_templates/README.md",
    "examples/README.md",
    ".flake8",
    ".gitignore",
    "LICENSE",
    "pyproject.toml",
    "README.rst",
    "requirements_build.txt",
    "requirements_doc.txt",
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Get the desired build system
    build_system = "{{ cookiecutter.build_system }}"

    # Remove non-desired files
    if build_system == "setuptools":
        DESIRED_STRUCTURE.append("setup.py")

    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
