# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the project summary step."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, Input, Output, State

from ansys.saf.glow.client.dashclient import callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.project_information_table import ProjectInformationTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.commands import ProjectCommandsAIO


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the project summary view."""

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(ProjectInformationTableAIO(problem_setup_step, aio_id="project_information_table"), width=12),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(ProjectCommandsAIO(problem_setup_step, aio_id="project_commands"), width=12),
                ]
            ),
        ]
    )


@callback(
    Output({'component': 'ProjectInformationTableAIO', 'subcomponent': 'interval', 'aio_id': 'project_information_table'}, "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on
