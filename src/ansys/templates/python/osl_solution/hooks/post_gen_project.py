import shutil
import os
from pathlib import Path
from ansys.templates.utils import keep_files
import zipfile


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
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/osl_project_tree.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/utils.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/definition.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/monitoring_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/problem_setup_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/css/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/images/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/logos/ansys-solutions-horizontal-logo.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_information_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_logs_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_statistics_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/design_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/logs_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/project_summary_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/summary_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/system_files.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/monitoring_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/problem_setup_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/alerts.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/common_functions.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/constants.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/monitoring.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/placeholders.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/design_table_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/project_summary_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/result_files_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/scenery_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/status_overview_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/summary_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/visualization_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/app.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/__init__.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/main.py",
    "tests/common_test_files/README.md",
    "tests/integration/test_integration_dummy.py",
    "tests/unit/test_unit_dummy.py",
    "tests/conftest.py",
    ".codespell.exclude",
    ".codespell.ignore",
    ".env",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    "AUTHORS",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CODEOWNERS",
    "CONTRIBUTING.md",
    "CONTRIBUTORS.md",
    "LICENSE.rst",
    "poetry.lock",
    "pyproject.toml",
    "README.rst",
    "setup_environment.py",
    "tox.ini"
]
"""A list holding all desired files to be included in the project."""

ASSETS_DIRCTORY = Path(f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/model/assets/").absolute()


def unzip_archive(archive_path: Path, extract_path: Path) -> None:
    """Unzip an archive."""

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def copy_file_to_assets_folder(file_path: str, destination: str) -> None:
    """Copy a file if it exists."""

    if not os.path.isabs(file_path):
        working_directory = os.path.dirname(os.getcwd())
        file_path = os.path.join(working_directory, file_path)

    if os.path.exists(file_path):
        shutil.copy(file_path, destination)
    else:
        print(f"Unable to find {file_path}.")


def collect_files_with_extension(directory, extension):
    """
    Collects all files with the specified extension from a directory.
    Args:
        directory (str): The directory path.
        extension (str): The desired file extension.
    Returns:
        list: A list of file names with the specified extension.
    """
    files_with_extension = [file for file in os.listdir(directory) if file.endswith(extension)]
    return files_with_extension


def main():
    """Entry point of the script."""

    keep_files(DESIRED_STRUCTURE)

    if len("{{ cookiecutter.__optiSLang_application_archive }}".replace(" ", "")):
        unzip_archive("{{ cookiecutter.__optiSLang_application_archive }}", ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}")
        for file in ["metadata.json", "doc.md"]:
            copy_file_to_assets_folder(
                str(ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / file),
                str(ASSETS_DIRCTORY / file)
            )
        for extension in [".json", ".opf"]:
            candidates = collect_files_with_extension(str(ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / "custom_data"), extension)
            if len(candidates) == 0:
                raise Exception("The optiSLang application archive contains no project file (opf).")
            elif len(candidates) > 1:
                raise Exception("The optiSLang application archive contains multiple project files (opf).")
            else:
                candidate = "{{ cookiecutter.__optiSLang_application_archive_stem }}" + extension
                copy_file_to_assets_folder(
                    str(ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / "custom_data" / candidates[0]),
                    str(ASSETS_DIRCTORY / candidate)
                )
        shutil.rmtree(str(ASSETS_DIRCTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}"))

if __name__ == "__main__":
    main()
