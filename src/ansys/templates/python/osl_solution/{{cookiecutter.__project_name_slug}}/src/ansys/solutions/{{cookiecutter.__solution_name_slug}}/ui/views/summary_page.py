# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.core.method_status import MethodStatus
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, html, dcc, callback_context

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_information_table import ActorInformationTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_logs_table import ActorLogsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_statistics_table import ActorStatisticsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.system_files import SystemFiles
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.commands import ActorCommands


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:

    actor_information_table = ActorInformationTable()
    actor_commands = ActorCommands(problem_setup_step.lock_commands)
    system_files = SystemFiles()
    actor_log_table = ActorLogsTable()
    actor_statistics_table = ActorStatisticsTable()

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        actor_information_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
        system_files.node_name = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]["name"]
        actor_log_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
        actor_statistics_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
        actor_information_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

    actor_information_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Actor information", className="card-title"),
                    html.Div(actor_information_table.render(), id="actor_information_table"),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    actor_commands_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Actor commands", className="card-title"),
                    actor_commands.render(),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    system_files_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("System Files", className="card-title"),
                    system_files.render(),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    actor_log_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Actor Log", className="card-title"),
                    actor_log_table.render(),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    actor_statistics_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Actor Statistics", className="card-title"),
                    actor_statistics_table.render(),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    content = [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(actor_information_card, width=12),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(actor_commands_card, width=12),
            ]
        ),
    ]

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        if problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]["kind"] == "system":
            content.extend(
                [
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(system_files_card, width=12),
                        ]
                    ),
                ]
            )

    content.extend(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(actor_log_card, width=12),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(actor_statistics_card, width=12),
                ]
            ),
            dcc.Interval(
                id="summary_auto_update",
                interval=problem_setup_step.auto_update_frequency * 1000,  # in milliseconds
                n_intervals=0,
            ),
        ]
    )

    return html.Div(content)


@callback(
    Output("actor_information_table", "children"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_actor_information(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    actor_information_table = ActorInformationTable()
    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        actor_information_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
        actor_information_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

    return actor_information_table.render()


@callback(
    Output("commands_alert", "children"),
    Output("commands_alert", "color"),
    Output("restart_actor", "n_clicks"),
    Output("stop_gently_actor", "n_clicks"),
    Output("stop_actor", "n_clicks"),
    Output("reset_actor", "n_clicks"),
    Output("restart_actor", "disabled"),
    Output("stop_gently_actor", "disabled"),
    Output("stop_actor", "disabled"),
    Output("reset_actor", "disabled"),
    Input("restart_actor", "n_clicks"),
    Input("stop_gently_actor", "n_clicks"),
    Input("stop_actor", "n_clicks"),
    Input("reset_actor", "n_clicks"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def run_actor_command(restart_actor, stop_gently_actor, stop_actor, reset_actor, n_intervals, pathname):
    """Run command against actor."""

    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    # Click on button
    if triggered_id in ["restart_actor", "stop_gently_actor", "stop_actor", "reset_actor"]:
        run_command = False
        if restart_actor:
            run_command = True
            problem_setup_step.selected_command = "restart"
            problem_setup_step.restart()
        elif stop_gently_actor:
            run_command = True
            problem_setup_step.selected_command = "stop_gently"
            problem_setup_step.stop_gently()
        elif stop_actor:
            run_command = True
            problem_setup_step.selected_command = "stop"
            problem_setup_step.stop()
        elif reset_actor:
            run_command = True
            problem_setup_step.selected_command = "reset"
            problem_setup_step.reset()
        if run_command:
            problem_setup_step.lock_commands = True
            uid = problem_setup_step.selected_actor_from_treeview
            problem_setup_step.selected_actor_from_command = uid
            return (
                "",
                "light",
                0,
                0,
                0,
                0,
                True,
                True,
                True,
                True,
            )

    # Monitoring
    if triggered_id == "summary_auto_update":
        if problem_setup_step.selected_command:
            if problem_setup_step.selected_actor_from_command == problem_setup_step.selected_actor_from_treeview:
                status = problem_setup_step.get_long_running_method_state(problem_setup_step.selected_command).status
                if status == MethodStatus.Completed:
                    problem_setup_step.lock_commands = False
                    return (
                        f"{problem_setup_step.selected_command.replace('_', ' ').title()} command completed successfully.",
                        "success",
                        restart_actor,
                        stop_gently_actor,
                        stop_actor,
                        reset_actor,
                        False,
                        False,
                        False,
                        False,
                    )
                elif status == MethodStatus.Failed:
                    problem_setup_step.lock_commands = False
                    return (
                        f"{problem_setup_step.selected_command.replace('_', ' ').title()} command failed.",
                        "danger",
                        restart_actor,
                        stop_gently_actor,
                        stop_actor,
                        reset_actor,
                        False,
                        False,
                        False,
                        False,
                    )
                elif status == MethodStatus.Running:
                    return (
                        f"{problem_setup_step.selected_command.replace('_', ' ').title()} command is under process.",
                        "primary",
                        restart_actor,
                        stop_gently_actor,
                        stop_actor,
                        reset_actor,
                        True,
                        True,
                        True,
                        True,
                    )
                else:
                    raise Exception(f"Method {problem_setup_step.selected_command} should be in one of these states: Completed, Failed or Running.")


    raise PreventUpdate
