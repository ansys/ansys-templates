# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the project summary step."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc, Input, Output, State

from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.project_summary_table import ProjectSummaryTable


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the project summary view."""

    project_summary_table = ProjectSummaryTable()

    if problem_setup_step.project_status_info:
        project_summary_table.project_status_info = problem_setup_step.project_status_info

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
                                        html.Div(
                                            project_summary_table.render(),
                                            id="project_summary_table"
                                        ),
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
            dcc.Interval(
                id="project_summary_auto_update",
                interval=1 * 2000,  # in milliseconds
                n_intervals=0,
                disabled=False
            ),
        ]
    )


@callback(
    Output("project_summary_table", "children"),
    Input("project_summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_design_table(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    project_summary_table = ProjectSummaryTable()

    if problem_setup_step.project_status_info:
        project_summary_table.project_status_info = problem_setup_step.project_status_info

    return project_summary_table.render()
