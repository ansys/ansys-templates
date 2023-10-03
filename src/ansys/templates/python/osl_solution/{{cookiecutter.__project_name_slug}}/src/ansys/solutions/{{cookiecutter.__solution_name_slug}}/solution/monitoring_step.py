# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
from pathlib import Path
import time
from typing import List, Union, Optional

from ansys.optislang.core import logging
from ansys.optislang.core.errors import OslCommunicationError
from ansys.optislang.core.osl_server import OslServer
from ansys.saf.glow.solution import FileReference, StepModel, StepSpec, instance, long_running, transaction

from ansys.solutions.{{cookiecutter.__solution_name_slug}}.datamodel import datamodel
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.optislang_manager import OptislangManager
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.utilities.common_functions import read_log_file, check_optislang_server, get_states_ids_from_states


class MonitoringStep(StepModel):
    """Step model of the monitoring step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    selected_actor_from_treeview: Optional[str] = None # uid of the actor selected from the treeview.
    selected_command: Optional[str] = None
    selected_actor_from_command: Optional[str] = None # uid of the actor from which a control command has been requested.
    selected_state_id: Optional[str] = None
    commands_locked: bool = False

    auto_update_activated: bool = True
    actor_uid: Optional[str] = None
    project_command_execution_status: dict = {"alert-message": "", "alert-color": "info"}
    actor_command_execution_status: dict = {"alert-message": "", "alert-color": "info"}
    project_btn_group_options: List = [
                                {
                                    "icon": "fas fa-play",
                                    "tooltip": "Restart optiSLang project.",
                                    "value": "restart",
                                    "id": {
                                        "type":"action-button",
                                        "action":"restart"
                                    }
                                },
                                {
                                    "icon":"fa fa-hand-paper",
                                    "tooltip": "Stop optiSLang project gently.",
                                    "value": "stop_gently",
                                    "id": {
                                        "type":"action-button",
                                        "action":"stop_gently"
                                    }
                                },
                                {
                                    "icon": "fas fa-stop",
                                    "tooltip":"Stop optiSLang project.",
                                    "value": "stop",
                                    "id": {
                                        "type": "action-button",
                                        "action":"stop"
                                        }
                                    },
                                {
                                    "icon": "fas fa-fast-backward",
                                    "tooltip": "Reset optiSLang project.",
                                    "value": "reset",
                                    "id": {
                                        "type":"action-button",
                                        "action":"reset"
                                        }
                                    },
                                {
                                    "icon": "fas fa-power-off",
                                    "tooltip": "Shutdown optiSLang project.",
                                    "value": "shutdown",
                                    "id": {
                                        "type":"action-button",
                                        "action":"shutdown"
                                    }
                                },
                            ]
    actor_btn_group_options: List = [
                            {
                                "icon": "fas fa-play",
                                "tooltip": "Restart node.",
                                "value": "restart",
                                "id": {
                                    "type":"action-button",
                                    "action":"restart"
                                }
                            },

                            {
                                "icon":"fa fa-hand-paper",
                                "tooltip": "Stop node gently.",
                                "value": "stop_gently",
                                "id": {
                                    "type":"action-button",
                                    "action":"stop_gently"
                                }
                            },

                            {
                                "icon": "fas fa-stop",
                                "tooltip":"Stop node.",
                                "value": "stop",
                                "id": {
                                    "type": "action-button",
                                    "action":"stop"
                                }
                            },

                            {
                                "icon": "fas fa-fast-backward",
                                "tooltip": "Reset node.",
                                "value": "reset",
                                "id": {
                                    "type":"action-button",
                                    "action":"reset"
                                }
                            },
                        ]

    # Backend data model
    osl_server_healthy: Optional[bool] = None
    osl_max_server_request_attempts: int = 3
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
    osl_project_state: str = "NOT STARTED"
    osl_start_timeout: int = 100
    auto_update_frequency: float = 2000 # ms
    command_timeout: int = 30

    # File storage ----------------------------------------------------------------------------------------------------

    # Output
    full_project_status_info_file: FileReference = FileReference("Monitoring/full_project_status_info.json")
    project_data_file: FileReference = FileReference("Monitoring/project_data.json")
    osl_log_file: FileReference = FileReference("Monitoring/optiSLang.log")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        self=StepSpec(
            upload=["osl_server_healthy"],
        )
    )
    @instance("problem_setup_step.osl_manager", identifier="osl_manager")
    def check_optislang_server(self, osl_manager: OptislangManager) -> None:
        """optiSLang server health check."""
        osl = osl_manager.instance
        self.osl_server_healthy = check_optislang_server(osl.get_osl_server())

    @transaction(
        problem_setup_step=StepSpec(
            download=[
                "osl_server_host",
                "osl_server_port",
                "osl_project_tree",
                "osl_loglevel",
            ]
        ),
        self=StepSpec(
            download=[
                "osl_max_server_request_attempts"
            ],
            upload=[
                "osl_server_healthy",
                "osl_project_state",
                "full_project_status_info_file",
                "project_data_file",
                "osl_log_file"
            ],
        )
    )
    @instance("problem_setup_step.osl_manager", identifier="osl_manager")
    @long_running
    def upload_project_data(self, problem_setup_step: ProblemSetupStep, osl_manager: OptislangManager) -> None:
        """Monitor the progress of the optiSLang project and continuously upload project data."""
        # Creat monitoring directory
        Path(self.osl_log_file.path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize new instance
        osl = osl_manager.instance

        # Set timeout
        osl.set_timeout(25)

        # Get optiSLang server
        osl_server = osl.get_osl_server()

        # Create log file
        osl_logs = open(self.osl_log_file.path, 'w')
        osl_logs.write("Start monitoring.\n\n")

        # Initialize project data structure
        project_data = {"project": {"information": {}}, "actors": {}}
        for node_props in problem_setup_step.osl_project_tree:
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
            self.osl_server_healthy = check_optislang_server(osl_server)
            osl_logs.write(f"Server health check: {self.osl_server_healthy}\n")

            # Get project state
            self.osl_project_state = osl.project.get_status()
            osl_logs.write(f"Project state: {self.osl_project_state}\n")

            # Get full project status info
            full_project_status_info = osl_server.get_full_project_status_info()
            with open(self.full_project_status_info_file.path, "w") as json_file: json.dump(full_project_status_info, json_file)
            osl_logs.write("Get full project status info\n")

            # Collect project information
            project_data["project"]["information"] = datamodel.extract_project_status_info(full_project_status_info)

            # Walk through project tree
            osl_logs.write("Walk through project tree\n")
            for node_props in problem_setup_step.osl_project_tree:

                # Get node
                if node_props["uid"] == osl.project.root_system.uid:
                    node = osl.project.root_system
                else:
                    node = osl.project.root_system.find_node_by_uid(node_props["uid"], search_depth=-1)
                osl_logs.write(f"   Current node: {node.uid}\n")

                # Get actor info (TCP REQUEST)
                osl_logs.write(f"       Get actor info\n")
                actor_info = self._make_osl_server_request(osl_server, "get_actor_info", node.uid)

                # Collect actor log data
                project_data["actors"][node.uid]["log"] = datamodel.extract_actor_log_data(actor_info)

                # Collect actor statistics data
                project_data["actors"][node.uid]["statistics"] = datamodel.extract_actor_statistics_data(actor_info)

                # Get states ids (TCP REQUEST)
                osl_logs.write(f"       Get states ids\n")
                actor_states = self._make_osl_server_request(osl_server, "get_actor_states", node.uid)
                actor_states_ids = get_states_ids_from_states(actor_states)
                project_data["actors"][node.uid]["states_ids"] = actor_states_ids

                # Walk through states ids
                if len(actor_states_ids):
                    osl_logs.write("       Walk through states ids\n")
                    for hid in actor_states_ids:
                        osl_logs.write(f"        Current hid: {hid}\n")

                        # Get actor status info (TCP REQUEST)
                        osl_logs.write(f"        Get actor status info\n")
                        actor_status_info = self._make_osl_server_request(osl_server, "get_actor_status_info", node.uid, hid)

                        # Collect actor information data
                        project_data["actors"][node.uid]["information"][hid] = datamodel.extract_actor_information_data(actor_status_info, node_props["kind"])

                        # Collect design table data
                        if node_props["kind"] == "system":
                            project_data["actors"][node.uid]["design_table"][hid] = datamodel.extract_design_table_data(actor_status_info)

            # Dump project data
            osl_logs.write(f"Dump project data\n")
            with open(self.project_data_file.path, "w") as json_file: json.dump(project_data, json_file, allow_nan=True)

            # Upload fields
            osl_logs.write(f"Upload fields\n")
            self.transaction.upload(["osl_server_healthy"])
            self.transaction.upload(["osl_project_state"])
            self.transaction.upload(["full_project_status_info_file"])
            self.transaction.upload(["project_data_file"])
            self.transaction.upload(["osl_log_file"])

            osl_logs.write(f"--------------------------------------------------\n")

            # Wait
            time.sleep(5)

        osl_logs.close()

    @transaction(
        problem_setup_step=StepSpec(
            download=[
                "osl_server_host",
                "osl_server_port",
                "osl_project_tree",
            ]
        ),
        self=StepSpec(
            download=[
                "command_timeout",
                "selected_actor_from_command",
                "selected_command",
            ],
            upload=["actor_uid"],
        )
    )
    @instance("problem_setup_step.osl_manager", identifier="osl_manager")
    def control_node_state(self, problem_setup_step: ProblemSetupStep, osl_manager: OptislangManager) -> None:
        """Update the state of root or actor node based on the selected command in the UI."""
        osl = osl_manager.instance
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
            raise Exception(f"{self.selected_command.replace('_', ' ').title()} command against node {node.get_name()} failed.")

    def _make_osl_server_request(self, osl_server: OslServer, request_name: str, actor_uid: str, hid: str = None) -> Union[list, dict]:
        """Make a server request and try multiple times if a communication error is raised."""
        # Check inputs
        if request_name not in ["get_actor_info", "get_actor_states", "get_actor_status_info"]:
            raise ValueError(f"Unknown request {request_name}.")
        if request_name == "get_actor_status_info" and not hid:
            raise Exception("A state id is needed to run the get_actor_status_info request.")
        # Get method from optiSLanf server
        request = getattr(osl_server, request_name)
        # Make request
        attempts = 0
        success = False
        while attempts <= self.osl_max_server_request_attempts:
            attempts += 1
            try:
                if request_name == "get_actor_info":
                    response = request(actor_uid)
                elif request_name == "get_actor_states":
                    response = request(actor_uid)
                elif request_name == "get_actor_status_info":
                    response = request(actor_uid, hid)
                success = True
            except OslCommunicationError:
                pass
            if success:
                break
        if not success:
            request_name_splitted = request_name.replace("_", " ").capitalize()
            raise Exception(f"{request_name_splitted} method failed after {attempts} attempts.")

        return response
