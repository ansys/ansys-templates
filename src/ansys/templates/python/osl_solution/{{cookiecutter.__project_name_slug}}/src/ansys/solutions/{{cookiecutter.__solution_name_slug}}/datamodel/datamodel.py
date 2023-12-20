# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from datetime import datetime

from ansys.solutions.{{cookiecutter.__solution_name_slug}}.utilities.common_functions import (
    remove_key_from_dictionaries,
    sort_dict_by_ordered_keys,
    convert_microseconds
)


def extract_project_status_info(full_project_status_info: dict) -> dict:
    """ Extract project status info from the optiSLang server response.

    Parameters
    ----------
    full_project_status_info: dict
        Full project status info.

    Returns
    -------
        dict
            A dictionary containing project status data.
    """

    data = {
        "State": None,
        "Id": None,
        "Name": None,
        "Machine": None,
        "Location": None,
        "Project directory": None,
        "Owner": None,
        "Registered": "--",
        "Lock info": "--"
    }

    if full_project_status_info:
        data["State"] = full_project_status_info["projects"][0].get("state", None)
        data["Id"] = full_project_status_info["projects"][0].get("project_id", None)
        data["Name"] = full_project_status_info["projects"][0].get("name", None)
        data["Machine"] = full_project_status_info["projects"][0].get("machine", None)
        data["Location"] = full_project_status_info["projects"][0].get("location", None)
        data["Project directory"] = full_project_status_info["projects"][0].get("working_dir", None)
        data["Owner"] = full_project_status_info["projects"][0].get("user", None)
        data["Registered"] = "--"
        data["Lock info"] = "--"

    return data


def extract_actor_information_data(actor_status_info: dict, actor_info: dict, kind: str) -> dict:
    """ Extract actor information data from the optiSLang server response.

    Parameters
    ----------
    actor_status_info: dict
        Actor status info.
    actor_info: dict
        Actor info.
    kind: str
        Actor kind (actor/system).

    Returns
    -------
        dict
            A dictionary containing actor information data.
    """

    data = {
        "Working directory": None,
        "Processing state": None,
        "Execution duration": None,
    }
    if kind == "system":
        data["Processed"] = None
        data["Status"] = None
        data["Succeeded"] = None
        data["Not succeeded"] = None
        data["Pending"] = None

    if actor_status_info:
        data["Working directory"] = actor_status_info.get("working dir", None)
        data["Processing state"] = actor_status_info.get("state", None)
        data["Execution duration"] = actor_status_info.get("exec_dur_us", None)
        if kind == "system":
            # Process data
            succeeded_designs = actor_status_info["succeeded_designs"]
            failed_designs = actor_status_info["failed_designs"]
            pending_designs = actor_status_info["pending_designs"]
            total_designs = actor_info["max_designs"]
            processed_designs = total_designs - pending_designs
            try:
                status = int(processed_designs / total_designs * 100)
            except ZeroDivisionError:
                status = 0
            # Update data
            data["Processed"] = f"{processed_designs} / {total_designs}"
            data["Status"] = f"{status}%"
            data["Succeeded"] = succeeded_designs
            data["Not succeeded"] = failed_designs
            data["Pending"] = pending_designs

    return data


def extract_actor_log_data(actor_info: dict) -> dict:
    """ Extract actor log data from the optiSLang server response.

    Parameters
    ----------
    actor_info: dict
        Actor info.

    Returns
    -------
        dict
            A dictionary containing actor log data.
    """

    data = {"Time": [], "Level": [], "Message": []}

    if actor_info:
        if "log_messages" in actor_info.keys():
            if len(actor_info["log_messages"]):
                # Remove hid key from list dictionaries because it is useless for UI
                # and prevent transformation to DataFrame.
                data = remove_key_from_dictionaries(actor_info["log_messages"], "hid")
                # Transform list of dictionaries into dictionary
                data = {
                    key: [d[key] for d in actor_info["log_messages"]]
                    for key in actor_info["log_messages"][0]
                }
                # Sort keys in order
                data = sort_dict_by_ordered_keys(data, ["time_stamp", "level", "message"])
                # Rename keys
                data["Time"] = data.pop("time_stamp")
                data["Level"] = data.pop("level")
                data["Message"] = data.pop("message")
                # Convert timestamp
                for index, value in enumerate(data["Time"]):
                    dt = datetime.strptime(value, "%Y%m%dT%H%M%S.%f")
                    data["Time"][index] = dt.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]

    return data


def extract_actor_statistics_data(actor_info: dict) -> dict:
    """ Extract actor statistics data from the optiSLang server response.

    Parameters
    ----------
    actor_info: dict
        Actor info.

    Returns
    -------
        dict
            A dictionary containing actor statistics data.
    """

    data = {
        "Header": ["Current Run", "All Runs"],
        "Usages": [None, None],
        "Accumulated": [None, None],
        "Minimum": [None, None],
        "Maximum": [None, None],
        "Mean": [None, None],
        "std_dev": [None, None],
    }

    if actor_info:
        for i, run in enumerate(["Current Run", "All Runs"]):
            run_type = run.split()[0].lower()
            data["Usages"][i] = actor_info["usage_stats"][run_type]["num_usages"]
            for key in data.keys():
                if key != "Header" and key != "Usages":
                    duration = actor_info["usage_stats"][run_type]["exec_duration_us"][key.lower()]
                    duration = convert_microseconds(duration)
                    data[key][i] = duration

    data["Standard devieation"] = data.pop("std_dev")

    return data


def extract_design_table_data(actor_status_info: dict) -> dict:
    """Extract design table data from the optiSLang server response.

    Parameters
    ----------
    actor_status_info: dict
        Actor status info.

    Returns
    -------
        dict
            A dictionary containing design table data.
    """

    data = {
        "Design": [],
        "Feasible": [],
        "Status": [],
        "Pareto": [],
    }

    field_types = ["parameter", "constraint", "objective", "response"]

    if actor_status_info:
        for field_type in field_types:
            field_name_index = field_type + "_names"
            for field_name in actor_status_info["designs"][field_name_index]:
                data[field_name] = []
        design_numbers = []
        for design_values in reversed(actor_status_info["designs"]["values"]):
            design_numbers.append(design_values["hid"].split(".")[-1])
            data["Design"].append(design_values["hid"])
            for field_type in field_types:
                field_name_index = field_type + "_names"
                field_value_index = field_type + "_values"
                field_names = actor_status_info["designs"][field_name_index]
                field_values = design_values[field_value_index]
                if len(field_names) != len(field_values):
                    field_values = [None for i in range(len(field_names))]
                for field_name, field_value in zip(field_names, field_values):
                    if isinstance(field_value, dict):
                        if field_value["type"] == "xy_data":
                            field_value = f"[1:%s]" % (field_value["num_entries"])
                    data[field_name].append(field_value)
        for design_status in reversed(actor_status_info["design_status"]):
            data["Feasible"].append(design_status["feasible"])
            data["Status"].append(design_status["status"])
            data["Pareto"].append(design_status["pareto_design"])

    return data
