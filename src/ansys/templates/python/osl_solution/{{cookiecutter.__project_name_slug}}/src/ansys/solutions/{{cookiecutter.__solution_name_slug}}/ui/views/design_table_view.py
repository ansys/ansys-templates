# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, Input, Output, State, dcc

from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.design_table import DesignTableAIO


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the design table view."""

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(html.Div(DesignTableAIO(problem_setup_step), id="design_table"), width=12),
                ]
            ),
            dcc.Interval(
                id="design_table_auto_update",
                interval=problem_setup_step.auto_update_frequency,  # in milliseconds
                n_intervals=0,
                disabled=False if problem_setup_step.auto_update_activated else True
            ),
        ]
    )


@callback(
    Output("design_table_auto_update", "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on


@callback(
    Output("design_table", "children"),
    Input("design_table_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_view(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    return DesignTableAIO(problem_setup_step)
