# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the project summary step."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.project_summary_table import ProjectSummaryTable


def layout(project_status_info: dict, font_size: str = "15px") -> html.Div:
    """Layout of the project summary view."""

    project_summary_table = ProjectSummaryTable()

    if project_status_info:
        project_summary_table.project_status_info = project_status_info

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Project Information", className="card-title"),
                                        project_summary_table.render(),
                                    ]
                                ),
                            ],
                            color="warning",
                            outline=True,
                        ),
                        width=12,
                    ),
                ]
            ),
        ]
    )
