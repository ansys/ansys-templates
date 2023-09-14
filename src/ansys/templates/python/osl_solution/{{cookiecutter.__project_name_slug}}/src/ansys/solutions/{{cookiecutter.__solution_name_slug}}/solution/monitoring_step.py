# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
from pathlib import Path
import time
from typing import List, Optional

from ansys.optislang.core import Optislang, logging
from ansys.saf.glow.solution import FileReference, StepModel, StepSpec, instance, long_running, transaction
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.optislang_manager import OptislangManager
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.utilities.common_functions import read_log_file


class MonitoringStep(StepModel):
    """Step model of the monitoring step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    selected_actor_from_treeview: Optional[str] = None
    selected_command: Optional[str] = None
    selected_actor_from_command: Optional[str] = None
    selected_actor_from_treeview_states_ids: list = []
    commands_locked: bool = False
    auto_update_frequency: float = 2000
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
    command_timeout: int = 30

    # File storage ----------------------------------------------------------------------------------------------------

    # Output
    optislang_log_file: FileReference = FileReference("Problem_Setup/pyoptislang.log")
    project_status_info_file: FileReference = FileReference("Problem_Setup/project_status_info.json")
    actors_info_file: FileReference = FileReference("Problem_Setup/actors_info.json")
    actors_status_info_file: FileReference = FileReference("Problem_Setup/actors_status_info.json")
    actors_states_ids_file: FileReference = FileReference("Problem_Setup/actors_states_ids.json")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        problem_setup_step=StepSpec(
            download=[
                "osl_server_host",
                "osl_server_port",
                "project_tree",
                "optislang_log_level",
            ]
        ),
        self=StepSpec(
            upload=[
                "project_state",
                "project_status_info_file",
                "actors_info_file",
                "actors_status_info_file",
                "actors_states_ids_file",
                "optislang_logs",
                "optislang_log_file",
                "results_files",
            ],
        )
    )
    @instance("problem_setup_step.osl", identifier="osl")
    @long_running
    def upload_project_data(self, problem_setup_step: ProblemSetupStep, osl: OptislangManager) -> None:
        """Monitor the progress of the optiSLang project and continuously upload project data."""
        # Creat monitoring directory
        Path(self.optislang_log_file.path).parent.mkdir(parents=True, exist_ok=True)

        # Configure logging.
        osl_logger = logging.OslLogger(
            loglevel=problem_setup_step.optislang_log_level,
            log_to_file=True,
            logfile_name=self.optislang_log_file.path,
            log_to_stdout=True,
        )
        osl.instance.__logger = osl_logger.add_instance_logger(osl.instance.name, osl.instance, problem_setup_step.optislang_log_level)

        # Monitor project state and upload data.
        while True:
            # Get project state
            self.project_state = osl.instance.project.get_status()
            osl.instance.log.info(f"Analysis status: {self.project_state}")
            # Get project status info
            with open(self.project_status_info_file.path, "w") as json_file: json.dump(osl.instance.get_osl_server().get_full_project_status_info(), json_file)
            # Read pyoptislang logs
            self.optislang_logs = read_log_file(self.optislang_log_file.path)
            # Get actor status info
            actors_info, actors_status_info, actors_states_ids = {}, {}, {}
            for node_info in problem_setup_step.project_tree:
                if node_info["uid"] == osl.instance.project.root_system.uid:
                    node = osl.instance.project.root_system
                else:
                    node = osl.instance.project.root_system.find_node_by_uid(node_info["uid"], search_depth=-1)
                actors_info[node.uid] = osl.instance.get_osl_server().get_actor_info(node.uid)
                actors_states_ids[node.uid] = node.get_states_ids()
                if node.get_states_ids():
                    actors_status_info[node.uid] = []
                    for hid in node.get_states_ids():
                        actors_status_info[node.uid].append(
                            osl.instance.get_osl_server().get_actor_status_info(node.uid, hid)
                        )
            with open(self.actors_info_file.path, "w") as json_file: json.dump(actors_info, json_file)
            with open(self.actors_status_info_file.path, "w") as json_file: json.dump(actors_status_info, json_file)
            with open(self.actors_states_ids_file.path, "w") as json_file: json.dump(actors_states_ids, json_file)
            # Upload fields
            self.transaction.upload(["project_state"])
            self.transaction.upload(["project_status_info_file"])
            self.transaction.upload(["actors_info_file"])
            self.transaction.upload(["actors_status_info_file"])
            self.transaction.upload(["optislang_logs"])
            self.transaction.upload(["actors_states_ids_file"])
            if self.project_state == "FINISHED":
                break
            time.sleep(3) # Waiting 3 sec before pulling new data. The frequency might be adjusted in the future.


    @transaction(
        problem_setup_step=StepSpec(
            download=[
                "osl_server_host",
                "osl_server_port",
                "project_tree",
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
    @instance("problem_setup_step.osl", identifier="osl")
    def control_node_state(self, problem_setup_step: ProblemSetupStep, osl: OptislangManager) -> None:
        """Update the state of root or actor node based on the selected command in the UI."""
        if not self.selected_actor_from_command == "shutdown":
            if self.selected_actor_from_command == osl.instance.project.root_system.uid:
                node = osl.instance.project.root_system
                self.actor_uid = None
            else:
                node = osl.instance.project.root_system.find_node_by_uid(self.selected_actor_from_command, search_depth=-1)
                self.actor_uid = node
        else:
            node = osl.instance.project.root_system

        status = node.control(self.selected_command, wait_for_completion=True, timeout=self.command_timeout)

        if not status:
            raise Exception(f"{self.selected_command.replace('_', ' ').title()} command against node {node.get_name()} failed.")
