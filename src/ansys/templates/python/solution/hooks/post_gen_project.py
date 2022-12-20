from ansys.templates.utils import keep_files


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
    "LICENSE.rst",
    "pyproject.toml",
    "README.rst",
    "requirements/requirements_build.txt",
    "requirements/requirements_doc.txt",
    "requirements/requirements_style.txt",
    "requirements/requirements_tests.txt",
    "setup_environment.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/__init__.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/main.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/definition.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/first_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/other_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/app.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/first.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/other.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/Graphics/ansys-solutions-horizontal-logo.png",
    "tests/conftest.py",
    "tests/common_test_files/README.md",
    "tests/integration/test_dummy.py",
    "tests/unit/test_dummy.py",
    "tox.ini",
    ".flake8",
    ".github/workflows/ci_cd.yml",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".vscode/launch.json",
]
"""A list holding all desired files to be included in the project."""


def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
