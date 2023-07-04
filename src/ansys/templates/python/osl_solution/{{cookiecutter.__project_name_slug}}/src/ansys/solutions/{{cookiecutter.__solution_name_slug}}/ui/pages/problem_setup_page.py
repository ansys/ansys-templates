# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the problem setup step."""

import time

from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.solution import MethodStatus
from ansys.solutions.dash_components.table import InputRow
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, dcc, html
from ansys.solutions.optislang.frontend_components.load_sections import to_dash_sections

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.alerts import update_alerts
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.placeholders import update_placeholders


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the problem setup step."""

    # Upload placeholders and assets
    if problem_setup_step.placeholders == {}:
        problem_setup_step.get_default_placeholder_values()
        problem_setup_step.ui_placeholders = problem_setup_step.placeholders

    project_properties_sections = to_dash_sections(problem_setup_step.placeholders, problem_setup_step.registered_files)

    return html.Div(
        [
            # Header
            html.H1(
                problem_setup_step.app_metadata["title"].strip().title(),
                className="display-3",
                style={"font-size": "45px"},
            ),
            html.P(
                problem_setup_step.app_metadata["description"].strip(),
                className="lead",
                style={"font-size": "25px"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
            # Alerts
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Stack(
                                update_alerts(problem_setup_step),
                                id="alert_messages",
                                direction="horizontal",
                                gap=3,
                            ),
                        ],
                        width=12,
                    )
                ]
            ),
            html.Br(),
            # Input form
            dbc.Row(project_properties_sections),
            dbc.Row(
                [
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    # InputRow(
                                    #     "button",
                                    #     "check_ansys_ecosystem",
                                    #     "Check Ansys ecosystem",
                                    #     disabled=False,
                                    #     label_width=2,
                                    #     value_width=4,
                                    #     unit_width=1,
                                    #     description_width=4,
                                    #     class_name="button",
                                    # ).get(),
                                    # dcc.Loading(
                                    #     type="circle",
                                    #     fullscreen=True,
                                    #     color="#ffb71b",
                                    #     style={
                                    #         "background-color": "rgba(55, 58, 54, 0.1)",
                                    #     },
                                    #     children=html.Div(id="wait_ecosystem_ckeck"),
                                    # ),
                                    # html.Br(),
                                    InputRow(
                                        "button",
                                        "start_analysis",
                                        "Start analysis",
                                        disabled=True
                                        if problem_setup_step.analysis_running
                                        or not problem_setup_step.ansys_ecosystem_ready
                                        else False,
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                        class_name="button",
                                    ).get(),
                                    dcc.Loading(
                                        type="circle",
                                        fullscreen=True,
                                        color="#ffb71b",
                                        style={
                                            "background-color": "rgba(55, 58, 54, 0.1)",
                                        },
                                        children=html.Div(id="wait_start_analysis"),
                                    ),
                                    dcc.Interval(
                                        id="solve_interval_component",
                                        interval=1 * 3000,  # in milliseconds
                                        n_intervals=0,
                                    ),
                                ],
                                title="Start Analysis",
                                item_id="start_analysis_accordion",
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


for alert in ["optislang_version", "optislang_solve"]:

    @callback(
        Output(f"popover_{alert}", "is_open"),
        [Input(f"popover_{alert}_target", "n_clicks")],
        [State(f"popover_{alert}", "is_open")],
    )
    def toggle_popover(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open


# @callback(
#     Output("alert_messages", "children"),
#     Output("wait_ecosystem_ckeck", "children"),
#     Output("start_analysis", "disabled"),
#     Input("check_ansys_ecosystem", "n_clicks"),
#     State("url", "pathname"),
#     prevent_initial_call=True,
# )
# def check_ansys_ecosystem(n_clicks, pathname):
#     """Start optiSLang and run the simulation. Wait for the process to complete."""

#     project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
#     problem_setup_step = project.steps.problem_setup_step

#     if n_clicks:
#         problem_setup_step.check_ansys_ecosystem()
#         return update_alerts(problem_setup_step), True, False if problem_setup_step.ansys_ecosystem_ready else True
#     else:
#         raise PreventUpdate


@callback(
    Output("alert_messages", "children"),
    Output("wait_start_analysis", "children"),
    Output("start_analysis", "disabled"),
    Input("start_analysis", "n_clicks"),
    [State("table-placeholders", "children")],
    State("url", "pathname"),
    prevent_initial_call=True,
)
def start_analysis(n_clicks, table_children, pathname):
    """Start optiSLang and run the simulation. Wait for the process to complete."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if n_clicks:
        # Update project properties file prior to the solve
        problem_setup_step.ui_placeholders = update_placeholders(table_children, problem_setup_step.placeholders)
        problem_setup_step.write_updated_properties_file()
        # Start analysis
        problem_setup_step.start_analysis()
        # Lock start analysis
        problem_setup_step.analysis_running = True
        # Wait until the analysis effectively starts
        while problem_setup_step.optislang_solve_status == "initial":
            time.sleep(1)
        return update_alerts(problem_setup_step), True, True
    else:
        raise PreventUpdate


@callback(
    Output("alert_messages", "children"),
    Output("start_analysis", "disabled"),
    Input("solve_interval_component", "n_intervals"),
    Input("start_analysis", "n_clicks"),
    State("url", "pathname"),
)
def update_alert_messages(n_intervals, n_clicks, pathname):
    """Display status badges."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.ansys_ecosystem_ready:
        status = problem_setup_step.get_long_running_method_state("start_analysis").status
        if status != MethodStatus.Running:
            problem_setup_step.analysis_running = False
        return update_alerts(problem_setup_step), problem_setup_step.analysis_running
    else:
        raise PreventUpdate
