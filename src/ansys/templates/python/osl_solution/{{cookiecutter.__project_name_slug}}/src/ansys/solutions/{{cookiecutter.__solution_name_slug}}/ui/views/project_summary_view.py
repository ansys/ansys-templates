# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the project summary step."""

import dash_bootstrap_components as dbc

from dash_extensions.enrich import html, Input, Output, State, dcc

from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.node_control import NodeControlAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.project_information_table import ProjectInformationTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.service_table import ServiceTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.button_group import ButtonGroup


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the project summary view."""
    alert_props = {
        "children":monitoring_step.project_command_execution_status["alert-message"],
        "color":monitoring_step.project_command_execution_status["alert-color"],
        "is_open": bool(monitoring_step.project_command_execution_status["alert-message"]),
    }
    button_group = ButtonGroup(options=monitoring_step.project_btn_group_options, disabled=monitoring_step.commands_locked).buttons

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(html.Div(ProjectInformationTableAIO(monitoring_step), id="project_information_table"), width=8),
                    dbc.Col(html.Div(ServiceTableAIO(problem_setup_step), id="service_table"), width=4),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(NodeControlAIO(button_group, alert_props, "project-commands"), width=12),
                ]
            ),
            dcc.Interval(
                id="project_summary_auto_update",
                interval=monitoring_step.auto_update_frequency,  # in milliseconds
                n_intervals=0,
                disabled=False if monitoring_step.auto_update_activated else True
            ),
        ]
    )


@callback(
    Output("project_summary_auto_update", "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on


@callback(
    Output("project_information_table", "children"),
    Input("project_summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_view(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step

    return ProjectInformationTableAIO(monitoring_step)
