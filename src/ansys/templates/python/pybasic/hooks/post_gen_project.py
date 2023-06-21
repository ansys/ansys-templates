from ansys.templates.utils import keep_files

DESIRED_STRUCTURE = [
    "README.md",
    "pyproject.toml",
    "setup.py",
    "src/ansys/api/{{ cookiecutter.__project_name_slug }}/__init__.py",
    "src/ansys/api/{{ cookiecutter.__project_name_slug }}/VERSION",
    "src/ansys/api/{{ cookiecutter.__project_name_slug }}/py.typed",
    "src/ansys/api/{{ cookiecutter.__project_name_slug }}/v0",
]
"""A list holding all desired files to be included in the project."""

def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
