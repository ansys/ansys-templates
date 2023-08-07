# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""General purpose functions."""

import json
from pathlib import Path
import re
from typing import Any, Iterable, Union

import dash_bootstrap_components as dbc

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.constants import MONITORING_TABS


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


def remove_key_from_dictionaries(dictionaries: list, key: str) -> list:

    for dictionary in dictionaries:
        if key in dictionary:
            del dictionary[key]

    return dictionaries


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


def sorted_nicely(l) -> Iterable:
    """Sort the given iterable in the way that humans expect.
    Reference: https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def sort_dict_by_ordered_keys(dictionary: dict, list_of_keys: list) -> dict:
    return {key: dictionary[key] for key in list_of_keys if key in dictionary}


def check_empty_strings(lst) -> bool:
    for sublist in lst:
        for item in sublist:
            if not item.strip():  # Using strip() to remove leading/trailing whitespaces
                return False
    return True
