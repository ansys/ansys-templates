# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import json
from pathlib import Path
from typing import Union


def _get_root_by_name(tcp_server_response: dict, root_name: str) -> dict:
    """Get root data by name."""

    for root in tcp_server_response["projects"]:
        if root["system"]["name"].lower() == root_name.lower():
            return root["system"]

    raise Exception(f"Unable to find root with name {root_name}.")


def _get_root_by_uid(tcp_server_response: dict, uid: str) -> dict:

    for root in tcp_server_response["projects"]:
        if root["system"]["uid"] == uid:
            return root["system"]

    raise Exception(f"Unable to find root with uid {uid}.")


def _get_node_by_uid(data: dict, uid: str) -> dict:

    pause = True

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "uid" and value == uid:
                return data
            elif isinstance(value, (dict, list)):
                result = _get_node_by_uid(value, uid)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for node in data:
            result = _get_node_by_uid(node, uid)
            if result is not None:
                return result

    return None


def _get_actor_hids(actor_states: dict) -> list:

    if "states" in actor_states.keys():
        return [state["hid"] for state in actor_states["states"]]
    else:
        return []


def read_optislang_logs(log_file: Union[Path, str]) -> list:

    logs = []

    log_file = Path(log_file)

    if log_file.exists():
        with open(log_file, "r") as file:
            for line in file:
                if len(line.strip().rstrip("\n").replace(" ", "")) > 0:
                    logs.append(line.strip().rstrip("\n"))
    else:
        raise FileNotFoundError(f"Unable to find log file {log_file}.")

    return logs


def test_() -> None:

    working_directory = Path(__file__).parent.absolute()
    response_file = working_directory / "get_full_project_tree_with_properties.json"

    with open(response_file) as f:
        response = json.load(f)

    test_nodes = [
        {"uid": "bcc95c97-0313-4bee-971a-a84aa2ff6dc1", "name": "{{ cookiecutter.__solution_name_slug }}"},
        {"uid": "4b3d77be-efcb-4d8f-ac49-9deeed1900e2", "name": "AMOP"},
        {"uid": "17622ac8-158f-4ae7-85f4-1156975a75e4", "name": "hook"},
        {"uid": "75746764-9e04-4bc6-a810-f8cdf0dd8bd4", "name": "ETK"},
        {"uid": "dfe29781-f507-462c-bdec-f75e726dd501", "name": "NLPQL"},
        {"uid": "d5ee9376-3885-4671-bd29-d7af3283b89c", "name": "MOP Solver"},
        {"uid": "5355d7c6-b7be-4ed0-9a35-59c4d180bbf7", "name": "Postprocessing"},
        {"uid": "70c2aadf-9a45-4098-9036-e5c27a924d16", "name": "Filter designs"},
        {"uid": "8521baa0-482c-4c93-baff-d6e8690a316d", "name": "Validator System"},
        {"uid": "0a74788b-8d54-467b-8926-5fa6f2dc1279", "name": "hook"},
        {"uid": "2892af77-59ff-4a33-b343-1f432ffac415", "name": "ETK"},
        {"uid": "c70eacf6-dc63-4844-ba6d-1d4f853e0f04", "name": "Batch Script"},
        {"uid": "c888a27c-76e3-4b15-82fa-4c95be8b5c13", "name": "Append designs"},
        {"uid": "2976c166-0ba1-4d6b-b291-3f8c1615dd3f", "name": "Validator Postprocessing"},
    ]

    # root = _get_root_by_name(response, "{{ cookiecutter.__solution_name_slug }}")
    for test_node in test_nodes:
        output = _get_node_by_uid(response, test_node["uid"])
        if output["name"] == test_node["name"]:
            print("Success")
        else:
            print("Failure")
