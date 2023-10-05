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
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/datamodel/datamodel.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/logic/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/logic/assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/pim_configurations/osl_wrapper.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/pim_configurations/pim_osl_configuration.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/method_assets/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/definition.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/problem_setup_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/monitoring_step.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/optislang_manager.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/css/style.css",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/images/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/logos/ansys-solutions-horizontal-logo.png",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/assets/scripts/README.md",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_information_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_logs_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/actor_statistics_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/button_group.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/node_control.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/design_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/logs_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/components/project_information_table.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/monitoring_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/pages/problem_setup_page.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/utils/alerts.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/design_table_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/project_summary_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/scenery_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/status_overview_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/summary_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/views/visualization_view.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/ui/app.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/utilities/common_functions.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/__init__.py",
    f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/main.py",
    "telemetry/grafana/compose.yaml",
    "telemetry/grafana/_deploy/compose/collector/otel-collector-config.yaml",
    "telemetry/grafana/_deploy/compose/grafana/grafana-dashboard.json",
    "telemetry/grafana/_deploy/compose/grafana/grafana-dashboards.yml",
    "telemetry/grafana/_deploy/compose/grafana/grafana-datasources.yml",
    "telemetry/grafana/_deploy/compose/grafana/grafana.ini",
    "telemetry/grafana/_deploy/compose/loki/loki.yml",
    "telemetry/grafana/_deploy/compose/prometheus/prometheus.yml",
    "telemetry/tracelens/compose.yaml",
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

LOGIC_ASSETS_DIRECTORY = Path(f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/logic/assets").absolute()
METHOD_ASSETS_DIRECTORY = Path(f"src/ansys/solutions/{{ cookiecutter.__solution_name_slug }}/solution/method_assets/Problem_Setup").absolute()

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
        archive_path = Path("{{ cookiecutter.__optiSLang_application_archive }}".strip())

        if not archive_path.is_absolute():
            raise Exception("Relative path not allowed, please provide the absolute path of the owa archive.")
        if not archive_path.exists():
            raise Exception(f"File not found: {archive_path}")

        unzip_archive(archive_path, METHOD_ASSETS_DIRECTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}")

        for file in ["metadata.json", "doc.md"]:
            copy_file_to_assets_folder(
                str(METHOD_ASSETS_DIRECTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / file),
                str(METHOD_ASSETS_DIRECTORY / file)
            )
        for extension in [".json", ".opf"]:
            candidates = collect_files_with_extension(str(METHOD_ASSETS_DIRECTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / "custom_data"), extension)
            if len(candidates) == 0:
                raise Exception("The optiSLang application archive contains no project file (opf).")
            elif len(candidates) > 1:
                raise Exception("The optiSLang application archive contains multiple project files (opf).")
            else:
                candidate = "{{ cookiecutter.__optiSLang_application_archive_stem }}" + extension
                if extension == ".json":
                    destination_folder = METHOD_ASSETS_DIRECTORY
                if extension == ".opf":
                    destination_folder = LOGIC_ASSETS_DIRECTORY
                copy_file_to_assets_folder(
                    str(METHOD_ASSETS_DIRECTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}" / "custom_data" / candidates[0]),
                    str(destination_folder / candidate)
                )
        shutil.rmtree(str(METHOD_ASSETS_DIRECTORY / "{{ cookiecutter.__optiSLang_application_archive_stem }}"))


if __name__ == "__main__":
    main()
