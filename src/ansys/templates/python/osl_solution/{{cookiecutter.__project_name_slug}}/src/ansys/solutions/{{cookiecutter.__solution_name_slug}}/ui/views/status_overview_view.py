# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the node status overview view."""

import json
import optislang_dash_lib

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import html, Input, Output, State, dcc
from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the status overview view."""

    full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())

    return html.Div(
        [
            html.Div(
                id="status-overview-component-div1",
                children=[
                    optislang_dash_lib.Nodestatusviewcomponent(
                        id="node-status-view-component1",
                        project_state=full_project_status_info,
                    ),
                ],
                style={"display": "block"},
            ),
            html.Div(
                id="status-overview-component-div2",
                children=[
                    optislang_dash_lib.Nodestatusviewcomponent(
                        id="node-status-view-component2",
                        project_state=full_project_status_info,
                    ),
                ],
                style={"display": "none"},
            ),
            dcc.Interval(
                id="status-overview_auto_update",
                interval=monitoring_step.auto_update_frequency,  # in milliseconds
                n_intervals=0,
                disabled=False if monitoring_step.auto_update_activated else True,
            ),
        ]
    )


@callback(
    Output("status-overview-component-div1", "children"),
    Output("status-overview-component-div2", "children"),
    Output("status-overview-component-div1", "style"),
    Output("status-overview-component-div2", "style"),
    Input("status-overview_auto_update", "n_intervals"),
    State("url", "pathname"),
)
def update_view(n_intervals, pathname):
    """Update design table."""

    # Get project
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    # Get problem setup step
    problem_setup_step = project.steps.problem_setup_step
    # Get monitoring step
    monitoring_step = project.steps.monitoring_step

    if monitoring_step.auto_update_activated:
        # Get project data
        full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())

        status_overview_status_view_1_child = None
        status_overview_status_view_1_style = None
        status_overview_status_view_2_child = None
        status_overview_status_view_2_style = None

        if n_intervals % 2 == 0:  # (even)
            status_overview_status_view_1_child = (
                optislang_dash_lib.Nodestatusviewcomponent(
                    id="node-status-view-component1",
                    project_state=full_project_status_info,
                ),
            )
            status_overview_status_view_1_style = {"display": "block"}
            status_overview_status_view_2_style = {"display": "none"}
        else:
            status_overview_status_view_2_child = (
                optislang_dash_lib.Nodestatusviewcomponent(
                    id="node-status-view-component2",
                    project_state=full_project_status_info,
                ),
            )
            status_overview_status_view_2_style = {"display": "block"}
            status_overview_status_view_1_style = {"display": "none"}

        return (
            status_overview_status_view_1_child,
            status_overview_status_view_2_child,
            status_overview_status_view_1_style,
            status_overview_status_view_2_style,
        )

    else:
        raise PreventUpdate
