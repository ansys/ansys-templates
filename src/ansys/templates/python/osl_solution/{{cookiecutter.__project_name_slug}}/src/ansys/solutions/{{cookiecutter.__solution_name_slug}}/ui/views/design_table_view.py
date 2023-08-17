# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, Input, Output, State

from ansys.saf.glow.client.dashclient import callback

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
                    dbc.Col(DesignTableAIO(problem_setup_step, aio_id="design_table"), width=12),
                ]
            ),
        ]
    )


@callback(
    Output({'component': 'DesignTableAIO', 'subcomponent': 'interval', 'aio_id': 'design_table'}, "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on
