# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import json
import dash_bootstrap_components as dbc
import uuid

from dash_extensions.enrich import Output, Input, State, html, callback, MATCH, callback_context, ALL
from dash.exceptions import PreventUpdate

from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.core.method_status import MethodStatus

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.button_group import ButtonGroup

class NodeControlAIO(html.Div):

    class ids:
        button_group = lambda aio_id: {
            'component': 'NodeControlAIO',
            'subcomponent': 'btn_group',
            'aio_id': aio_id
        }
        alert = lambda aio_id: {
            'component': 'NodeControlAIO',
            'subcomponent': 'alert',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, button_group, alert_props, aio_id: str = None):
        """NodeControlAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dbc.Stack` and a `dbc.Alert` as children.

        - `button_group` - The container of buttons used to build the project commands.
        - `alert_props` - The dictionary of properties for the alert component.
        - `aio_id` - The All-in-One component ID used to generate the components dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__([
            html.H5("Commands", className="card-title"),
            html.Hr(className="my-2"),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Stack(
                                            id=self.ids.button_group(aio_id),
                                            children=button_group,
                                            direction="horizontal",
                                            gap=1,
                                        ),
                                        width="auto",
                                    ),
                                    dbc.Col(
                                        children=[
                                            dbc.Alert(
                                                id=self.ids.alert(aio_id),
                                                dismissable=True,
                                                fade= True,
                                                style= {"width": "600px", "height": "40px", "display": "flex", "justify-content": "left", "align-items": "center"},
                                                **alert_props,
                                            ),
                                        ],
                                        width="auto",
                                    ),
                                    html.Div(id="action-requested", style={"display": "none"}, children=False),
                                ],
                            ),
                        ],
                        className="border-0 bg-transparent"
                    ),
                ],
                className="border-0 bg-transparent"
            )
        ])

    @callback(
        Output(ids.alert(MATCH), "children"),
        Output(ids.alert(MATCH), "color"),
        Output(ids.alert(MATCH), "is_open"),
        Output(ids.button_group(MATCH), "children"),
        Input("action-requested", "children"),
        State("url", "pathname"),
        prevent_initial_call=True
    )
    def run_command(action_requested, pathname):
        """This performs actions such as stopping, restarting, and shutting down on an instance of optiSlang when action is requested. A message with the status of the method execution and states of each button is updated on completion of the method."""
        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        monitoring_step = project.steps.monitoring_step
        monitoring_step.selected_actor_from_command = monitoring_step.selected_actor_from_treeview
        ctx = callback_context
        if (ctx.triggered and action_requested):
            alert_status = {"alert-message": "", "alert-color": ""}
            try:
                monitoring_step.control_node_state()
                command_execution_state = monitoring_step.get_method_state("control_node_state").status
                if command_execution_state == MethodStatus.Completed:
                    alert_status["alert-message"] =  f"{monitoring_step.selected_command.replace('_', ' ').title()} command completed successfully.",
                    alert_status["alert-color"] = "success"
            except Exception as e:
                alert_status["alert-message"] = f"{monitoring_step.selected_command.replace('_', ' ').title()} command failed. For details, review the logs.",
                alert_status["alert-color"] = "warning"
        else:
            raise PreventUpdate
        if monitoring_step.actor_uid:
            monitoring_step.actor_command_execution_status = alert_status
            monitoring_step.project_command_execution_status = {"alert-message": "", "alert-color": ""}
            btn_group_options = monitoring_step.actor_btn_group_options
        else:
            monitoring_step.project_command_execution_status = alert_status
            monitoring_step.actor_command_execution_status = {"alert-message": "", "alert-color": ""}
            btn_group_options = monitoring_step.project_btn_group_options
        monitoring_step.commands_locked = False
        return alert_status["alert-message"], alert_status["alert-color"], bool(alert_status["alert-message"]), ButtonGroup(options=btn_group_options, disabled=monitoring_step.commands_locked).buttons

    @callback(
        Output("action-requested", "children"),
        Output({"type": "action-button", "action": ALL}, 'disabled'),
        Input({"type": "action-button", "action": ALL}, 'n_clicks'),
        State({"type": "action-button", "action": ALL}, 'disabled'),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def set_selected_command_and_disable_buttons(n_clicks_actions, button_states, pathname):
        """This disables all project and actor command buttons on click of a button and sends and returns a bool for action requested."""
        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        monitoring_step = project.steps.monitoring_step
        monitoring_step.selected_actor_from_command = monitoring_step.selected_actor_from_treeview
        ctx = callback_context
        if (
            ctx.triggered
            and not all(n_click is None for n_click in n_clicks_actions)
        ):
            triggered_button = callback_context.triggered[0]["prop_id"].split(".")[0]
            action = json.loads(triggered_button)["action"]
            monitoring_step.selected_command = action
            disable_buttons = [True] * len(button_states)
            monitoring_step.commands_locked = True
        else:
            raise PreventUpdate
        return True, disable_buttons
