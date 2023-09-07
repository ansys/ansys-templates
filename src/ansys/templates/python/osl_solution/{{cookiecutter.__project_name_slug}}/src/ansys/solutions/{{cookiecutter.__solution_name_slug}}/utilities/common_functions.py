# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Common functions."""

import dash_bootstrap_components as dbc
import re

from dash_extensions.enrich import html
from pathlib import Path
from typing import Any, Iterable, Union


MONITORING_TABS = [
    {
        "label": "Project Summary",
        "tab_id": "project_summary_tab",
        "is_root": True,
        "is_system": False,
        "is_actor": False,
    },
    {"label": "Summary", "tab_id": "summary_tab", "is_root": False, "is_system": True, "is_actor": True},
    {"label": "Result Files", "tab_id": "result_files_tab", "is_root": True, "is_system": False, "is_actor": False},
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


def get_treeview_items_from_project_tree(project_tree: list) -> list:

    treeview_items = [
        {
            "key": "problem_setup_step",
            "text": "Problem Setup",
            "depth": 0,
            "uid": None,
        },
    ]

    for node in project_tree:
        if node["kind"] == "system":
            treeview_items.append(
                {
                    "key": f'{node["name"].lower()}_{node["uid"]}_toggle',
                    "text": node["name"],
                    "depth": node["level"],
                    "uid": node["uid"],
                }
            )
        treeview_items.append(
            {
                "key": f'{node["name"].lower()}_{node["uid"]}',
                "text": node["name"],
                "depth": node["level"] + 1 if node["kind"] == "system" else node["level"],
                "uid": node["uid"],
            }
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


def update_alerts(problem_setup_step, monitoring_step) -> list:
    """Update all Alerts."""

    alerts = []

    # Product version alerts
    for product_name, product_data in problem_setup_step.ansys_ecosystem.items():
        alerts.append(
            html.Div(
                [
                    dbc.Button(
                        f"{product_data['alias']} Version",
                        id=f"popover_{product_name}_version_target",
                        disabled=False,
                        color=product_data["alert_color"],
                        n_clicks=0,
                    ),
                    dbc.Popover(
                        [
                            dbc.PopoverBody(product_data["alert_message"]),
                        ],
                        id=f"popover_{product_name}_version",
                        target=f"popover_{product_name}_version_target",
                        placement="top",
                        is_open=False,
                    ),
                ]
            ),
        )

    # optiSLang solve alert
    if monitoring_step.project_state in PROJECT_STATES.keys():
        solve_message, solve_color = PROJECT_STATES[monitoring_step.project_state]["alert"], PROJECT_STATES[monitoring_step.project_state]["color"]
    else:
        raise ValueError(f"Unknown optiSLang state: {monitoring_step.project_state}.")

    alerts.append(
        html.Div(
            [
                dbc.Button(
                    "optiSLang Solve",
                    id="popover_optislang_solve_target",
                    disabled=False,
                    color=solve_color,
                    n_clicks=0,
                ),
                dbc.Popover(
                    [
                        dbc.PopoverBody(solve_message),
                    ],
                    id="popover_optislang_solve",
                    target="popover_optislang_solve_target",
                    placement="top",
                    is_open=False,
                ),
            ]
        ),
    )

    return alerts
