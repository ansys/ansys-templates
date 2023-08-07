# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc, Input, Output, State

from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.design_table import DesignTable


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the design table view."""

    design_table = DesignTable()

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        design_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
        design_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            design_table.render(),
                            id="project_design_table"
                        ),
                        width=12
                    ),
                ]
            ),
            dcc.Interval(
                id="design_table_auto_update",
                interval=1 * 2000,  # in milliseconds
                n_intervals=0,
                disabled=False
            ),
        ]
    )


@callback(
    Output("project_design_table", "children"),
    Input("design_table_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_design_table(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    design_table = DesignTable()

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        design_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
        design_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

    return design_table.render()
