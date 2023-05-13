# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the second step UI."""
    # this page is used to display a diagram of system and node components of the project
    # this diagram is generated with optislang and exists in the .opf file
    # need pyoptislang commands to export this as a .png?

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dcc.Markdown("**Scenery page: Under construction**", style={"font-size": "15px"}),
                ],
            ),
        ]
    )
