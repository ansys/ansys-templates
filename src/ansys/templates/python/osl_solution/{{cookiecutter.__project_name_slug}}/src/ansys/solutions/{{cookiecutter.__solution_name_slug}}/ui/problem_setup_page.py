# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the problem setup step."""
import time
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, callback, dcc, html
from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.solution import MethodStatus
from ansys.solutions.dash_components.table import InputRow
from ansys.solutions.optislang.frontend_components.placeholder_table import PlaceholderTable


from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def update_alerts_(problem_setup_step):
    """Update all Alerts."""

    alerts = []

    # Product version alerts
    for product_data in problem_setup_step.ansys_ecosystem.values(): 
        alerts.append(
            html.Div(
                children=[
                    dbc.Alert(
                        product_data["alert_message"],
                        color=product_data["alert_color"],
                    )
                ]  
            )
        )

    # OptiSLang solve alert
    if problem_setup_step.optislang_solve_status == "initial":
        alerts.append(
            dbc.Alert(
                "OptiSLang simulation not started.",
                color="warning",
                id="optislang_simulation_alert",
            )
        )
    elif problem_setup_step.optislang_solve_status == "in-progress":
        alerts.append(
            dbc.Alert(
                "OptiSLang simulation in progress.",
                color="warning",
                id="optislang_simulation_alert",
            )
        )
    elif problem_setup_step.optislang_solve_status == "success":
        alerts.append(
            dbc.Alert(
                "OptiSLang simulation completed successfully.",
                color="success",
                id="optislang_simulation_alert",
            )
        )
    elif problem_setup_step.optislang_solve_status == "failure":
        alerts.append(
            dbc.Alert(
                "OptiSLang simulation failed.",
                color="danger",
                id="optislang_simulation_alert"
            )
        )
    else:
        alerts.append(None)

    return alerts


def update_alerts(problem_setup_step):
    """Update all Alerts."""

    alerts = []

    # Product version alerts
    for product_name, product_data in problem_setup_step.ansys_ecosystem.items(): 
        alerts.append(
            html.Div(
                [
                    dbc.Button(
                        f"{product_name.title()} Version",
                        id=f"popover-{product_name}-version-target",
                        disabled = False,
                        color=product_data["alert_color"],
                        n_clicks=0,
                    ),
                    dbc.Popover(
                        [
                            dbc.PopoverBody(product_data["alert_message"]),
                        ],
                        id=f"popover-{product_name}-version",
                        target=f"popover-{product_name}-version-target",
                        placement="top",
                        is_open=False,
                    ),
                ]
            ),
        )

    # OptiSLang solve alert
    if problem_setup_step.optislang_solve_status == "initial":
        solve_message, solve_color = "OptiSLang simulation not started.", "warning"
    elif problem_setup_step.optislang_solve_status == "in-progress":
        solve_message, solve_color = "OptiSLang simulation in progress.", "primary"
    elif problem_setup_step.optislang_solve_status == "success":
        solve_message, solve_color = "OptiSLang simulation completed successfully.", "success"
    elif problem_setup_step.optislang_solve_status == "failure":
        solve_message, solve_color = "OptiSLang simulation failed.", "danger"

    alerts.append(
        html.Div(
            [
                dbc.Button(
                    "OptiSLang Solve",
                    id="popover-optislang-solve-target",
                    disabled = False,
                    color=solve_color,
                    n_clicks=0,
                ),
                dbc.Popover(
                    [
                        dbc.PopoverBody(solve_message),
                    ],
                    id="popover-optislang-solve",
                    target="popover-optislang-solve-target",
                    placement="top",
                    is_open=False,
                ),
            ]
        ),
    )

    return alerts

