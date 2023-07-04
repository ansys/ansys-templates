# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import json
from pathlib import Path
from typing import Union

from ansys.optislang.core import Optislang


def get_node_tree(data: Union[list, dict], depth: int = 1) -> list:

    if isinstance(data, dict):
        node_tree = []
        depth += 1
        node_tree.append(
            {
                "key": f'{data["name"].lower()}_{data["uid"]}',
                "text": data["name"],
                "depth": depth,
                "uid": data["uid"],
                "type": data["type"],
                "kind": data["kind"],
                "is_root": False,
            }
        )
        if "nodes" in data.keys():
            node_tree.extend(get_node_tree(item, depth=1))
        return node_tree
    elif isinstance(data, list):
        node_tree = []
        for item in data:
            node_tree.extend(get_node_tree(item, depth=depth))
        return node_tree


def dump_project_state(project_file: Path, project_state_file: Path) -> None:
    """Start PyOptiSLang and dump project state file."""

    osl = Optislang(
        project_path=project_file,
        loglevel="INFO",
        reset=True,
        shutdown_on_finished=True,
        dump_project_state=project_state_file,
        ini_timeout=50,
    )

    osl.dispose()

    if not project_state_file.exists():
        raise Exception("The project state file has not been generated.")


def get_osl_project_tree(project_state_file: Path) -> dict:
    """Read the project tree of an optiSLang project."""

    with open(str(project_state_file.absolute())) as f:
        response = json.load(f)

    # Initialize project tree with default steps.
    project_tree = [
        {
            "key": "problem_setup_step",
            "text": "Problem Setup",
            "depth": 0,
            "uid": None,
            "type": None,
            "kind": None,
            "is_root": False,
        },
    ]

    root_system = response["projects"][0]["system"]

    # Declare root.
    project_tree.extend(
        [
            {
                "key": f'{root_system["name"].lower()}_{root_system["uid"]}',
                "text": f'{root_system["name"]} (root)',
                "depth": 0,
                "uid": root_system["uid"],
                "type": root_system["type"],
                "kind": root_system["kind"],
                "is_root": True,
            },
        ]
    )

    # Declare nodes.
    for node in root_system["nodes"]:
        depth = 1
        project_tree.append(
            {
                "key": f'{node["name"].lower()}_{node["uid"]}',
                "text": node["name"],
                "depth": depth,
                "uid": node["uid"],
                "type": node["type"],
                "kind": node["kind"],
                "is_root": False,
            }
        )
        if "nodes" in node.keys():
            project_tree.extend(get_node_tree(node["nodes"], depth=depth))

    return {"project_tree": project_tree}


def get_osl_project_tree_from_opf(project_file: Path, project_state_file: Path) -> dict:
    """Read an optiSLang project file and return the project tree in a dictionary."""

    dump_project_state(project_file, project_state_file)

    return get_osl_project_tree(project_state_file)


def get_step_list(project_tree: dict) -> list:
    """Return a list of steps to feed the AnsysDashTreeview component."""

    return project_tree["project_tree"]


def get_node_list(project_tree: dict) -> list:
    """Return the list of nodes in the optiSLang project file."""

    return [
        node_info
        for node_info in project_tree["project_tree"]
        if node_info["key"] not in ["problem_setup_step"]
    ]


# model_directory = Path(__file__).absolute().parent
# assets_directory = model_directory / "assets"
# project_file = assets_directory / "hook_optimization.opf"
# project_state_file = assets_directory / "project_state.json"

# project_tree = get_osl_project_tree_from_opf(project_file, project_state_file)

# step_list = get_step_list(project_tree)
# node_list = get_node_list(project_tree)

# print(step_list)
# print()
# print(node_list)

