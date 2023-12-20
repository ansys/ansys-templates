# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Common functions."""

import dash_bootstrap_components as dbc
import re

from pathlib import Path
from typing import Any, Iterable, Union, Tuple

from ansys.optislang.core.osl_server import OslServer


MONITORING_TABS = [
    {
        "label": "Project Summary",
        "tab_id": "project_summary_tab",
        "is_root": True,
        "is_system": False,
        "is_actor": False,
    },
    {"label": "Summary", "tab_id": "summary_tab", "is_root": False, "is_system": True, "is_actor": True},
    {"label": "Scenery", "tab_id": "scenery_tab", "is_root": True, "is_system": False, "is_actor": False},
    {"label": "Design Table", "tab_id": "design_table_tab", "is_root": True, "is_system": True, "is_actor": False},
    {"label": "Visualization", "tab_id": "visualization_tab", "is_root": True, "is_system": True, "is_actor": False},
    {"label": "Status Overview", "tab_id": "status_overview_tab", "is_root": True, "is_system": True, "is_actor": True},
]


PROJECT_STATES = {
    "NOT STARTED": {
        "alert": "optiSLang project not started.",
        "color": "warning"
    },
    "IDLE": {
        "alert": "optiSLang project is pending.",
        "color": "warning"
    },
    "PROCESSING": {
        "alert": "optiSLang project in progress.",
        "color": "primary"
    },
    "PAUSED": {
        "alert": "optiSLang project paused.",
        "color": "warning"
    },
    "PAUSE_REQUESTED": {
        "alert": "optiSLang project requested to pause.",
        "color": "warning"
    },
    "STOPPED": {
        "alert": "optiSLang project stopped.",
        "color": "warning"
    },
    "STOP_REQUESTED": {
        "alert": "optiSLang project requetsed to stop.",
        "color": "warning"
    },
    "GENTLY_STOPPED": {
        "alert": "optiSLang project gently stopped.",
        "color": "warning"
    },
    "GENTLE_STOP_REQUESTED": {
        "alert": "optiSLang project requested to gently stop.",
        "color": "warning"
    },
    "FINISHED": {
        "alert": "optiSLang project completed successfully.",
        "color": "success"
    },
}


LOG_MESSAGE_COLORS = {
    "info": "primary",
    "warning": "warning",
    "error": "danger"
}


def find_dicts_by_key_recursively(structure, target_level, current_path=[]):
    results = []

    if isinstance(structure, list):
        for i, item in enumerate(structure):
            path = current_path + [i]
            results.extend(find_dicts_by_key_recursively(item, target_level, path))
    elif isinstance(structure, dict):
        if "level" in structure and structure["level"] == target_level:
            results.append(current_path)
        for key, value in structure.items():
            path = current_path + [key]
            results.extend(find_dicts_by_key_recursively(value, target_level, path))

    return results


def get_dict_from_indexes_sequence(nested_structure, mixed_keys):
    """
    Retrieve a dictionary from a complex nested structure of dictionaries and lists
    using a mixed list of keys and indexes.

    Args:
        nested_structure (dict or list): The complex nested structure.
        mixed_keys (list): List of keys and indexes to follow, in mixed order.

    Returns:
        dict: The retrieved dictionary, or None if not found.
    """
    for key_or_index in mixed_keys:
        if isinstance(nested_structure, dict) and isinstance(key_or_index, str) and key_or_index in nested_structure:
            nested_structure = nested_structure[key_or_index]
        elif isinstance(nested_structure, list) and isinstance(key_or_index, int) and 0 <= key_or_index < len(nested_structure):
            nested_structure = nested_structure[key_or_index]
        else:
            return None  # Key or index not found in the current level

    if isinstance(nested_structure, dict):
        return nested_structure
    else:
        return None  # If the final element is not a dictionary


