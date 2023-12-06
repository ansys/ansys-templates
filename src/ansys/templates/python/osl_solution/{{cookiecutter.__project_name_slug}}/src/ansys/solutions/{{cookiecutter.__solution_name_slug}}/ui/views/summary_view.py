# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

import dash_bootstrap_components as dbc
import json
import pandas as pd
from json.decoder import JSONDecodeError
import logging

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import html, Input, Output, State, dcc
from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.saf.glow.core.method_status import MethodStatus

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.datamodel import datamodel
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_information_table import ActorInformationTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.button_group import ButtonGroup
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.node_control import NodeControlAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_logs_table import ActorLogsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_statistics_table import ActorStatisticsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import extract_dict_by_key, LOG_MESSAGE_COLORS


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the summary view."""
    # Get project data
    project_data = json.loads(problem_setup_step.project_data_file.read_text())
    # Get actor info
    actor_info = extract_dict_by_key(problem_setup_step.osl_project_tree, "uid", monitoring_step.selected_actor_from_treeview, expect_unique=True, return_index=False)
    # Get actor uid
    actor_uid = monitoring_step.selected_actor_from_treeview
    # Get actor hid
    actor_hid = monitoring_step.selected_state_id

    alert_props = {
        "children": monitoring_step.actor_command_execution_status["alert-message"],
        "color": monitoring_step.actor_command_execution_status["alert-color"],
        "is_open": bool(monitoring_step.actor_command_execution_status["alert-message"]),
    }
    button_group = ButtonGroup(options=monitoring_step.actor_btn_group_options, disabled=monitoring_step.commands_locked).buttons

    # Collect node-specific data
    if monitoring_step.selected_state_id:
        actor_information_data = project_data["actors"][actor_uid]["information"][actor_hid]
    else:
        actor_information_data = datamodel.extract_actor_information_data({}, {}, actor_info["kind"])
    actor_log_data = project_data["actors"][actor_uid]["log"]
    actor_statistics_data = project_data["actors"][actor_uid]["statistics"]

    # Assemble UI components
    content = [
        html.Br(),
        html.Div(
            id="alerts_container",
            style={"position": "fixed", "top": 130, "right": 10, "width": 350},
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        ActorInformationTableAIO(
                            actor_information_data,
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
                        actor_log_data,
                        monitoring_step.selected_page,
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
                            actor_statistics_data,
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
        html.Div(id="dummy-output", style= {'display': 'block'}),
    ]

    # Build layout
    return html.Div(content)


@callback(
    Output("alerts_container", "children"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def display_alerts(n_intervals, pathname):
    # Get project
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    # Get problem setup step
    problem_setup_step = project.steps.problem_setup_step

    alerts_container = []

    method_state = problem_setup_step.get_long_running_method_state("start_and_monitor_osl_project")
    if method_state.status == MethodStatus.Failed:
        alerts_container.append(
            dbc.Toast(
                method_state.exception_message,
                header="Error",
                is_open=True,
                dismissable=True,
                icon="danger",
            )
        )

    if len(problem_setup_step.alerts) > 0:
        if problem_setup_step.alerts:
            alerts_container.append(
                dbc.Toast(
                    problem_setup_step.alerts["message"],
                    header=problem_setup_step.alerts["level"].capitalize(),
                    is_open=True,
                    dismissable=True,
                    icon=LOG_MESSAGE_COLORS[problem_setup_step.alerts["level"]],
                )
            )
        return alerts_container
    else:
        raise PreventUpdate


@callback(
    Output("actor_information_table", "children"),
    Output(ActorLogsTableAIO.ids.datatable("actor_logs_table"), "data"),
    Output(ActorLogsTableAIO.ids.datatable("actor_logs_table"), "store_value"),
    Output("actor_statistics_table", "children"),
    Output("selected_state_dropdown", "options"),
    Output("selected_state_dropdown", "value"),
    Output("summary_auto_update", "disabled"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
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
        try:
            # Get project data
            project_data = json.loads(problem_setup_step.project_data_file.read_text())
            # Get actor info
            actor_info = extract_dict_by_key(problem_setup_step.osl_project_tree, "uid", monitoring_step.selected_actor_from_treeview, expect_unique=True, return_index=False)
            # Get actor uid
            actor_uid = monitoring_step.selected_actor_from_treeview
            # Get actor hid
            actor_hid = monitoring_step.selected_state_id
            # Collect actor information data
            if monitoring_step.selected_state_id:
                actor_information_data = project_data.get("actors").get(actor_uid).get("information").get(actor_hid)
            else:
                actor_information_data = datamodel.extract_actor_information_data({}, actor_info["kind"])
            # Collect actor log data
            actor_log_data = project_data.get("actors").get(actor_uid).get("log")
            # Collect actor statistics data
            actor_statistics_data = project_data.get("actors").get(actor_uid).get("statistics")
            # Collect states ids
            if not monitoring_step.selected_state_id:
                if len(project_data.get("actors").get(monitoring_step.selected_actor_from_treeview).get("states_ids")):
                    monitoring_step.selected_state_id = project_data.get("actors").get(monitoring_step.selected_actor_from_treeview).get("states_ids")[0]
            return (
                ActorInformationTableAIO(actor_information_data),
                pd.DataFrame(actor_log_data).to_dict('records'),
                monitoring_step.selected_page,
                ActorStatisticsTableAIO(actor_statistics_data),
                project_data.get("actors").get(monitoring_step.selected_actor_from_treeview).get("states_ids"),
                monitoring_step.selected_state_id,
                True if problem_setup_step.osl_project_state in ["NOT STARTED", "FINISHED", "ABORTED"] else False
            )
        except Exception as e:
            logging.error(str(e))
            raise PreventUpdate
    else:
        raise PreventUpdate


@callback(
    Output("dummy-output", 'children'),
    Input(ActorLogsTableAIO.ids.datatable("actor_logs_table"), "page_current"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_table(page_current, pathname):

    # Get project
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    # Get monitoring step
    monitoring_step = project.steps.monitoring_step
    monitoring_step.selected_page = page_current
    return f"Dummy output updated {page_current}"