def layout(problem_setup_step: ProblemSetupStep):
    """Layout of the problem setup step UI."""

    # Check Ansys ecosystem
    if not problem_setup_step.ansys_ecosystem_checked:
        problem_setup_step.check_ansys_ecosystem()

    # Update alert messages
    alerts = update_alerts(problem_setup_step)

    # Upload placeholders and assets to project directory
    if problem_setup_step.placeholder_values == {}:
        problem_setup_step.upload_project_file_to_project_directory()
        problem_setup_step.upload_properties_file_to_project_directory()
        problem_setup_step.get_default_placeholder_values()
    
    placeholder_table = PlaceholderTable(problem_setup_step.placeholder_values, problem_setup_step.placeholder_definitions)

    # Placeholder card for displaying parameters defined in the <project_name>.json
    placeholder_card = dbc.Card(
        [
            dbc.CardBody(
                [
                dbc.Accordion(
                    [   
                        dbc.AccordionItem(
                            [
                                html.Div(placeholder_table.create()),
                            ],
                            
                            title="Placeholders",
                            item_id="parameter-placeholders",
                        )
                    ]
                )
            ]
            )
        ]            
    )
    return html.Div(
        [   
            html.H1("Insert OptiSLang Project Name Here", className="display-3", style={"font-size": "35px"}),
            html.Hr(className="my-2"),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Stack(
                                alerts,
                                direction = "horizontal",
                                gap = 3,
                            ),
                        ],
                        width=12,
                    )
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    # dbc.Row(image_card), 
                    dbc.Row(placeholder_card),
                ],
                style={"padding": "20px"},
            ),
            dbc.Row(
                [
                    dbc.Accordion(
                        [   
                            dbc.AccordionItem(
                                [
                                    InputRow(
                                        "input",
                                        "project_name_input",
                                        "Project settings",
                                        row_default_value=None,
                                        row_description="Enter a project name.",
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                    ).get(),
                                    html.Br(),
                                    InputRow(
                                        "button",
                                        "start_analysis",
                                        "Start analysis",
                                        disabled=False,
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                        class_name="button",
                                    ).get(),
                                    dcc.Loading(
                                        id="optislang_wait_spinner",
                                        type="circle",
                                        fullscreen=True,
                                        color="#ffb71b",
                                        style={
                                            "background-color": "rgba(55, 58, 54, 0.1)",
                                        },
                                        children=html.Div(id="wait_optislang_process"),
                                    ),
                                    dcc.Interval(
                                        id="solve-interval-component",
                                        interval=1 * 6000,  # in milliseconds
                                        n_intervals=0,
                                    ),
                                ],
                                title="Start Analysis",
                                item_id="start-analysis-accordion",
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


for alert in ["optislang-version", "workbench-version", "optislang-solve"]:
    @callback(
        Output(f"popover-{alert}", "is_open"),
        [Input(f"popover-{alert}-target", "n_clicks")],
        [State(f"popover-{alert}", "is_open")],
    )
    def toggle_popover(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open


@callback(
    Output("wait_optislang_process", "children"),
    # Output("optislang_simulation_alert", "children"),
    Input("start_analysis", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def run_optislang_synchronously(n_clicks, pathname):
    """Start OptiSLang and run the simulation. Wait for the process to complete."""
    
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    if n_clicks and problem_setup_step.run_synchronously:
        problem_setup_step.run_optislang()
        while (
            problem_setup_step.get_long_running_method_state("run_optislang").status == MethodStatus.Running
        ):
            time.sleep(2)
        if problem_setup_step.optislang_solve_status == "success":
            return (
                dbc.Alert(
                    "OptiSLang simulation completed successfully.",
                    color="success",
                ),
                True
            )
        elif problem_setup_step.optislang_solve_status == "failure":
            return (
                dbc.Alert(
                    "OptiSLang simulation failed.",
                    color="danger",
                ),
                True
            )
        else:
            return (
                dbc.Alert(
                    "OptiSLang simulation failed with an unknown error.",
                    color="danger",
                ),
                True
            )
    else:
        raise PreventUpdate
