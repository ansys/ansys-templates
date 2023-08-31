# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provides capabilities to generate commands to the optiSLang server."""

import logging
from pathlib import Path
import time
from typing import Union

from ansys.optislang.core import Optislang
from ansys.optislang.core import server_commands as commands

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.model.optislang.project_tree import get_node_by_uid, get_node_hids


logger = logging.getLogger(__name__)


PROJECT_COMMANDS_RETURN_STATES = {
    "start": "PROCESSING",
    "restart": "PROCESSING",
    "stop": "STOPPED",
    "stop_gently": "GENTLY_STOPPED",
    "reset": "FINISHED",
}


ROOT_COMMANDS_RETURN_STATES = {
    "start": "Running",
    "restart": "Running",
    "stop": "Processing aborted",
    "stop_gently": "Gently stopped",
    "reset": "Finished",
}


ACTOR_COMMANDS_RETURN_STATES = {
    "start": "Running",
    "restart": "Running",
    "stop": "Aborted",
    "stop_gently": "Gently stopped",
    "reset": "Finished",
}


PROJECT_STATES = [
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


ACTOR_STATES = [
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


def make_osl_server_command(osl: Optislang, command: str, actor_uid: str = None, hid: str = None) -> None:

    display_command = f"commands.{command}(actor_uid = {actor_uid}, hid = {hid})"
    logger.info(f"Command to oSL server: {display_command}")

    if command == "start":
        server_response = osl.get_osl_server().send_command(commands.start(actor_uid=actor_uid, hid=hid))
    elif command == "restart":
        server_response = osl.get_osl_server().send_command(commands.restart(actor_uid=actor_uid, hid=hid))
    elif command == "stop":
        server_response = osl.get_osl_server().send_command(commands.stop(actor_uid=actor_uid, hid=hid))
    elif command == "stop_gently":
        server_response = osl.get_osl_server().send_command(commands.stop_gently(actor_uid=actor_uid, hid=hid))
    elif command == "reset":
        server_response = osl.get_osl_server().send_command(commands.reset(actor_uid=actor_uid, hid=hid))
    elif command == "shutdown":
        server_response = osl.get_osl_server().send_command(commands.shutdown())
    else:
        raise ValueError(f"Unknown command {command}.")

    if server_response[0]["status"] != "success":
        raise Exception(f"oSL {command} command failed.")


def run_osl_server_command(
    tcp_server_host: str,
    tcp_server_port: int,
    command: str,
    actor_uid: str = None,
    hid: str = None,
    retries: int = 0,
    wait_for_completion: bool = True,
    timeout: Union[float, int] = 100,
    working_directory: str = Path.cwd(),
) -> None:
    """Commands can be executed against a given actor if it started at least once."""

    file_handler = logging.FileHandler(Path(working_directory) / "server_commands.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    osl = Optislang(
        host=tcp_server_host,
        port=tcp_server_port,
        shutdown_on_finished=False
    )

    if not actor_uid or actor_uid == osl.project.root_system.uid:
        # Run command against root
        is_root = True
        node = osl.project.root_system
    else:
        is_root = False
        node = get_node_by_uid(osl, actor_uid)
        if not hid:
            # Run command against all designs
            hids = get_node_hids(osl, actor_uid)
        else:
            # Run command against the given design
            hids = [hid]

    if is_root:
        status = run_project_command(
            osl, command, retries=retries, wait_for_completion=wait_for_completion, timeout=timeout
        )
    else:
        for hid in hids:
            status = run_actor_command(osl, command, actor_uid, hid, retries=retries, timeout=timeout)
            if status == "failure":
                break

    if status == "failure":
        if is_root:
            node_level = "project"
        else:
            node_level = "actor"
        raise Exception(f"{command} command against {node_level} {node.get_name()} failed.")


def run_project_command(
    osl: Optislang, command: str, retries: int = 0, wait_for_completion: bool = True, timeout: Union[float, int] = 100
) -> None:

    attempts = 1 + retries

    status = "failure"

    for i in range(attempts):
        logger.info(f"Run {command} command against {osl.project.get_name()} project. Attempt: {i + 1}/{attempts}")
        make_osl_server_command(osl, command)
        if wait_for_completion:
            status = monitor_project_command_execution(osl, command, timeout=timeout)
            logger.info("")
            if status == "success":
                logger.info(f"{command} command against project {osl.project.get_name()} executed successfully.")
                break
        else:
            return

    return status


def monitor_project_command_execution(osl: Optislang, command: str, timeout: Union[float, int] = 100) -> bool:

    time_stamp = time.time()

    while True:
        logger.info(
            f"""Project: {osl.project.get_name()} | State: {osl.project.get_status()} | Time: {round(time.time() - time_stamp)}s""")
        if osl.project.get_status() == PROJECT_COMMANDS_RETURN_STATES[command]:
            logger.info(f"{command} command successfully executed.")
            status = "success"
            break
        if (time.time() - time_stamp) > timeout:
            logger.info("Timeout limit reached. Skip monitoring.")
            status = "failure"
            break
        time.sleep(3)

    return status


def monitor_root_command_execution(osl: Optislang, command: str, timeout: Union[float, int] = 100) -> bool:

    node = osl.project.root_system

    time_stamp = time.time()

    while True:
        if node:
            logger.info(
                f"Project: {node.get_name()} | State: {node.get_status()} | Time: {round(time.time() - time_stamp)}s"
            )
            if node.get_status() == ROOT_COMMANDS_RETURN_STATES[command]:
                logger.info(f"{command} command successfully executed.")
                is_successful = True
                break
        if (time.time() - time_stamp) > timeout:
            logger.info("Timeout limit reached. Skip monitoring.")
            is_successful = False
            break
        time.sleep(3)

    return is_successful


def run_actor_command(
    osl: Optislang,
    command: str,
    actor_uid: str,
    hid: str,
    retries: int = 0,
    wait_for_completion: bool = True,
    timeout: Union[float, int] = 100,
) -> None:

    attempts = 1 + retries

    node = get_node_by_uid(osl, actor_uid)

    status = "failure"

    for i in range(attempts):
        logger.info(f"Run {command} command against {node.get_name()} actor on hid {hid}. Attempt: {i + 1}/{attempts}")
        make_osl_server_command(osl, command, actor_uid=actor_uid, hid=hid)
        if wait_for_completion:
            status = monitor_actor_command_execution(osl, command, actor_uid, hid, timeout=timeout)
            logger.info("")
            if status == "success":
                logger.info(f"{command} command against actor {node.get_name()} on hid {hid} executed successfully.")
                break
        else:
            return

    return status


def monitor_actor_command_execution(
    osl: Optislang, command: str, actor_uid: str, hid: str, timeout: Union[float, int] = 100
) -> bool:

    node = get_node_by_uid(osl, actor_uid)

    time_stamp = time.time()

    while True:
        logger.info(
            f"""Actor: {node.get_name()} | Hid: {hid} | State: {node.get_status()} | Time: {round(time.time() - time_stamp)}s""")
        if node.get_status() == ACTOR_COMMANDS_RETURN_STATES[command]:
            logger.info(f"{command} command successfully executed.")
            status = "success"
            break
        if (time.time() - time_stamp) > timeout:
            logger.info("Timeout limit reached. Skip monitoring.")
            status = "failure"
            break
        time.sleep(3)

    return status
