# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import os
import json
from pathlib import Path
import platform
import time
from typing import List
import tempfile


from ansys.optislang.core import Optislang, logging
from ansys.saf.glow.solution import FileReference, FileGroupReference, StepModel, StepSpec, long_running, transaction
from ansys.solutions.optislang.frontend_components.project_properties import ProjectProperties, write_properties_file, apply_placeholders_to_properties_file
from ansys.solutions.products_ecosystem.controller import AnsysProductsEcosystemController
from ansys.solutions.products_ecosystem.utils import convert_to_long_version

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.model.optislang.project_tree import dump_project_state, get_project_tree, get_node_list, get_step_list, get_node_hids
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.model.optislang.server_commands import run_osl_server_command
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.monitoring import read_log_file


class ProblemSetupStep(StepModel):
    """Step model of the problem setup step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    ansys_ecosystem_ready: bool = False
    ui_placeholders: dict = {}
    app_metadata: dict = {}
    analysis_running: bool = False
    analysis_locked: bool = True
    project_locked: bool = False
    selected_actor_info: dict = {}
    selected_actor_index: int = None
    selected_actor_command: str = None # expect a string with format <actor-uid>-<actor-command>
    lock_commands: bool = False
    project_initialized: bool = False
    project_started: bool = False

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
    project_state: str = "NOT STARTED"
    osl_project_states: list = [
        "IDLE",
        "PROCESSING",
        "PAUSED",
        "PAUSE_REQUESTED",
        "STOPPED",
        "STOP_REQUESTED",
        "GENTLY_STOPPED",
        "GENTLE_STOP_REQUESTED",
        "FINISHED"
    ]
    osl_actor_states: list = [
        "Idle",
        "Succeeded",
        "Failed",
        "Running",
        "Aborted",
        "Predecessor failed",
        "Skipped",
        "Incomplete",
        "Processing done",
        "Stopped",
        "Gently stopped"
    ]
    optislang_logs: list = []
    optislang_log_level: str = "INFO"
    has_project_state: bool = False
    command_timeout: int = 100
    command_retries: int = 0
    auto_update_frequency: float = 4

    # File storage ----------------------------------------------------------------------------------------------------

    # Inputs
    project_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.opf")
    properties_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.json")
    metadata_file: FileReference = FileReference("Problem_Setup/metadata.json")
    project_state_file: FileReference = FileReference("Problem_Setup/project_state.json")
    input_files: FileGroupReference = FileGroupReference("Problem_Setup/Input_Files/*.*")
    # If folder doesn't exist, it will be created later
    upload_directory = os.path.join(tempfile.gettempdir(), "GLOW")

    # Outputs
    working_properties_file: FileReference = FileReference("Problem_Setup/working_properties_file.json")
    server_info_file: FileReference = FileReference("Problem_Setup/server_info.ini")
    optislang_log_file: FileReference = FileReference("Problem_Setup/pyoptislang.log")
    server_command_log_file: FileReference = FileReference("server_commands.log")

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

    @transaction(
        self=StepSpec(
            download=["properties_file", "ui_placeholders"],
            upload=[
                "working_properties_file",
                "placeholders",
                "registered_files",
                "settings",
                "parameter_manager",
                "criteria",
            ],
        )
    )
    def write_updated_properties_file(self) -> None:
        properties = apply_placeholders_to_properties_file(self.ui_placeholders, self.properties_file.path)
        self.placeholders = properties["placeholders"]
        self.registered_files = properties["registered_files"]
        self.settings = properties["settings"]
        self.parameter_manager = properties["parameter_manager"]
        self.criteria = properties["criteria"]
        write_properties_file(properties, Path(self.working_properties_file.path))

    @transaction(
        self=StepSpec(
            download=["properties_file", "ui_placeholders"],
            upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"],
        )
    )
    def update_osl_placeholders_with_ui_values(self) -> None:
        properties = apply_placeholders_to_properties_file(self.ui_placeholders, self.properties_file.path)
        self.placeholders = properties["placeholders"]
        self.registered_files = properties["registered_files"]
        self.settings = properties["settings"]
        self.parameter_manager = properties["parameter_manager"]
        self.criteria = properties["criteria"]

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
                "optislang_log_level",
                "node_list",
                "input_files",
            ],
            upload=[
                "project_state",
                "server_info_file",
                "actors_info",
                "actors_status_info",
                "project_status_info",
                "results_files",
                "optislang_log_file",
                "optislang_logs",
                "project_started",
                "tcp_server_port",
            ],
        )
    )
    @long_running
    def start(self) -> None:
        """Start optiSLang and run the project."""

        self.project_started = True
        self.transaction.upload(["project_started"])

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
            self.transaction.upload(["tcp_server_port"])

        osl.start(wait_for_started=True, wait_for_finished=False)

        while True:
            # Get project state
            self.project_state = osl.project.get_status()
            osl.log.info(f"Analysis status: {self.project_state}")
            # Get project status info
            self.project_status_info = osl.get_osl_server().get_full_project_status_info()
            # Read pyoptislang logs
            self.optislang_logs = read_log_file(self.optislang_log_file.path)
            # Get actor status info
            for node_info in self.node_list:
                self.actors_info[node_info["uid"]] = osl.get_osl_server().get_actor_info(node_info["uid"])
                node_hids = get_node_hids(osl, node_info["uid"])
                if len(node_hids):
                    self.actors_status_info[node_info["uid"]] = []
                    for hid in node_hids:
                        self.actors_status_info[node_info["uid"]].append(
                            osl.get_osl_server().get_actor_status_info(node_info["uid"], hid)
                        )
             # Upload fields
            self.transaction.upload(["project_state"])
            self.transaction.upload(["project_status_info"])
            self.transaction.upload(["actors_info"])
            self.transaction.upload(["actors_status_info"])
            self.transaction.upload(["optislang_logs"])
            if self.project_state == "FINISHED":
                break
            time.sleep(3)

        osl.dispose()

    @transaction(
        self=StepSpec(
            download=["tcp_server_host", "tcp_server_port", "command_timeout", "command_retries", "selected_actor_command", "selected_actor_info"],
            upload=["server_command_log_file"],
        )
    )
    @long_running
    def restart(self) -> None:
        """Restart project/actor."""

        if self.selected_actor_info["is_root"]:
            actor_uid = None
        else:
            actor_uid = self.selected_actor_info["uid"]

        run_osl_server_command(
            self.tcp_server_host,
            self.tcp_server_port,
            "restart",
            actor_uid=actor_uid,
            wait_for_completion=True,
            retries=self.command_retries,
            timeout=self.command_timeout,
            working_directory=self.server_command_log_file.project_path,
        )

    @transaction(
        self=StepSpec(
            download=["tcp_server_host", "tcp_server_port", "command_timeout", "command_retries", "selected_actor_command", "selected_actor_info"],
            upload=["server_command_log_file"],
        )
    )
    @long_running
    def stop_gently(self) -> None:
        """Stop project/actor gently."""

        if self.selected_actor_info["is_root"]:
            actor_uid = None
        else:
            actor_uid = self.selected_actor_info["uid"]

        run_osl_server_command(
            self.tcp_server_host,
            self.tcp_server_port,
            "stop_gently",
            actor_uid=actor_uid,
            wait_for_completion=True,
            retries=self.command_retries,
            timeout=self.command_timeout,
            working_directory=self.server_command_log_file.project_path,
        )

    @transaction(
        self=StepSpec(
            download=["tcp_server_host", "tcp_server_port", "command_timeout", "command_retries", "selected_actor_command", "selected_actor_info"],
            upload=["server_command_log_file"],
        )
    )
    @long_running
    def stop(self) -> None:
        """Stop project/actor."""

        if self.selected_actor_info["is_root"]:
            actor_uid = None
        else:
            actor_uid = self.selected_actor_info["uid"]

        run_osl_server_command(
            self.tcp_server_host,
            self.tcp_server_port,
            "stop",
            actor_uid=actor_uid,
            wait_for_completion=True,
            retries=self.command_retries,
            timeout=self.command_timeout,
            working_directory=self.server_command_log_file.project_path,
        )

    @transaction(
        self=StepSpec(
            download=["tcp_server_host", "tcp_server_port", "command_timeout", "command_retries", "selected_actor_command", "selected_actor_info"],
            upload=["server_command_log_file"],
        )
    )
    @long_running
    def reset(self) -> None:
        """Reset project/actor."""

        if self.selected_actor_info["is_root"]:
            actor_uid = None
        else:
            actor_uid = self.selected_actor_info["uid"]

        run_osl_server_command(
            self.tcp_server_host,
            self.tcp_server_port,
            "reset",
            actor_uid=actor_uid,
            wait_for_completion=True,
            retries=self.command_retries,
            timeout=self.command_timeout,
            working_directory=self.server_command_log_file.project_path,
        )

    @transaction(
        self=StepSpec(
            download=["tcp_server_host", "tcp_server_port", "command_timeout", "command_retries"],
            upload=["server_command_log_file"],
        )
    )
    @long_running
    def shutdown(self) -> None:
        """Shutdown project."""

        run_osl_server_command(
            self.tcp_server_host,
            self.tcp_server_port,
            "shutdown",
            wait_for_completion=True,
            retries=self.command_retries,
            timeout=self.command_timeout,
            working_directory=self.server_command_log_file.project_path,
        )
