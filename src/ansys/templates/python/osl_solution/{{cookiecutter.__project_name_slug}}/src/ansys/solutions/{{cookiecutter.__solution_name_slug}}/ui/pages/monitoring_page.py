# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the monitoring step."""

from ansys.saf.glow.client.dashclient import DashClient
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.logs_table import LogsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.alerts import update_monitoring_alert
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import update_list_of_tabs
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.views import (
    design_table_page,
    project_summary_page,
    result_files_page,
    scenery_page,
    status_overview_page,
    summary_page,
    visualization_page,
)


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep, node_info: dict) -> html.Div:

    list_of_tabs = update_list_of_tabs(node_info)

    return html.Div(
        [
            html.Div(
                id="monitoring_alert",
                children=update_monitoring_alert(problem_setup_step),
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
            ),
            dcc.Store(id="node_info", data=node_info),
            html.Br(),
            html.Div(
                [
                    dbc.Button(
                        "optiSLang logs",
                        id="fade_button",
                        className="mb-3",
                        n_clicks=0,
                        style={"background-color": "#000000", "borderColor": "#000000"},
                    ),
                    dbc.Fade(
                        id="fade",
                        is_in=False,
                        appear=False,
                    ),
                ]
            ),
            dcc.Interval(
                id="update_data_interval",
                interval=1 * 3000,  # in milliseconds
                n_intervals=0,
            ),
        ]
    )


@callback(
    Output("monitoring_page_content", "children"),
    Input("monitoring_tabs", "active_tab"),
    Input("update_data_interval", "n_intervals"),
    Input("url", "pathname"),
    State("node_info", "data"),
)
def update_page_content(active_tab, n_intervals, pathname, node_info):
    """Update the page content according to the selected tab."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if active_tab == "project_summary_tab":
        return project_summary_page.layout(problem_setup_step.project_status_info)
    elif active_tab == "summary_tab":
        return summary_page.layout(
            problem_setup_step.actors_info,
            problem_setup_step.actors_status_info,
            problem_setup_step.results_files,
            node_info["uid"],
        )
    elif active_tab == "result_files_tab":
        return result_files_page.layout(problem_setup_step.project_status_info, node_info["uid"])
    elif active_tab == "scenery_tab":
        return scenery_page.layout(problem_setup_step.project_status_info)
    elif active_tab == "design_table_tab":
        return design_table_page.layout(
            problem_setup_step.actors_info, problem_setup_step.actors_status_info, node_info["uid"]
        )
    elif active_tab == "visualization_tab":
        return visualization_page.layout(problem_setup_step.project_status_info, node_info["uid"])
    elif active_tab == "status_overview_tab":
        return status_overview_page.layout(problem_setup_step.project_status_info)


@callback(
    Output("fade", "children"),
    Output("fade", "is_in"),
    Input("fade_button", "n_clicks"),
    Input("url", "pathname"),
    State("fade", "is_in"),
)
def display_optislang_logs(n_clicks, pathname, is_in):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if not n_clicks:
        # Button has never been clicked
        return None, False

    table = LogsTable(problem_setup_step.optislang_logs)

    return table.render(), not is_in

