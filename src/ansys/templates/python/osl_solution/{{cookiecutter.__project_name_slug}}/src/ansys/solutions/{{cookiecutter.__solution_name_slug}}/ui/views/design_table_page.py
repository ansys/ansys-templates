# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.design_table import DesignTable


def layout(actors_info: list, actors_status_info: dict, uid: str, font_size: str = "15px") -> html.Div:
    """Layout of the design table view."""

    design_table = DesignTable()

    if uid in actors_info.keys():
        design_table.actor_info = actors_info[uid]
    if uid in actors_status_info.keys():
        design_table.actor_status_info = actors_status_info[uid][
            0
        ]  # the index 0 here means that we arbitrarily select the 1st hid

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(design_table.render(), width=12),
                ]
            ),
        ]
    )
