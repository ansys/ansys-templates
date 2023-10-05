# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the design table view."""

import json

from dash_extensions.enrich import html, Input, Output, State, dcc
from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.datamodel import datamodel
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.design_table import DesignTableAIO


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the design table view."""

    # Get project data
    project_data = json.loads(problem_setup_step.project_data_file.read_text())
    # Get actor uid
    actor_uid = monitoring_step.selected_actor_from_treeview
    # Get actor hid
    actor_hid = monitoring_step.selected_state_id
    # Collect design table data
    if monitoring_step.selected_state_id:
        design_table_data = project_data["actors"][actor_uid]["design_table"][actor_hid]
    else:
        design_table_data = datamodel.extract_design_table_data({})
    # Build layout
    return html.Div(
        [
            html.Br(),
            html.Div(
                id="design_table",
                children=DesignTableAIO(
                    design_table_data,
                )
            ),
            dcc.Interval(
                id="design_table_auto_update",
                interval=monitoring_step.auto_update_frequency,  # in milliseconds
                n_intervals=0,
                disabled=False if monitoring_step.auto_update_activated else True
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
    """Enable/Disable auto update."""
    return not on


@callback(
    Output("design_table", "children"),
    Output("selected_state_dropdown", "options"),
    Output("selected_state_dropdown", "value"),
    Input("design_table_auto_update", "n_intervals"),
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
    # Get project data
    project_data = json.loads(problem_setup_step.project_data_file.read_text())
    # Get actor uid
    actor_uid = monitoring_step.selected_actor_from_treeview
    # Get actor hid
    actor_hid = monitoring_step.selected_state_id
    # Collect design table data
    if monitoring_step.selected_state_id:
        design_table_data = project_data["actors"][actor_uid]["design_table"][actor_hid]
    else:
        design_table_data = datamodel.extract_design_table_data({})
    # Collect states ids
    if not monitoring_step.selected_state_id:
        if len(project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"]):
            monitoring_step.selected_state_id = project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"][0]
    return (
        DesignTableAIO(design_table_data),
        project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"],
        monitoring_step.selected_state_id
    )
