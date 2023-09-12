# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import uuid

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Output, Input, State, html, dcc, callback, MATCH, callback_context

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import PROJECT_STATES


class AlertsAIO(html.Div):

    class ids:

        button = lambda aio_id: {
            'component': 'AlertsAIO',
            'subcomponent': 'button',
            'aio_id': aio_id
        }
        collapse = lambda aio_id: {
            'component': 'AlertsAIO',
            'subcomponent': 'collapse',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, aio_id: str = None):
        """AlertsAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        toggle_props = {}
        collapse_props = {}

        super().__init__([
            dbc.Button(
                "Display alerts",
                id=self.ids.button(aio_id),
                size="sm",
                style={
                    "background-color": "rgba(255, 183, 27, 1)",
                    "borderColor": "rgba(255, 183, 27, 1)",
                    "color": "rgba(0, 0, 0, 1)"
                },
                **toggle_props
            ),
            html.Br(),
            dbc.Collapse(
                id=self.ids.collapse(aio_id),
                is_open=False,
                **collapse_props
            ),
        ])

    def check_ansys_ecosystem(problem_setup_step):

        alerts = []

        for product_name, product_data in problem_setup_step.ansys_ecosystem.items():
            alerts.append(
                dbc.Alert(
                    product_data["alert_message"],
                    color=product_data["alert_color"],
                    style={
                        "display": "flex",
                        "height": "20px",
                        "text-align": "left",
                        "align-items": "center",
                    }
                )
            )

        return alerts

    def check_optislang_project_state(monitoring_step):

        # optiSLang solve alert
        if monitoring_step.project_state in PROJECT_STATES.keys():
            alert_message, alert_color = PROJECT_STATES[monitoring_step.project_state]["alert"], PROJECT_STATES[monitoring_step.project_state]["color"]
        else:
            raise ValueError(f"Unknown optiSLang state: {monitoring_step.project_state}.")

        return dbc.Alert(
            alert_message,
            color=alert_color,
            style={
                "display": "flex",
                "height": "20px",
                "text-align": "left",
                "align-items": "center",
            }
        )

    @callback(
        Output(ids.collapse(MATCH), 'children'),
        Output(ids.collapse(MATCH), "is_open"),
        Input(ids.button(MATCH), 'n_clicks'),
        State("url", "pathname"),
        State(ids.collapse(MATCH), "is_open"),
        prevent_initial_call=True,
    )
    def toggle_alert(n_clicks, pathname, is_in):

        if not n_clicks:
            # Button has never been clicked
            return None, False

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step
        monitoring_step = project.steps.monitoring_step

        alerts = []
        alerts.extend(AlertsAIO.check_ansys_ecosystem(problem_setup_step))
        alerts.append(AlertsAIO.check_optislang_project_state(monitoring_step))

        return alerts, not is_in
