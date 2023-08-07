# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.design_table import DesignTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


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
                    dbc.Col(design_table.render(), width=12),
                ]
            ),
        ]
    )