def get_treeview_items_from_project_tree(osl_project_tree: list) -> list:

    treeview_items = [
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

    for i, node in enumerate(osl_project_tree):
        if node["is_root"]:
            treeview_items.append(
                {
                    "id": node["uid"],
                    "text": node["name"],
                    "expanded": True,
                    "prefixIcon": {
                        "src": "https://s2.svgbox.net/materialui.svg?ic=account_tree"
                    },
                    "level": 0,
                    "children": []
                }
            )
        else:
            # Find parent node
            matching_indexes = find_dicts_by_key_recursively(treeview_items, (node["level"] - 1))
            if len(matching_indexes) == 0:
                raise Exception("Unable to find parent node.")
            parent_node = get_dict_from_indexes_sequence(treeview_items, matching_indexes[-1])
            if node["kind"] == "system":
                icon = "https://s2.svgbox.net/materialui.svg?ic=workspaces_filled"
            elif node["kind"] == "actor":
                icon = "https://s2.svgbox.net/materialui.svg?ic=workspaces_outline"
            else:
                raise ValueError(f"Unknown actor kind {node['kind']}.")
            parent_node["children"].append(
                {
                    "id": node["uid"],
                    "text": node["name"],
                    "expanded": True,
                    "prefixIcon": {
                        "src": icon
                    },
                    "level": node["level"],
                    "children": []
                },
            )

    return treeview_items


def check_empty_strings(lst) -> bool:
    for sublist in lst:
        for item in sublist:
            if not item.strip():  # Using strip() to remove leading/trailing whitespaces
                return False
    return True


def sort_dict_by_ordered_keys(dictionary: dict, list_of_keys: list) -> dict:
    return {key: dictionary[key] for key in list_of_keys if key in dictionary}


def sorted_nicely(l) -> Iterable:
    """Sort the given iterable in the way that humans expect.
    Reference: https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def convert_microseconds(duration: int) -> str:
    """Convert a time duration in microseconds into a string with format: WWh XXmin YYs ZZms."""

    milliseconds = duration // 1000
    microseconds = duration % 1000
    seconds = milliseconds // 1000
    milliseconds = milliseconds % 1000
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60

    return f"{int(hours):02}h {int(minutes):02}m {int(seconds):02}s {int(milliseconds):03}ms"


def remove_key_from_dictionaries(dictionaries: list, key: str) -> list:

    for dictionary in dictionaries:
        if key in dictionary:
            del dictionary[key]

    return dictionaries


def update_list_of_tabs(node_info: dict) -> list:

    list_of_tabs = []

    for tab_info in MONITORING_TABS:
        if (
            node_info["is_root"]
            and tab_info["is_root"]
            or not node_info["is_root"]
            and node_info["kind"] == "system"
            and tab_info["is_system"]
            or not node_info["is_root"]
            and node_info["kind"] == "actor"
            and tab_info["is_actor"]
        ):
            list_of_tabs.append(
                dbc.Tab(
                    label=tab_info["label"],
                    tab_id=tab_info["tab_id"],
                    label_style={
                        "color": "#000000",
                        "text-color": "#000000",
                    },
                    active_label_style={
                        "color": "#FFFFFF",
                        "text-color": "#000000",
                        "background-color": "#000000",
                        "border-style": "solid",
                        "border-color": "#000000",
                    },
                )
            )

    return list_of_tabs


def extract_dict_by_key(dictionaries: list, key: str, value: Any, expect_unique: bool = False, return_index: bool = True) -> Union[None, dict]:
    """Given a list of dictionaries, return the ones matching specific key and value."""

    matches, indexes = [], []

    for (index, dictionary) in enumerate(dictionaries):
        if dictionary.get(key) == value:
            matches.append(dictionary)
            indexes.append(index)

    if expect_unique:
        if len(matches) == 0:
            raise Exception(f"No matching dictionaries with key {key} and value {value}.")
        elif len(matches) == 1:
            result_m = matches[0]
            result_i = indexes[0]
        else:
            raise Exception(f"Multiple matches found with key {key} and value {value}.")
    else:
        result_m = matches
        result_i = indexes

    return (result_m, result_i) if return_index else result_m


def read_log_file(log_file: Union[Path, str]) -> list:

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


def update_placeholders(ui_values: list, placeholders: dict) -> dict:
    """Information needed."""

    updated_dict = {}
    for row in ui_values[1:]:
        parameter_name = row["props"]["children"][0]["props"]["children"]["props"]["children"]
        input_value = row["props"]["children"][1]["props"]["children"]["props"]["value"]

        placeholder_values = placeholders.get("placeholder_values")
        if parameter_name in placeholder_values:
            updated_dict[parameter_name] = input_value
    return updated_dict


def check_optislang_server(osl_server: OslServer) -> None:
    """optiSLang server health check."""

    try:
        server_is_alive = osl_server.get_server_is_alive()
    except Exception as e:
        return False

    return server_is_alive


def get_states_ids_from_states(actor_states: dict) -> Tuple[str]:
    """Get available actor states ids from actor states response."""
    if not actor_states.get("states", None):
        return tuple([])
    return tuple([state["hid"] for state in actor_states["states"]])
