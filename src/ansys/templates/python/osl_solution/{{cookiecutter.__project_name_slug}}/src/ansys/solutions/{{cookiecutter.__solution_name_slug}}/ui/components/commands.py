# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Output, Input, State, html, dcc, callback, MATCH, callback_context
import uuid

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}


class ProjectCommandsAIO(html.Div):

    class ids:
        interval = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'interval',
            'aio_id': aio_id
        }
        restart_button = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'restart_button',
            'aio_id': aio_id
        }
        stop_gently_button = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'stop_gently_button',
            'aio_id': aio_id
        }
        stop_button = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'stop_button',
            'aio_id': aio_id
        }
        reset_button = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'reset_button',
            'aio_id': aio_id
        }
        shutdown_button = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'shutdown_button',
            'aio_id': aio_id
        }
        alert = lambda aio_id: {
            'component': 'ProjectCommandsAIO',
            'subcomponent': 'alert',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, aio_id: str = None):
        """ProjectCommandsAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        interval_props = {
            "interval": 3000,
            "n_intervals": 0,
            "disabled": not problem_setup_step.commands_locked
        }

        button_props = {
            "disabled": problem_setup_step.commands_locked,
            "style": {
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "fontSize": "150%",
                "color": "rgba(0, 0, 0, 1)",
                "background-color": "rgba(255, 255, 255, 1)",
                "border-color": "rgba(0, 0, 0, 1)",
                "height": "40px",
                "width": "70px",
            }
        }

        alert_props = {
            "children": "",
            "color": "light",
            "dismissable": False,
            "is_open": True,
            "fade": False,
            "style": {
                "width": "600px",
                "height": "40px",
                "display": "flex",
                "justify-content": "left",
                "align-items": "center",
            },
        }

        super().__init__([
            dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Project commands", className="card-title"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Stack(
                                            [
                                                dbc.Button(
                                                    children=html.I(className="fas fa-play", style={"display": "inline-block"}),
                                                    id=self.ids.restart_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Restart optiSLang project.",
                                                    target=self.ids.restart_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fa fa-hand-paper", style={"display": "inline-block"}),
                                                    id=self.ids.stop_gently_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Stop optiSLang project gently.",
                                                    target=self.ids.stop_gently_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fas fa-stop", style={"display": "inline-block"}),
                                                    id=self.ids.stop_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Stop optiSLang project.",
                                                    target=self.ids.stop_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fas fa-fast-backward", style={"display": "inline-block"}),
                                                    id=self.ids.reset_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Reset optiSLang project.",
                                                    target=self.ids.reset_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fas fa-power-off", style={"display": "inline-block"}),
                                                    id=self.ids.shutdown_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Shutdown optiSLang project.",
                                                    target=self.ids.shutdown_button(aio_id),
                                                    placement="bottom"
                                                ),
                                            ],
                                            direction="horizontal",
                                            gap=1,
                                        ),
                                        width="auto",
                                    ),
                                    dbc.Col(
                                        dbc.Alert(id=self.ids.alert(aio_id), **alert_props),
                                        width="auto",
                                    ),
                                ]
                            )

                        ]
                    ),
                ],
                color="warning",
                outline=True,
            )
        ])

    @callback(
        Output(ids.restart_button(MATCH), 'disabled'),
        Input(ids.restart_button(MATCH), 'n_clicks'),
        Input(ids.stop_gently_button(MATCH), 'n_clicks'),
        Input(ids.stop_button(MATCH), 'n_clicks'),
        Input(ids.reset_button(MATCH), 'n_clicks'),
        Input(ids.shutdown_button(MATCH), 'n_clicks'),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def run_command(restart, stop_gently, stop, reset, shutdown, pathname):

        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step

        if "restart_button" in triggered_id:
            problem_setup_step.restart()
        elif "stop_gently_button" in triggered_id:
            problem_setup_step.stop_gently()
        elif "stop_button" in triggered_id:
            problem_setup_step.stop()
        elif "reset_button" in triggered_id:
            problem_setup_step.reset()
        elif "shutdown_button" in triggered_id:
            problem_setup_step.shutdown()

        return False


class ActorCommandsAIO(html.Div):

    class ids:
        interval = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'interval',
            'aio_id': aio_id
        }
        restart_button = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'restart_button',
            'aio_id': aio_id
        }
        stop_gently_button = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'stop_gently_button',
            'aio_id': aio_id
        }
        stop_button = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'stop_button',
            'aio_id': aio_id
        }
        reset_button = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'reset_button',
            'aio_id': aio_id
        }
        alert = lambda aio_id: {
            'component': 'ActorCommandsAIO',
            'subcomponent': 'alert',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, aio_id: str = None):
        """ActorCommandsAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        interval_props = {
            "interval": 3000,
            "n_intervals": 0,
            "disabled": not problem_setup_step.commands_locked
        }

        button_props = {
            "disabled": problem_setup_step.commands_locked,
            "style": {
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "fontSize": "150%",
                "color": "rgba(0, 0, 0, 1)",
                "background-color": "rgba(255, 255, 255, 1)",
                "border-color": "rgba(0, 0, 0, 1)",
                "height": "40px",
                "width": "70px",
            }
        }

        alert_props = {
            "children": "",
            "color": "light",
            "dismissable": False,
            "is_open": True,
            "fade": False,
            "style": {
                "width": "600px",
                "height": "40px",
                "display": "flex",
                "justify-content": "left",
                "align-items": "center",
            },
        }

        super().__init__([
            dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Actor commands", className="card-title"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Stack(
                                            [
                                                dbc.Button(
                                                    children=html.I(className="fas fa-play", style={"display": "inline-block"}),
                                                    id=self.ids.restart_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Restart node.",
                                                    target=self.ids.restart_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fa fa-hand-paper", style={"display": "inline-block"}),
                                                    id=self.ids.stop_gently_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Stop node gently.",
                                                    target=self.ids.stop_gently_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fas fa-stop", style={"display": "inline-block"}),
                                                    id=self.ids.stop_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Stop node.",
                                                    target=self.ids.stop_button(aio_id),
                                                    placement="bottom"
                                                ),
                                                dbc.Button(
                                                    children=html.I(className="fas fa-fast-backward", style={"display": "inline-block"}),
                                                    id=self.ids.reset_button(aio_id),
                                                    **button_props
                                                ),
                                                dbc.Tooltip(
                                                    "Reset node.",
                                                    target=self.ids.reset_button(aio_id),
                                                    placement="bottom"
                                                ),
                                            ],
                                            direction="horizontal",
                                            gap=1,
                                        ),
                                        width="auto",
                                    ),
                                    dbc.Col(
                                        dbc.Alert(id=self.ids.alert(aio_id), **alert_props),
                                        width="auto",
                                    ),
                                ]
                            )

                        ]
                    ),
                ],
                color="warning",
                outline=True,
            )
        ])

    @callback(
        Output(ids.restart_button(MATCH), 'disabled'),
        Input(ids.restart_button(MATCH), 'n_clicks'),
        Input(ids.stop_gently_button(MATCH), 'n_clicks'),
        Input(ids.stop_button(MATCH), 'n_clicks'),
        Input(ids.reset_button(MATCH), 'n_clicks'),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def run_command(restart, stop_gently, stop, reset, pathname):

        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step

        if "restart_button" in triggered_id:
            problem_setup_step.restart()
        elif "stop_gently_button" in triggered_id:
            problem_setup_step.stop_gently()
        elif "stop_button" in triggered_id:
            problem_setup_step.stop()
        elif "reset_button" in triggered_id:
            problem_setup_step.reset()

        return False
