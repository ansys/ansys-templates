# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the monitoring step."""

import dash_bootstrap_components as dbc
import dash_daq as daq

from dash_extensions.enrich import Input, Output, State, html
from dash.exceptions import PreventUpdate

from ansys.saf.glow.client.dashclient import DashClient, callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.views import (
    design_table_view,
    project_summary_view,
    scenery_view,
    status_overview_view,
    summary_view,
    visualization_view,
)
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import extract_dict_by_key, update_list_of_tabs


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:

    actor_info = extract_dict_by_key(problem_setup_step.osl_project_tree, "uid", monitoring_step.selected_actor_from_treeview, expect_unique=True, return_index=False)
    list_of_tabs = update_list_of_tabs(actor_info)

    return html.Div(
        [
            dbc.Stack(
                [
                    daq.BooleanSwitch(
                        id='activate_auto_update',
                        on=monitoring_step.auto_update_activated,
                        color="#FFB71B",
                        className="ms-auto",
                    ),
                    html.Div("Auto update")
                ],
                direction="horizontal",
                gap=1,
            ),
            dbc.Tabs(
                list_of_tabs,
                id="monitoring_tabs",
                active_tab=list_of_tabs[0].tab_id,
                style={
                    "color": "#000000",
                    "background-color": "#FFFFFF",
                    "text-color": "#000000",
                },
            ),
            html.Div(
                id="monitoring_page_content",
            )
        ]
    )


@callback(
    Output("monitoring_page_content", "children"),
    Input("monitoring_tabs", "active_tab"),
    Input("selected_state_dropdown", "value"),
    State("url", "pathname"),
)
def update_page_content(selected_tab, selected_state_id, pathname):
    """Update the page content according to the selected tab."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    monitoring_step = project.steps.monitoring_step

    monitoring_step.selected_state_id = selected_state_id

    if selected_tab == "project_summary_tab":
        return project_summary_view.layout(problem_setup_step, monitoring_step)
    elif selected_tab == "summary_tab":
        return summary_view.layout(problem_setup_step, monitoring_step)
    elif selected_tab == "scenery_tab":
        return scenery_view.layout(problem_setup_step)
    elif selected_tab == "design_table_tab":
        return design_table_view.layout(problem_setup_step, monitoring_step)
    elif selected_tab == "visualization_tab":
        return visualization_view.layout(problem_setup_step, monitoring_step)
    elif selected_tab == "status_overview_tab":
        return status_overview_view.layout(problem_setup_step)


@callback(
    Output("activate_auto_update", "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):
    """Enable/Disable auto update of monitoring tabs."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step

    monitoring_step.auto_update_activated = on

    raise PreventUpdate
