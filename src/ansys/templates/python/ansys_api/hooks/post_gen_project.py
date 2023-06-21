"""Hook to copy the .proto files into the project, and create __init__.py and py.typed files."""

from ansys.templates.utils import keep_files

src_path = "src/ansys/api/{{ cookiecutter.__product_name_slug }}"

if "{{ cookiecutter.__library_name_slug }}" != "":
    src_path += "/{{ cookiecutter.__library_name_slug }}"

DESIRED_STRUCTURE = [
    "README.md",
    "pyproject.toml",
    "setup.py",
    f"{src_path}/__init__.py",
    f"{src_path}/VERSION",
    f"{src_path}/py.typed",
    f"{src_path}/v0",
    ".github/workflows/ci.yml",
]
"""A list holding all desired files to be included in the project."""

def main():
    """Entry point of the script."""
    # Apply the desired structure to the project
    keep_files(DESIRED_STRUCTURE)

if __name__ == "__main__":
    main()
