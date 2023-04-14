# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the monitoring step."""
import dash_bootstrap_components as dbc

from dash_extensions.enrich import Input, Output, callback, dcc, html
from ansys.saf.glow.client.dashclient import DashClient

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.monitoring_tabs import project_summary_page, summary_page, result_files_page, scenery_page, design_table_page, visualization_page, status_overview_page


def update_monitoring_tabs(component):
    if component == "root":
        monitoring_tabs = [ 
            dcc.Tab(label='Project Summary', value='project_summary_step'),
            dcc.Tab(label='Result Files', value='result_files_step'),
            dcc.Tab(label='Scenery', value='scenery_step'),
            dcc.Tab(label='Design Table', value='design_table_step'),
            dcc.Tab(label='Visualization', value='visualization_step'),
            dcc.Tab(label='Status Overview', value='status_overview_step')
        ]
    elif component == "system":
        monitoring_tabs = [
            dcc.Tab(label='Summary', value='summary_step'),
            dcc.Tab(label='Design Table', value='design_table_step'),
            dcc.Tab(label='Visualization', value='visualization_step'),
            dcc.Tab(label='Status Overview', value='status_overview_step'),
        ]
    elif component == "node":
        monitoring_tabs = [
            dcc.Tab(label='Summary', value='summary_step'),
            dcc.Tab(label='Status Overview', value='status_overview_step'),
        ]
    return monitoring_tabs


def layout(step: MonitoringStep):
    monitoring_tabs = update_monitoring_tabs(step.component_level)
    return html.Div(
        [
            dcc.Markdown("""#### Monitoring step""", className="display-3"),
            html.Hr(className="my-2"),
            html.Br(),
            dbc.Row(
                dcc.Tabs(id="monitoring-tabs", value='project_summary_step', 
                    children= monitoring_tabs,
                ),
            ),
            dbc.Row(
                html.Div(
                    id="monitoring-page-content",
                ),
            ),
        ]
    )


@callback(
    Output("monitoring-page-content", "children"),
    [
        Input("url", "pathname"),
        Input("monitoring-tabs", "value"),
    ],
    prevent_initial_call=True,
)
def display_monitoring_page(pathname, tab):
    """Display monitoring page content that corresponds to the tab selected."""
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)

    if tab == "project_summary_step":
        page_layout = project_summary_page.layout(project.steps.hook_optimization_step)
    elif tab == "summary_step":
        page_layout = summary_page.layout(project.steps.problem_setup_step, project.steps.monitoring_step)
    elif tab == "result_files_step":
        page_layout = result_files_page.layout(project.steps.hook_optimization_step)
    elif tab == "scenery_step":
        page_layout = scenery_page.layout(project.steps.hook_optimization_step)
    elif tab == "design_table_step":
        page_layout = design_table_page.layout(project.steps.hook_optimization_step)
    elif tab == "visualization_step":
        page_layout = visualization_page.layout(project.steps.hook_optimization_step)
    elif tab == "status_overview_step":
        page_layout = status_overview_page.layout(project.steps.hook_optimization_step)    
    return page_layout
