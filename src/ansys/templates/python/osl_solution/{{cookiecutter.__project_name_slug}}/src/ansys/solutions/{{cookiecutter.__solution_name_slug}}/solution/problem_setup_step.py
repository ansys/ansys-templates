# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
from pathlib import Path
import platform
import time
from typing import List
import subprocess
import sys

from ansys.optislang.core import Optislang, logging
from ansys.saf.glow.solution import FileReference, AssetFileReference, StepModel, StepSpec, long_running, transaction
from ansys.solutions.optislang.frontend_components.project_properties import ProjectProperties, write_properties_file, apply_placeholders_to_properties_file
from ansys.solutions.products_ecosystem.controller import AnsysProductsEcosystemController
from ansys.solutions.products_ecosystem.utils import convert_to_long_version

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.model.osl_project_tree import dump_project_state, get_project_tree, get_node_list, get_step_list
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.monitoring import _get_actor_hids, read_optislang_logs


class ProblemSetupStep(StepModel):
    """Step model of the problem setup step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    ansys_ecosystem_ready: bool = False
    optislang_solve_status: str = "initial"  # initial, processing, finished, stopped, aborted, idle
    ui_placeholders: dict = {}
    app_metadata: dict = {}
    analysis_running: bool = False

    # Backend data model
    tcp_server_host: str = "127.0.0.1"
    tcp_server_port: int = None
    ansys_ecosystem: dict = {
        "optislang": {
            "authorized_versions": ["2022.2", "2023.1"],
            "installed_versions": [],
            "compatible_versions": [],
            "selected_version": None,
            "alert_message": "OptiSLang install not checked.",
            "alert_color": "warning",
            "alias": "optiSLang",
        }
    }
    step_list: list = []
    node_list: list = []
    placeholders: dict = {}
    registered_files: List = []
    settings: dict = {}
    parameter_manager: dict = {}
    criteria: dict = {}
    project_status_info: dict = {}
    actors_info: dict = {}
    actors_status_info: dict = {}
    results_files: dict = {}
    tcp_server_stopped_states = ["idle", "finished", "stopped", "aborted"]
    optislang_logs: list = []
    optislang_log_level: str = "INFO"
    project_initialized: bool = False
    has_project_state: bool = False

    # File storage ----------------------------------------------------------------------------------------------------

    # Inputs
    project_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.opf")
    properties_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.json")
    metadata_file: FileReference = FileReference("Problem_Setup/metadata.json")
    project_state_file: FileReference = FileReference("Problem_Setup/project_state.json")

    # Outputs
    working_properties_file: FileReference = FileReference("Problem_Setup/working_properties_file.json")
    server_info_file: FileReference = FileReference("Problem_Setup/server_info.ini")
    optislang_log_file: FileReference = FileReference("Problem_Setup/pyoptislang.log")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        self=StepSpec(
            upload=["has_project_state"]
        )
    )
    def generate_project_state(self) -> None:
        """Generate a project state from an optiSLang opf file."""

        project_file = Path(__file__).absolute().parent.parent / "model" / "assets" / "{{ cookiecutter.__optiSLang_application_archive_stem }}.opf"

        dump_project_state(project_file, Path(project_file).parent / "project_state.json")

        self.has_project_state = True

    @transaction(
        self=StepSpec(
            download=["project_state_file"],
            upload=["step_list", "node_list"]
        )
    )
    def read_project_tree(self) -> None:
        """Read project tree from optiSLang project state file."""

        project_tree = get_project_tree(self.project_state_file.path)
        self.step_list = get_step_list(project_tree)
        self.node_list = get_node_list(project_tree)

    @transaction(
        self=StepSpec(
            upload=[
                "project_file",
                "properties_file",
                "metadata_file",
                "project_state_file",
            ]
        )
    )
    def upload_bulk_files_to_project_directory(self) -> None:
        """Upload bulk files to project directory."""

        original_project_file = Path(__file__).parent.absolute().parent / "model" / "assets" / "{{ cookiecutter.__optiSLang_application_archive_stem }}.opf"
        self.project_file.write_bytes(original_project_file.read_bytes())

        original_properties_file = (
            Path(__file__).parent.absolute().parent / "model" / "assets" / "{{ cookiecutter.__optiSLang_application_archive_stem }}.json"
        )
        self.properties_file.write_bytes(original_properties_file.read_bytes())

        original_metadata_file = Path(__file__).parent.absolute().parent / "model" / "assets" / "metadata.json"
        self.metadata_file.write_bytes(original_metadata_file.read_bytes())

        original_project_state_file = Path(__file__).parent.absolute().parent / "model" / "assets" / "project_state.json"
        self.project_state_file.write_bytes(original_project_state_file.read_bytes())

    @transaction(
        self=StepSpec(
            upload=["ansys_ecosystem", "ansys_ecosystem_ready"],
        )
    )
    def check_ansys_ecosystem(self) -> None:
        """Check if Ansys Products are installed and if the appropriate versions are available."""

        self.ansys_ecosystem_ready = True

        controller = AnsysProductsEcosystemController()

        for product_name in self.ansys_ecosystem.keys():

            self.ansys_ecosystem[product_name]["installed_versions"] = controller.get_installed_versions(
                product_name, outout_format="long"
            )
            self.ansys_ecosystem[product_name]["compatible_versions"] = [
                product_version
                for product_version in self.ansys_ecosystem[product_name]["installed_versions"]
                if product_version in self.ansys_ecosystem[product_name]["authorized_versions"]
            ]

            if len(self.ansys_ecosystem[product_name]["installed_versions"]) == 0:
                alert_message = f"No installation of {product_name.title()} found in the machine {platform.node()}."
                alert_color = "danger"
                self.ansys_ecosystem_ready = False
            elif len(self.ansys_ecosystem[product_name]["compatible_versions"]) == 0:
                alert_message = (
                    f"None of the authorized versions of {product_name.title()} "
                    f"is installed in the machine {platform.node()}.\n"
                )
                alert_message += "At least one of these versions is required:"
                for authorized_version in self.ansys_ecosystem[product_name]["authorized_versions"]:
                    self.ansys_ecosystem[product_name][
                        "alert_message"
                    ] += f" {convert_to_long_version(authorized_version)}"
                alert_message += "."
                alert_color = "danger"
                self.ansys_ecosystem_ready = False
            else:
                self.ansys_ecosystem[product_name]["selected_version"] = self.ansys_ecosystem[product_name][
                    "compatible_versions"
                ][
                    -1
                ]  # Latest
                alert_message = f"{product_name.title()} install detected. Compatible versions are:"
                for compatible_version in self.ansys_ecosystem[product_name]["compatible_versions"]:
                    alert_message += f" {convert_to_long_version(compatible_version)}"
                alert_message += ".\n"
                alert_message += "Selected version is %s." % (self.ansys_ecosystem[product_name]["selected_version"])
                alert_color = "success"
            self.ansys_ecosystem[product_name]["alert_message"] = alert_message
            self.ansys_ecosystem[product_name]["alert_color"] = alert_color

    @transaction(self=StepSpec(download=["properties_file"], upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"]))
    def get_default_placeholder_values(self):
        """Get placeholder values and definitions using the ProjectProperties class."""

        pp = ProjectProperties()
        pp.read_file(self.properties_file.path)
        self.placeholders = pp._placeholders
        self.registered_files = pp._registered_files
        self.settings = pp._settings
        self.parameter_manager = pp._parameter_manager
        self.criteria = pp._criteria

    @transaction(self=StepSpec(download=["properties_file", "ui_placeholders"], upload=["working_properties_file"]))
    def write_updated_properties_file(self) -> None:
        properties = apply_placeholders_to_properties_file(self.ui_placeholders, self.properties_file.path)
        write_properties_file(properties, Path(self.working_properties_file.path))

    @transaction(
        self=StepSpec(
            download=["metadata_file"],
            upload=["app_metadata"]
        )
    )
    def get_app_metadata(self) -> None:
        """Read OWA metadata file."""

        with open(self.metadata_file.path) as f:
            self.app_metadata = json.load(f)

    @transaction(
        self=StepSpec(
            download=[
                "project_file",
                "working_properties_file",
                "tcp_server_stopped_states",
                "optislang_log_level",
                "node_list",
            ],
            upload=[
                "optislang_solve_status",
                "server_info_file",
                "actors_info",
                "actors_status_info",
                "tcp_server_port",
                "project_status_info",
                "results_files",
                "optislang_log_file",
                "optislang_logs",
            ],
        )
    )
    @long_running
    def start_analysis(self) -> None:
        """Start optiSLang and run the project."""

        osl_logger = logging.OslLogger(
            loglevel=self.optislang_log_level,
            log_to_file=True,
            logfile_name=self.optislang_log_file.path,
            log_to_stdout=True,
        )

        osl = Optislang(
            project_path=self.project_file.path,
            loglevel=self.optislang_log_level,
            reset=True,
            shutdown_on_finished=True,
            import_project_properties_file=self.working_properties_file.path,
            additional_args=[f"--write-server-info={self.server_info_file.path}"],
            ini_timeout=300,  # might need to be adjusted
        )

        osl.__logger = osl_logger.add_instance_logger(osl.name, osl, self.optislang_log_level)

        if self.tcp_server_port is None:
            if self.server_info_file.exists():
                with open(self.server_info_file.path, "r") as file:
                    lines = [line.rstrip("\n") for line in file.readlines()]
                for line in lines:
                    if line.startswith("server_port="):
                        self.tcp_server_port = int(line.split("=")[1])
                        break
            else:
                raise Exception("No server info file detected. Unable to retrieve TCP port number.")

        osl.start(wait_for_started=True, wait_for_finished=False)

        while True:
            # Get project status info
            self.project_status_info = osl.get_osl_server().get_full_project_status_info()
            # Read pyoptislang logs
            self.optislang_logs = read_optislang_logs(self.optislang_log_file.path)
            # Get actor status info
            for node_info in self.node_list:
                self.actors_info[node_info["uid"]] = osl.get_osl_server().get_actor_info(node_info["uid"])
                node_hids = _get_actor_hids(osl.get_osl_server().get_actor_states(node_info["uid"]))
                if len(node_hids):
                    self.actors_status_info[node_info["uid"]] = []
                    for hid in node_hids:
                        self.actors_status_info[node_info["uid"]].append(
                            osl.get_osl_server().get_actor_status_info(node_info["uid"], hid)
                        )
            # Get status
            self.optislang_solve_status = osl.project.get_status().lower()
            osl.log.info(f"Analysis status: {self.optislang_solve_status}")
            # Upload fields
            self.transaction.upload(["optislang_solve_status"])
            self.transaction.upload(["project_status_info"])
            self.transaction.upload(["actors_info"])
            self.transaction.upload(["actors_status_info"])
            self.transaction.upload(["optislang_logs"])
            # Check if analysis stopped
            if self.optislang_solve_status in self.tcp_server_stopped_states:
                break
            time.sleep(3)

        osl.dispose()
