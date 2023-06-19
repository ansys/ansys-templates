# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""A Python script to Extract system hierarchy from optiSLang project."""

# ==================================================== [Imports] ==================================================== #

import argparse
import json
from pathlib import Path
import textwrap
from typing import Union

from ansys.optislang.core import Optislang

# =================================================== [Functions] =================================================== #


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
            node_tree.append(
                {
                    "key": f'{data["name"].lower()}_{data["uid"]}_duplicate',
                    "text": data["name"],
                    "depth": depth + 1,
                    "uid": data["uid"],
                    "type": data["type"],
                    "kind": data["kind"],
                    "is_root": False,
                }
            )
            node_tree.extend(get_node_tree(item, depth=1))
        return node_tree
    elif isinstance(data, list):
        node_tree = []
        for item in data:
            node_tree.extend(get_node_tree(item, depth=depth))
        return node_tree


def get_system_hierarchy(project_state: Path) -> dict:

    with open(str(project_state.absolute())) as f:
        response = json.load(f)

    # Initialize system hierarchy with default steps.
    system_hierarchy = [
        {
            "key": "problem_setup_step",
            "text": "Problem Setup",
            "depth": 0,
            "uid": None,
            "type": None,
            "kind": None,
            "is_root": False,
        },
        {
            "key": "monitoring_step",
            "text": "Monitoring",
            "depth": 0,
            "uid": None,
            "type": None,
            "kind": None,
            "is_root": False,
        },
    ]

    root_system = response["projects"][0]["system"]

    # Declare root.
    system_hierarchy.extend(
        [
            {
                "key": f'{root_system["name"].lower()}_{root_system["uid"]}',
                "text": f'{root_system["name"]} (root)',
                "depth": 1,
                "uid": root_system["uid"],
                "type": root_system["type"],
                "kind": root_system["kind"],
                "is_root": True,
            },
            # Here we are forced to duplicate the step because the AnsysDashTreeview component considers the
            # first occurrence as a section, not a real node. This behavior has been implemented by design but
            # conflicts with what we are aiming to for optiSLang project tree.
            {
                "key": f'{root_system["name"].lower()}_{root_system["uid"]}_duplicate',
                "text": root_system["name"],
                "depth": 2,
                "uid": root_system["uid"],
                "type": root_system["type"],
                "kind": root_system["kind"],
                "is_root": True,
            },
        ]
    )

    # Declare nodes.
    for node in root_system["nodes"]:
        depth = 2
        system_hierarchy.append(
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
            # Duplicate step because is contains substeps (see comments above).
            system_hierarchy.append(
                {
                    "key": f'{node["name"].lower()}_{node["uid"]}_duplicate',
                    "text": node["name"],
                    "depth": depth + 1,
                    "uid": node["uid"],
                    "type": node["type"],
                    "kind": node["kind"],
                    "is_root": False,
                }
            )
            system_hierarchy.extend(get_node_tree(node["nodes"], depth=depth))

    return system_hierarchy


def parser() -> None:
    """Parse command line arguments."""

    # Code Name
    program_name = "Extract system hierarchy from optiSLang project."
    # Code description
    program_description = "A Python script to Extract system hierarchy from optiSLang project."
    # Create top-level parser
    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=None,
        prefix_chars="-",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(program_description),
    )
    parser._action_groups.pop()
    # Definition of the group of arguments
    required_inputs = parser.add_argument_group("Required arguments")
    # Required parameters
    required_inputs.add_argument(
        "-p",
        "--project-file",
        type=Path,
        help="Path to the optiSLang project file.",
        required=True,
    )

    return parser.parse_args()


def main():
    """Entry point."""

    scripts_directory = Path(__file__).parent.absolute()
    assets_directory = scripts_directory.parent / "assets"
    project_state_file = assets_directory / "project_state.json"
    system_hierarchy_file = assets_directory / "system_hierarchy.json"

    args = parser()

    osl = Optislang(
        project_path=args.project_file,
        loglevel="INFO",
        reset=True,
        shutdown_on_finished=True,
        dump_project_state=project_state_file,
        ini_timeout=30,  # might need to be adjusted
    )

    osl.dispose()

    if project_state_file.exists():
        system_hierarchy = {"system_hierarchy": get_system_hierarchy(project_state_file)}
    else:
        raise Exception("No project state file detected. Unable to retrieve system hierarchy.")

    with open(system_hierarchy_file, "w") as file:
        json.dump(system_hierarchy, file)

    project_state_file.unlink()


# =================================================== [Execution] =================================================== #

if __name__ == "__main__":
    main()
