# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

import dash_bootstrap_components as dbc
import pandas as pd

from dash_extensions.enrich import html, Input, Output, State, dcc
from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.datamodel import datamodel
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_information_table import ActorInformationTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.button_group import ButtonGroup
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.node_control import NodeControlAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_logs_table import ActorLogsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_statistics_table import ActorStatisticsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import extract_dict_by_key


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the summary view."""

    actor_info = extract_dict_by_key(problem_setup_step.project_tree, "uid", monitoring_step.selected_actor_from_treeview, expect_unique=True, return_index=False)

    alert_props = {
        "children": monitoring_step.actor_command_execution_status["alert-message"],
        "color": monitoring_step.actor_command_execution_status["alert-color"],
        "is_open": bool(monitoring_step.actor_command_execution_status["alert-message"]),
    }
    button_group = ButtonGroup(options=monitoring_step.actor_btn_group_options, disabled=monitoring_step.commands_locked).buttons

    # Collect node-specific data
    if monitoring_step.selected_state_id:
        actor_information = monitoring_step.actors_information[monitoring_step.selected_actor_from_treeview][monitoring_step.selected_state_id]
    else:
        actor_information = datamodel.extract_actor_information_data({}, actor_info["kind"])
    actor_log = monitoring_step.actors_log[monitoring_step.selected_actor_from_treeview]
    actor_statistics = monitoring_step.actors_statistics[monitoring_step.selected_actor_from_treeview]

    # Assemble UI components
    content = [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        ActorInformationTableAIO(
                            actor_information,
                        ),
                        id="actor_information_table"
                    ),
                    width=12
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    NodeControlAIO(
                        button_group,
                        alert_props,
                        "actor-commands"
                    ),
                    width=12
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    ActorLogsTableAIO(
                        actor_log,
                        aio_id = "actor_logs_table"
                    ),
                    width=12
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        ActorStatisticsTableAIO(
                            actor_statistics,
                        ),
                        id = "actor_statistics_table"
                    ),
                    width=12
                ),
            ]
        ),
        dcc.Interval(
            id="summary_auto_update",
            interval=monitoring_step.auto_update_frequency,  # in milliseconds
            n_intervals=0,
            disabled=False if monitoring_step.auto_update_activated else True
        ),
    ]

    # Build layout
    return html.Div(content)


@callback(
    Output("summary_auto_update", "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on


@callback(
    Output("actor_information_table", "children"),
    Output(ActorLogsTableAIO.ids.datatable("actor_logs_table"), "data"),
    Output("actor_statistics_table", "children"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_view(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    monitoring_step = project.steps.monitoring_step

    actor_info = extract_dict_by_key(problem_setup_step.project_tree, "uid", monitoring_step.selected_actor_from_treeview, expect_unique=True, return_index=False)

    if monitoring_step.selected_state_id:
        actor_information = monitoring_step.actors_information[monitoring_step.selected_actor_from_treeview][monitoring_step.selected_state_id]
    else:
        actor_information = datamodel.extract_actor_information_data({}, actor_info["kind"])

    return (
        ActorInformationTableAIO(actor_information),
        pd.DataFrame(monitoring_step.actors_log[monitoring_step.selected_actor_from_treeview]).to_dict('records'),
        ActorStatisticsTableAIO(monitoring_step.actors_statistics[monitoring_step.selected_actor_from_treeview])
    )
