import shutil
import os
from pathlib import Path
from ansys.templates.utils import keep_files


DESIRED_STRUCTURE = [
    ".github/workflows/ci.yml",
    ".vscode/launch.json",
    "doc/source/_static/ansys-solutions-logo-black-background.png",
    "doc/source/_static/README.md",
    "doc/source/_templates/README.md",
    "doc/source/conf.py",
    "doc/source/index.rst",
    "doc/styles/Vocab/ANSYS/accept.txt",
    "doc/styles/Vocab/ANSYS/reject.txt",
    "doc/styles/.gitignore",
    "doc/.vale.ini",
    "doc/make.bat",
    "doc/Makefile",
    "examples/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/definition.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/monitoring_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/problem_setup_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/__init__.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/main.py",
    "tests/common_test_files/README.md",
    "tests/integration/test_integration_dummy.py",
    "tests/unit/test_unit_dummy.py",
    "tests/conftest.py",
    ".codespell.exclude",
    ".codespell.ignore",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CODEOWNERS",
    "CONTRIBUTING.md",
    "LICENSE.rst",
    "pyproject.toml",
    "README.rst",
    "setup_environment.py",
    "tox.ini"
]
"""A list holding all desired files to be included in the project."""

UI_STRUCTURE = [
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/Graphics/ansys-solutions-horizontal-logo.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/design_table_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/project_summary_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/result_files_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/scenery_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/status_overview_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/summary_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_tabs/visualization_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/app.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/monitoring_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/problem_setup_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/page.py"
]

ASSETS_DIRCTORY = Path(f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/assets/").absolute()

# Add UI structure to desired structure if applicable
if "{{ cookiecutter.with_dash_ui }}" == "yes":
    DESIRED_STRUCTURE = DESIRED_STRUCTURE + UI_STRUCTURE


def copy_file_to_assets_folder(file, des):
    """Copy a file if it exists."""

    if os.path.exists(file):
        shutil.copy(file, des)


def main():
    """Entry point of the script."""

    keep_files(DESIRED_STRUCTURE)

    copy_file_to_assets_folder("{{ cookiecutter.__optiSLang_project_file }}",  ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_project_file_name }}")
    copy_file_to_assets_folder("{{ cookiecutter.__optiSLang_properties_file }}", ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_properties_file_name }}")


if __name__ == "__main__":
    main()
