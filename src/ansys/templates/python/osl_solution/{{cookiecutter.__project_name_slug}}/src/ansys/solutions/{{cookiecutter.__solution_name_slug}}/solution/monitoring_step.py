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
    selected_page: int = 0
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
    auto_update_frequency: float = 2000 # millisecond
    command_timeout: int = 30 # second

    # File storage ----------------------------------------------------------------------------------------------------

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
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
    def control_node_state(self, osl_manager: OptislangManager) -> None:
        """Update the state of root or actor node based on the selected command in the UI."""
        osl = osl_manager.instance
        if not self.selected_command == "shutdown":
            if self.selected_actor_from_command == osl.project.root_system.uid:
                node = osl.project.root_system
                self.actor_uid = None
            else:
                node = osl.project.root_system.find_node_by_uid(self.selected_actor_from_command, search_depth=-1)
                self.actor_uid = node

            status = node.control(self.selected_command, wait_for_completion=True, timeout=self.command_timeout)

            if not status:
                raise Exception(f"{self.selected_command.replace('_', ' ').title()} command against node {node.get_name()} failed.")
        else:
            osl_manager.shutdown()

