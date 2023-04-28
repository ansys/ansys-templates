# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

import dash_bootstrap_components as dbc

from ansys.saf.glow.client.dashclient import DashClient
from dash_extensions.enrich import Input, Output, State, callback, dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.monitoring_tabs import (
    design_table_page,
    project_summary_page,
    result_files_page,
    scenery_page,
    status_overview_page,
    summary_page,
    visualization_page,
)


def layout(monitoring_step: MonitoringStep, problem_setup_step: ProblemSetupStep):

    if not len(monitoring_step.available_root_nodes) and problem_setup_step.optislang_solve_status != "initial":
        monitoring_step.get_system_hierarchy()

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.Div(
                                        [
                                            html.Div(html.H5(children="""Root""")),
                                            dcc.Dropdown(
                                                monitoring_step.available_root_nodes,
                                                None,
                                                id="root_level",
                                                multi=False,
                                                clearable=True,
                                                disabled=False,
                                            ),
                                            dcc.Loading(
                                                type="circle",
                                                fullscreen=True,
                                                color="#ffb71b",
                                                style={
                                                    "background-color": "rgba(55, 58, 54, 0.1)",
                                                },
                                                children=html.Div(id="wait_system_update"),
                                            ),
                                        ],
                                        style={"width": "20%", "display": "inline-block"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(html.H5(children="""System""")),
                                            dcc.Dropdown(
                                                id="system_level",
                                                multi=False,
                                                clearable=True,
                                                disabled=False,
                                            ),
                                            dcc.Loading(
                                                type="circle",
                                                fullscreen=True,
                                                color="#ffb71b",
                                                style={
                                                    "background-color": "rgba(55, 58, 54, 0.1)",
                                                },
                                                children=html.Div(id="wait_subsystem_update"),
                                            ),
                                        ],
                                        style={"width": "20%", "display": "inline-block"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(html.H5(children="""Sub-System""")),
                                            dcc.Dropdown(
                                                id="subsystem_level",
                                                multi=False,
                                                clearable=True,
                                                disabled=False,
                                            ),
                                        ],
                                        style={"width": "20%", "display": "inline-block"},
                                    ),
                                ],
                                title="Node selection",
                                item_id="node-selection-accordion-item",
                            ),
                            dbc.AccordionItem(
                                [
                                    dbc.Tabs(
                                        id="monitoring_tabs",
                                        active_tab="summary_tab",
                                        style={
                                            "color": "#000000",
                                            "background-color": "#FFFFFF",
                                            "text-color": "#000000",
                                        },
                                    ),
                                    html.Div(
                                        id="monitoring_page_content",
                                    ),
                                    dcc.Loading(
                                        type="circle",
                                        fullscreen=True,
                                        color="#ffb71b",
                                        style={
                                            "background-color": "rgba(55, 58, 54, 0.1)",
                                        },
                                        children=html.Div(id="wait_page_content_update"),
                                    ),
                                ],
                                title="Monitoring",
                                item_id="monitoring-accordion-item",
                            ),
                        ],
                        id="monitoring-accordion",
                        active_item=[
                            "node-selection-accordion-item",
                            "monitoring-accordion-item",
                        ],
                        always_open=True,
                    )
                ],
            ),
        ]
    )


@callback(
    Output("system_level", "options"),
    Output("wait_system_update", "children"),
    Input("root_level", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_system_dropdown(root_node_name, pathname):
    """"""

    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step
    monitoring_step.selected_root_node = root_node_name
    return monitoring_step.available_system_nodes[root_node_name], True


@callback(
    Output("subsystem_level", "options"),
    Output("wait_subsystem_update", "children"),
    Input("system_level", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_subsystem_dropdown(system_node_name, pathname):
    """"""

    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step
    monitoring_step.selected_system_node = system_node_name
    return monitoring_step.available_subsystem_nodes[system_node_name], True


@callback(
    Output("monitoring_tabs", "children"),
    Input("root_level", "value"),
    Input("system_level", "value"),
    Input("subsystem_level", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_tabs(root_node_name, system_node_name, subsystem_node_name, pathname):
    """"""

    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step

    monitoring_step.selected_root_node = root_node_name
    monitoring_step.selected_system_node = system_node_name
    monitoring_step.selected_subsystem_node = subsystem_node_name

    monitoring_step.get_node_kind()

    if monitoring_step.selected_node_kind == "root":
        return [
            dbc.Tab(
                label="Project Summary",
                tab_id="project_summary_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Result Files",
                tab_id="result_files_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Scenery",
                tab_id="scenery_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Design Table",
                tab_id="design_table_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Status Overview",
                tab_id="status_overview_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
        ]
    elif monitoring_step.selected_node_kind == "system":
        return [
            dbc.Tab(
                label="Summary",
                tab_id="summary_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Design Table",
                tab_id="design_table_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Visualization",
                tab_id="visualization_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Status Overview",
                tab_id="status_overview_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
        ]
    elif monitoring_step.selected_node_kind == "actor":
        return [
            dbc.Tab(
                label="Summary",
                tab_id="summary_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
            dbc.Tab(
                label="Status Overview",
                tab_id="status_overview_tab",
                label_style={
                    "color": "#000000",
                    "text-color": "#000000",
                },
                active_label_style={
                    "color": "#FFFFFF",
                    "text-color": "#000000",
                    "background-color": "#000000",
                    "border-style": "solid",
                    "border-color": "#000000",
                },
            ),
        ]


@callback(
    Output("monitoring_page_content", "children"),
    Output("wait_page_content_update", "children"),
    Input("monitoring_tabs", "active_tab"),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def display_monitoring_page(active_tab, pathname):
    """Display monitoring page content that corresponds to the tab selected."""

    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)

    if active_tab == "project_summary_tab":
        return project_summary_page.layout(project.steps.monitoring_step), True
    elif active_tab == "summary_tab":
        return summary_page.layout(project.steps.monitoring_step), True
    elif active_tab == "result_files_tab":
        return result_files_page.layout(project.steps.monitoring_step), True
    elif active_tab == "scenery_tab":
        return scenery_page.layout(project.steps.monitoring_step), True
    elif active_tab == "design_table_tab":
        return design_table_page.layout(project.steps.monitoring_step), True
    elif active_tab == "visualization_tab":
        return visualization_page.layout(project.steps.monitoring_step), True
    elif active_tab == "status_overview_tab":
        return status_overview_page.layout(project.steps.monitoring_step), True
