# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the scenery view tab."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
import optislang_dash_lib

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the scenery view tab."""

    monitoring_step.get_project_state() # fetches data on page load

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    html.Div(
                        [
                            optislang_dash_lib.SceneryComponent(
                                id="input",
                                project_state=monitoring_step.project_state,
                            ),
                        ]
                    )
                ],
            ),
        ]
    )
