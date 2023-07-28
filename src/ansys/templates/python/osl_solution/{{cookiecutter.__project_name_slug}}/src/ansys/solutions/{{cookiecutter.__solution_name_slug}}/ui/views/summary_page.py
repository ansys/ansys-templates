# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.core.method_status import MethodStatus
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, html, dcc

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

    if problem_setup_step.selected_actor_info["uid"] in problem_setup_step.actors_info.keys():
        actor_information_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]
        system_files.node_name = problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]["name"]
        actor_log_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]
        actor_statistics_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]

    if problem_setup_step.selected_actor_info["uid"] in problem_setup_step.actors_status_info.keys():
        actor_information_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_info["uid"]][0]

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

    if problem_setup_step.selected_actor_info["uid"] in problem_setup_step.actors_info.keys():
        if problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]["kind"] == "system":
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
    if problem_setup_step.selected_actor_info["uid"] in problem_setup_step.actors_info.keys():
        actor_information_table.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_info["uid"]]
    if problem_setup_step.selected_actor_info["uid"] in problem_setup_step.actors_status_info.keys():
        actor_information_table.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_info["uid"]][0]

    return actor_information_table.render()


@callback(
    Output("restart_command", "n_clicks"),
    Output("stop_gently_command", "n_clicks"),
    Output("stop_command", "n_clicks"),
    Output("reset_command", "n_clicks"),
    Output("commands_alert", "dismissable"),
    Output("commands_alert", "is_open"),
    Output("restart_command", "disabled"),
    Output("stop_gently_command", "disabled"),
    Output("stop_command", "disabled"),
    Output("reset_command", "disabled"),
    Input("restart_command", "n_clicks"),
    Input("stop_gently_command", "n_clicks"),
    Input("stop_command", "n_clicks"),
    Input("reset_command", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def run_actor_command(restart_command, stop_gently_command, stop_command, reset_command, pathname):
    """Pause OptiSLang project."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    run_command = False

    if restart_command:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.selected_actor_info['uid']}_restart"
        problem_setup_step.restart()
    elif stop_gently_command:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.selected_actor_info['uid']}_stop_gently"
        problem_setup_step.stop_gently()
    elif stop_command:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.selected_actor_info['uid']}_stop"
        problem_setup_step.stop()
    elif reset_command:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.selected_actor_info['uid']}_reset"
        problem_setup_step.reset()

    if run_command:
        problem_setup_step.lock_commands = True
        return (0, 0, 0, 0, False, True, True, True, True, True)
    else:
        raise PreventUpdate


@callback(
    Output("commands_alert", "dismissable"),
    Output("commands_alert", "children"),
    Output("commands_alert", "color"),
    Output("restart_command", "disabled"),
    Output("stop_gently_command", "disabled"),
    Output("stop_command", "disabled"),
    Output("reset_command", "disabled"),
    Input("summary_auto_update", "n_intervals"),
    State("url", "pathname"),
)
def monitor_actor_command(n_intervals, pathname):
    """Pause OptiSLang project."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.selected_actor_command:
        if problem_setup_step.selected_actor_command.startswith(problem_setup_step.selected_actor_info['uid']):
            command = problem_setup_step.selected_actor_command.split("_")[1]
            status = problem_setup_step.get_long_running_method_state(command).status
            if status == MethodStatus.Completed:
                problem_setup_step.lock_commands = False
                problem_setup_step.selected_actor_command = None
                return (
                    True,
                    f"{command.replace('_', ' ').title()} command completed successfully.",
                    "success",
                    False,
                    False,
                    False,
                    False,
                )
            elif status == MethodStatus.Failed:
                problem_setup_step.lock_commands = False
                problem_setup_step.selected_actor_command = None
                return (True, f"{command.replace('_', ' ').title()} command failed.", "danger", False, False, False, False)
            elif status == MethodStatus.Running:
                return (False, f"{command.replace('_', ' ').title()} command is under process.", "primary", True, True, True, True)
        
    raise PreventUpdate
