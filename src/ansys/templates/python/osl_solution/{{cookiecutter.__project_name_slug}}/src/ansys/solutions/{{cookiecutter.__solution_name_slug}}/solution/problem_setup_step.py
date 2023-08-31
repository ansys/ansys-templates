# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
import os
import platform
import tempfile
import time

from pathlib import Path
from typing import List, Optional

from ansys.optislang.core import Optislang, logging, utils
from ansys.saf.glow.solution import FileReference, FileGroupReference, StepModel, StepSpec, long_running, transaction
from ansys.solutions.optislang.frontend_components.project_properties import ProjectProperties, write_properties_file, apply_placeholders_to_properties_file
from ansys.solutions.products_ecosystem.controller import AnsysProductsEcosystemController

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import get_treeview_items_from_project_tree, read_log_file


class ProblemSetupStep(StepModel):
    """Step model of the problem setup step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    ansys_ecosystem_ready: bool = False
    ui_placeholders: dict = {}
    app_metadata: dict = {}
    analysis_locked: bool = True
    project_locked: bool = False
    selected_actor_from_treeview: Optional[str] = None
    selected_command: Optional[str] = None
    selected_actor_from_command: Optional[str] = None
    commands_locked: bool = False
    auto_update_frequency: float = 2000
    auto_update_activated: bool = True
    actor_uid: Optional[str] = None
    project_command_execution_status: dict = {"alert-message": "", "alert-color": "info"}
    actor_command_execution_status: dict = {"alert-message": "", "alert-color": "info"}
    project_btn_group_options: List = [
                                {"icon": "fas fa-play", "tooltip": "Restart optiSLang project.", "value": "restart", "id": {"type":"action-button", "action":"restart"}},
                                {"icon":"fa fa-hand-paper", "tooltip": "Stop optiSLang project gently.", "value": "stop_gently", "id": {"type":"action-button", "action":"stop_gently"}},
                                {"icon": "fas fa-stop", "tooltip":"Stop optiSLang project.", "value": "stop", "id": {"type": "action-button", "action":"stop"}},
                                {"icon": "fas fa-fast-backward", "tooltip": "Reset optiSLang project.", "value": "reset", "id": {"type":"action-button", "action":"reset"}},
                                {"icon": "fas fa-power-off", "tooltip": "Shutdown optiSLang project.", "value": "shutdown", "id": {"type":"action-button", "action":"shutdown"}},
                            ]
    actor_btn_group_options: List = [
                            {"icon": "fas fa-play", "tooltip": "Restart node.", "value": "restart", "id": {"type":"action-button", "action":"restart"}},
                            {"icon":"fa fa-hand-paper", "tooltip": "Stop node gently.", "value": "stop_gently", "id": {"type":"action-button", "action":"stop_gently"}},
                            {"icon": "fas fa-stop", "tooltip":"Stop node.", "value": "stop", "id": {"type": "action-button", "action":"stop"}},
                            {"icon": "fas fa-fast-backward", "tooltip": "Reset node.", "value": "reset", "id": {"type":"action-button", "action":"reset"}},
                        ]

    # Backend data model
    tcp_server_host: Optional[str] = None
    tcp_server_port: Optional[int] = None
    ansys_ecosystem: dict = {
        "optislang": {
            "authorized_versions": [231, 232],
            "installed_versions": [],
            "compatible_versions": [],
            "selected_version": None,
            "alert_message": "optiSLang install not checked.",
            "alert_color": "warning",
            "alias": "optiSLang",
        }
    }
    project_tree: list = []
    treeview_items: list = [
        {
            "key": "problem_setup_step",
            "text": "Problem Setup",
            "depth": 0,
            "uid": None
        },
    ]
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
    osl_project_states: List = [
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
    osl_actor_states: List = [
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
    optislang_logs: List = []
    optislang_log_level: str = "INFO"
    project_initialized: bool = False
    command_timeout: int = 30

    # File storage ----------------------------------------------------------------------------------------------------

    # Inputs
    project_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.opf")
    properties_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.json")
    metadata_file: FileReference = FileReference("Problem_Setup/metadata.json")
    project_state_file: FileReference = FileReference("Problem_Setup/project_state.json")
    input_files: FileGroupReference = FileGroupReference("Problem_Setup/Input_Files/*.*")
    # If folder doesn't exist, it will be created later
    upload_directory: str = os.path.join(tempfile.gettempdir(), "GLOW")

    # Outputs
    working_properties_file: FileReference = FileReference("Problem_Setup/working_properties_file.json")
    server_info_file: FileReference = FileReference("Problem_Setup/server_info.ini")
    optislang_log_file: FileReference = FileReference("Problem_Setup/pyoptislang.log")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        self=StepSpec(
            upload=[
                "project_file",
                "properties_file",
                "metadata_file",
            ]
        )
    )
    @long_running
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

    @transaction(
        self=StepSpec(
            download=["properties_file"],
            upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"]
        )
    )
    @long_running
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

        # Collect optiSLang installations
        self.ansys_ecosystem["optislang"]["installed_versions"] = list(dict(utils.find_all_osl_exec()).keys())
        self.ansys_ecosystem["optislang"]["compatible_versions"] = [
            product_version
            for product_version in self.ansys_ecosystem["optislang"]["installed_versions"]
            if product_version in self.ansys_ecosystem["optislang"]["authorized_versions"]
        ]

        # Collect additonnal Ansys products installations
        controller = AnsysProductsEcosystemController()
        for product_name in self.ansys_ecosystem.keys():
            if product_name != "optislang":
                self.ansys_ecosystem[product_name]["installed_versions"] = controller.get_installed_versions(
                    product_name, output_format="long"
                )
                self.ansys_ecosystem[product_name]["compatible_versions"] = [
                    product_version
                    for product_version in self.ansys_ecosystem[product_name]["installed_versions"]
                    if product_version in self.ansys_ecosystem[product_name]["authorized_versions"]
                ]

        # Check ecosystem
        for product_name in self.ansys_ecosystem.keys():
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
                    ] += f" {authorized_version}"
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
                    alert_message += f" {compatible_version}"
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
    @long_running
    def get_app_metadata(self) -> None:
        """Read OWA metadata file."""

        with open(self.metadata_file.path) as f:
            self.app_metadata = json.load(f)

    @transaction(
        self=StepSpec(
            download=[
                "input_files",
                "optislang_log_level",
                "project_file",
                "working_properties_file",
            ],
            upload=[
                "tcp_server_host",
                "tcp_server_port",
                "project_tree",
                "treeview_items",
                "actors_info",
                "actors_status_info",
                "optislang_logs",
                "optislang_log_file",
                "project_state",
                "project_status_info",
                "results_files",
                "server_info_file",
            ],
        )
    )
    @long_running
    def start(self) -> None:
        """Start optiSLang and run the project."""

        # Start optiSLang instance
        osl = Optislang(
            project_path=self.project_file.path,
            loglevel=self.optislang_log_level,
            reset=True,
            shutdown_on_finished=False,
            import_project_properties_file=self.working_properties_file.path,
            additional_args=[f"--write-server-info={self.server_info_file.path}"],
            ini_timeout=300,  # might need to be adjusted depending on the hardware
        )

        # Configure logging
        osl_logger = logging.OslLogger(
            loglevel=self.optislang_log_level,
            log_to_file=True,
            logfile_name=self.optislang_log_file.path,
            log_to_stdout=True,
        )
        osl.__logger = osl_logger.add_instance_logger(osl.name, osl, self.optislang_log_level)

        # Get server host
        self.tcp_server_host = osl.get_osl_server().get_host()
        self.transaction.upload(["tcp_server_host"])

        # Get server port
        server_info = osl.get_osl_server().get_server_info()
        self.tcp_server_port = server_info["server"]["server_port"]
        self.transaction.upload(["tcp_server_port"])

        # Get project tree
        self.project_tree = osl.project._get_project_tree()
        self.transaction.upload(["project_tree"])

        # Update treeview items
        self.treeview_items = get_treeview_items_from_project_tree(self.project_tree)
        self.transaction.upload(["treeview_items"])

        # Start optiSLang project
        osl.start(wait_for_started=True, wait_for_finished=False)

        # Monitor project state and upload results
        while True:
            # Get project state
            self.project_state = osl.project.get_status()
            osl.log.info(f"Analysis status: {self.project_state}")
            # Get project status info
            self.project_status_info = osl.get_osl_server().get_full_project_status_info()
            # Read pyoptislang logs
            self.optislang_logs = read_log_file(self.optislang_log_file.path)
            # Get actor status info
            for node_info in self.project_tree:
                if node_info["uid"] == osl.project.root_system.uid:
                    node = osl.project.root_system
                else:
                    node = osl.project.root_system.find_node_by_uid(node_info["uid"], search_depth=-1)
                self.actors_info[node.uid] = osl.get_osl_server().get_actor_info(node.uid)
                if node.get_states_ids():
                    self.actors_status_info[node.uid] = []
                    for hid in node.get_states_ids():
                        self.actors_status_info[node.uid].append(
                            osl.get_osl_server().get_actor_status_info(node.uid, hid)
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

        # Close connection with optiSLang server
        osl.dispose()

    @transaction(
        self=StepSpec(
            download=[
                "tcp_server_host",
                "tcp_server_port",
                "command_timeout",
                "selected_actor_from_command",
                "project_tree",
                "selected_command"
            ],
            upload=["actor_uid"],
        )
    )
    def run_selected_project_command(self) -> None:
        """Run the selected project command."""
        osl = Optislang(
                host=self.tcp_server_host,
                port=self.tcp_server_port,
                shutdown_on_finished=False
            )
        if not self.selected_actor_from_command == "shutdown":
            if self.selected_actor_from_command == osl.project.root_system.uid:
                node = osl.project.root_system
                self.actor_uid = None
            else:
                node = osl.project.root_system.find_node_by_uid(self.selected_actor_from_command, search_depth=-1)
                self.actor_uid = node
        else:
            node = osl.project.root_system

        status = node.control(self.selected_command, wait_for_completion=True, timeout=self.command_timeout)

        if not status:
            raise Exception(f"{problem_setup_step.selected_command.replace('_', ' ').title()} command against node {node.get_name()} failed.")

        osl.dispose()