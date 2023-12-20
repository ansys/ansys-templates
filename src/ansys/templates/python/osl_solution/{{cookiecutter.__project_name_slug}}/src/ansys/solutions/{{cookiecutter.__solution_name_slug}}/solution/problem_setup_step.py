# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
import os
import platform
import tempfile
import time

from pathlib import Path
from typing import List, Optional, Union

from ansys.optislang.core import Optislang, utils, logging
from ansys.saf.glow.solution import (
    FileGroupReference,
    FileReference,
    AssetFileReference,
    StepModel,
    StepSpec,
    create_instance,
    instance,
    long_running,
    transaction,
)
from ansys.solutions.optislang.frontend_components.project_properties import (
    ProjectProperties,
    apply_placeholders_to_properties_file,
    write_properties_file,
)
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.datamodel import datamodel
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.optislang_manager import OptislangManager
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.utilities.common_functions import (
    get_treeview_items_from_project_tree, check_optislang_server, get_states_ids_from_states
)


class ProblemSetupStep(StepModel):
    """Step model of the problem setup step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    ansys_ecosystem_ready: bool = False
    project_initialized: bool = False
    analysis_locked: bool = False
    project_locked: bool = False
    analysis_started: bool = False
    alerts: dict = {}

    # Backend data model
    ansys_ecosystem: dict = {
        "optislang": {
            "authorized_versions": [],
            "installed_versions": [],
            "compatible_versions": [],
            "selected_version": None,
            "alias": "optiSLang",
        }
    }
    osl_server_host: Optional[str] = None
    osl_server_port: Optional[int] = None
    osl_loglevel: str = "INFO"
    osl_project_tree: list = []
    osl_start_timeout: int = 100 # second
    osl_instance_started: bool = False
    osl_server_healthy: Optional[bool] = None
    osl_project_state: str = "NOT STARTED"
    osl_max_server_request_attempts: int = 10
    placeholders: dict = {}
    registered_files: List = []
    settings: dict = {}
    parameter_manager: dict = {}
    criteria: dict = {}
    ui_placeholders: dict = {}
    app_metadata: dict = {}
    treeview_items: list = [
        {
            "id": "problem_setup_step",
            "text": "Problem Setup",
            "expanded": True,
            "prefixIcon": {
                "src": "https://s2.svgbox.net/hero-solid.svg?ic=adjustments"
            },
            "level": 0
        },
    ]

    # File storage ----------------------------------------------------------------------------------------------------

    # Inputs
    project_file: FileReference = FileReference("Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.opf")
    properties_file: AssetFileReference = AssetFileReference(relative_path="Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.json", encrypted=False)
    metadata_file: AssetFileReference = AssetFileReference(relative_path="Problem_Setup/metadata.json", encrypted=False)
    input_files: FileGroupReference = FileGroupReference("Problem_Setup/Input_Files/*.*")
    # If folder doesn't exist, it will be created later
    upload_directory: str = os.path.join(tempfile.gettempdir(), "GLOW")

    # Outputs
    working_properties_file: FileReference = FileReference("Problem_Setup/working_properties_file.json")
    osl_log_file: FileReference = FileReference("Problem_Setup/optiSLang.log")
    full_project_status_info_file: FileReference = FileReference("Monitoring/full_project_status_info.json")
    project_data_file: FileReference = FileReference("Monitoring/project_data.json")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        self=StepSpec(
            upload=[
                "project_file",
            ]
        )
    )
    def upload_bulk_files_to_project_directory(self) -> None:
        """Upload bulk files to project directory."""

        original_project_file = Path(__file__).absolute().parent.parent / "logic" / "assets" / "{{ cookiecutter.__optiSLang_application_archive_stem }}.opf"
        self.project_file.write_bytes(original_project_file.read_bytes())

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
            download=["properties_file"],
            upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"]
        )
    )
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
        """Write updated optiSLang project properties file."""
        Path(self.working_properties_file.path).parent.mkdir(parents=True, exist_ok=True)
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
    @long_running
    def update_osl_placeholders_with_ui_values(self) -> None:
        """Update placeholders with values selected by the user in the UI."""
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
        self.ansys_ecosystem["optislang"]["installed_versions"] = sorted(list(dict(utils.find_all_osl_exec()).keys()))
        if len(self.ansys_ecosystem["optislang"]["authorized_versions"]) > 0:
            self.ansys_ecosystem["optislang"]["compatible_versions"] = [
                product_version
                for product_version in self.ansys_ecosystem["optislang"]["installed_versions"]
                if product_version in self.ansys_ecosystem["optislang"]["authorized_versions"]
            ]
        else:
            self.ansys_ecosystem["optislang"]["compatible_versions"] = self.ansys_ecosystem["optislang"]["installed_versions"]

        # Check ecosystem
        for product_name in self.ansys_ecosystem.keys():
            if len(self.ansys_ecosystem[product_name]["installed_versions"]) == 0:
                message = f"No installation of {product_name.title()} found in the machine {platform.node()}."
                raise Exception(message)
            elif len(self.ansys_ecosystem[product_name]["compatible_versions"]) == 0:
                message = (
                    f"None of the authorized versions of {product_name.title()} "
                    f"is installed in the machine {platform.node()}.\n"
                )
                message += "At least one of these versions is required:"
                for authorized_version in self.ansys_ecosystem[product_name]["authorized_versions"]:
                    self.ansys_ecosystem[product_name][
                        "alert_message"
                    ] += f" {authorized_version}"
                message += "."
                raise Exception(message)
            else:
                self.ansys_ecosystem[product_name]["selected_version"] = self.ansys_ecosystem[product_name][
                    "compatible_versions"
                ][
                    -1
                ]  # Latest

    @transaction(
        self=StepSpec(
            download=[
                "input_files",
                "project_file",
                "working_properties_file",
                "osl_loglevel",
                "ansys_ecosystem",
                "osl_max_server_request_attempts"
            ],
            upload=[
                "osl_server_host",
                "osl_server_port",
                "osl_project_tree",
                "treeview_items",
                "osl_project_state",
                "osl_log_file",
                "full_project_status_info_file",
                "project_data_file",
                "alerts"
            ],
        )
    )
    @long_running
    @create_instance("osl_manager", OptislangManager)
    def start_and_monitor_osl_project(self, osl_manager: OptislangManager) -> None:
        """Start optiSLang and run the project."""
        # Create monitoring directory
        Path(self.project_data_file.path).parent.mkdir(parents=True, exist_ok=True)
        # Start optiSLang instance using instance manager.
        try:
            osl_manager.initialize(
                project_path=self.project_file.path,
                project_properties_file=self.working_properties_file.path,
                osl_version=self.ansys_ecosystem["optislang"]["selected_version"],
                loglevel=self.osl_loglevel
            )
        except ConnectionRefusedError:
            raise Exception(str(e))
        # Get optiSLang instance
        osl = osl_manager.instance
        # Set timeout
        osl.set_timeout(300)
        # Get optiSLang server
        osl_server =  osl.get_osl_server()
        # Get server host
        self.osl_server_host = osl_server.get_host()
        # Get server port
        server_info = osl_server.get_server_info()
        self.osl_server_port = server_info["server"]["server_port"]
        # Configure logging.
        osl_logger = logging.OslLogger(
            loglevel=self.osl_loglevel,
            log_to_file=True,
            logfile_name=self.osl_log_file.path,
            log_to_stdout=True,
        )
        osl.__logger = osl_logger.add_instance_logger(osl.name, osl, self.osl_loglevel)
         # Get project tree
        self.osl_project_tree = osl.project._get_project_tree()
        self.transaction.upload(["osl_project_tree"])
        # Update treeview items
        self.treeview_items = get_treeview_items_from_project_tree(self.osl_project_tree)
        self.transaction.upload(["treeview_items"])
        # Start optiSLang project
        osl.log.info("Start analysis")
        osl.start(wait_for_started=True, wait_for_finished=False)
        # Initialize project data structure
        project_data = {"project": {"information": {}}, "actors": {}}
        for node_props in self.osl_project_tree:
            # Get node
            if node_props["uid"] == osl.project.root_system.uid:
                node = osl.project.root_system
            else:
                node = osl.project.root_system.find_node_by_uid(node_props["uid"], search_depth=-1)
            # Initialize dictionary
            project_data["actors"][node.uid] = {"states_ids": {}, "information": {}, "log": {}, "statistics": {}, "design_table": {}}
        # Monitor project state and upload data.
        while self.osl_project_state not in ["FINISHED", "ABORTED"]:
            # Check optiSLang server health
            osl.log.info(f"optiSLang server health check: {check_optislang_server(osl)}")
            # Get project state
            self.osl_project_state = osl.project.get_status()
            osl.log.info(f"Project state: {self.osl_project_state}")
            # Get full project status info (TCP REQUEST)
            full_project_status_info = self._make_osl_server_request(osl, "get_full_project_status_info")
            with open(self.full_project_status_info_file.path, "w") as json_file: json.dump(full_project_status_info, json_file)
            # Collect project information
            project_data["project"]["information"] = datamodel.extract_project_status_info(full_project_status_info)
            # Walk through project tree
            for node_props in self.osl_project_tree:
                # Get actor info (TCP REQUEST)
                actor_info = self._make_osl_server_request(osl, "get_actor_info", actor_uid=node_props["uid"])
                # Collect actor log data
                project_data["actors"][node_props["uid"]]["log"] = datamodel.extract_actor_log_data(actor_info)
                # Collect actor statistics data
                project_data["actors"][node_props["uid"]]["statistics"] = datamodel.extract_actor_statistics_data(actor_info)
                # Get states ids (TCP REQUEST)
                actor_states = self._make_osl_server_request(osl, "get_actor_states", actor_uid=node_props["uid"])
                actor_states_ids = get_states_ids_from_states(actor_states)
                project_data["actors"][node_props["uid"]]["states_ids"] = actor_states_ids
                # Walk through states ids
                if len(actor_states_ids):
                    for hid in actor_states_ids:
                        # Get actor status info (TCP REQUEST)
                        actor_status_info = self._make_osl_server_request(osl, "get_actor_status_info", actor_uid=node_props["uid"], hid=hid)
                        # Collect actor information data
                        project_data["actors"][node_props["uid"]]["information"][hid] = datamodel.extract_actor_information_data(actor_status_info, actor_info, node_props["kind"])
                        # Collect design table data
                        if node_props["kind"] == "system":
                            project_data["actors"][node_props["uid"]]["design_table"][hid] = datamodel.extract_design_table_data(actor_status_info)
            # Dump project data
            with open(self.project_data_file.path, "w") as json_file: json.dump(project_data, json_file, allow_nan=True)
            # Upload fields
            self.transaction.upload(["osl_project_state"])
            self.transaction.upload(["full_project_status_info_file"])
            self.transaction.upload(["project_data_file"])
            self.transaction.upload(["osl_log_file"])
            # Wait
            time.sleep(5)

        # Reset alerts
        self.alerts = {}

    @transaction(
        self=StepSpec(
            upload=["osl_server_healthy"],
        )
    )
    @instance("osl_manager", identifier="osl_manager")
    def check_optislang_server(self, osl_manager: OptislangManager) -> None:
        """optiSLang server health check."""
        osl = osl_manager.instance
        self.osl_server_healthy = check_optislang_server(osl.get_osl_server())

    def _make_osl_server_request(self, osl: Optislang, request_name: str, actor_uid: str = None, hid: str = None) -> Union[list, dict]:
        """Make a server request and try multiple times if a communication error is raised."""
        # Check inputs
        if request_name not in ["get_actor_info", "get_actor_states", "get_actor_status_info", "get_full_project_status_info"]:
            raise ValueError(f"Unknown request {request_name}.")
        if request_name in ["get_actor_info", "get_actor_states"] and not actor_uid:
            raise Exception(f"An actor uid is needed to run the {request_name} request.")
        if request_name == "get_actor_status_info" and not hid:
            raise Exception("A state id is needed to run the get_actor_status_info request.")
        # Get optiSLang server
        osl_server =  osl.get_osl_server()
        # Get method from optiSLanf server
        request = getattr(osl_server, request_name)
        request_name_splitted = request_name.replace("_", " ").capitalize()
        # Make request
        attempts = 0
        success = False
        while attempts <= self.osl_max_server_request_attempts:
            attempts += 1
            try:
                if request_name == "get_full_project_status_info":
                    response = request()
                elif request_name == "get_actor_info":
                    response = request(actor_uid)
                elif request_name == "get_actor_states":
                    response = request(actor_uid)
                elif request_name == "get_actor_status_info":
                    response = request(actor_uid, hid)
                success = True
            except Exception as e:
                message = f"{request_name_splitted} OSL server request failed with the following exception: {str(e)}.\nAttempt: {attempts}/{self.osl_max_server_request_attempts}"
                osl.log.warning(message)
                self.alerts = {
                    "level": "warning",
                    "message": message
                }
                self.transaction.upload(["alerts"])
            if success:
                break
        if not success:
            message = f"{request_name_splitted} OSL server request failed {self.osl_max_server_request_attempts} times."
            osl.log.error(message)
            raise Exception(message)

        return response
