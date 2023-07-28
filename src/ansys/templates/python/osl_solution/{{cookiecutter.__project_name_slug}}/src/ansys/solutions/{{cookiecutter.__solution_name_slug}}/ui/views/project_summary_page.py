# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the project summary step."""

from ansys.saf.glow.client.dashclient import DashClient
from ansys.saf.glow.core.method_status import MethodStatus
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.commands import ProjectCommands
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.project_information_table import ProjectInformationTable


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the project summary view."""

    project_information_table = ProjectInformationTable(problem_setup_step.project_status_info)

    project_commands = ProjectCommands(problem_setup_step.lock_commands)

    project_information_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Project information", className="card-title"),
                    html.Div(project_information_table.render(), id="project_information_table"),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    project_commands_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Project commands", className="card-title"),
                    project_commands.render(),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(project_information_card, width=12),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(project_commands_card, width=12),
                ]
            ),
            dcc.Interval(
                id="project_summary_auto_update",
                interval=problem_setup_step.auto_update_frequency * 1000,  # in milliseconds
                n_intervals=0,
            ),
        ]
    )


@callback(
    Output("project_information_table", "children"),
    Input("project_summary_auto_update", "n_intervals"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_project_information(n_intervals, pathname):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    project_information_table = ProjectInformationTable(problem_setup_step.project_status_info)

    return project_information_table.render()


@callback(
    Output("restart_project", "n_clicks"),
    Output("stop_gently_project", "n_clicks"),
    Output("stop_project", "n_clicks"),
    Output("reset_project", "n_clicks"),
    Output("shutdown_project", "n_clicks"),
    Output("commands_alert", "dismissable"),
    Output("commands_alert", "is_open"),
    Output("restart_project", "disabled"),
    Output("stop_gently_project", "disabled"),
    Output("stop_project", "disabled"),
    Output("reset_project", "disabled"),
    Output("shutdown_project", "disabled"),
    Input("restart_project", "n_clicks"),
    Input("stop_gently_project", "n_clicks"),
    Input("stop_project", "n_clicks"),
    Input("reset_project", "n_clicks"),
    Input("shutdown_project", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def run_project_command(restart_project, stop_gently_project, stop_project, reset_project, shutdown_project, pathname):
    """Pause OptiSLang project."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    run_command = False

    if restart_project:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.project_status_info['projects'][0]['system']['uid']}_restart"
        problem_setup_step.restart()
    elif stop_gently_project:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.project_status_info['projects'][0]['system']['uid']}_stop_gently"
        problem_setup_step.stop_gently()
    elif stop_project:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.project_status_info['projects'][0]['system']['uid']}_stop"
        problem_setup_step.stop()
    elif reset_project:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.project_status_info['projects'][0]['system']['uid']}_reset"
        problem_setup_step.reset()
    elif shutdown_project:
        run_command = True
        problem_setup_step.selected_actor_command = f"{problem_setup_step.project_status_info['projects'][0]['system']['uid']}_shutdown"
        problem_setup_step.shutdown()

    if run_command:
        problem_setup_step.lock_commands = True
        print("COMMANDS LOCKED")
        return (0, 0, 0, 0, 0, False, True, True, True, True, True, True)
    else:
        raise PreventUpdate


@callback(
    Output("commands_alert", "dismissable"),
    Output("commands_alert", "children"),
    Output("commands_alert", "color"),
    Output("restart_project", "disabled"),
    Output("stop_gently_project", "disabled"),
    Output("stop_project", "disabled"),
    Output("reset_project", "disabled"),
    Output("shutdown_project", "disabled"),
    Input("project_summary_auto_update", "n_intervals"),
    State("url", "pathname"),
)
def monitor_project_command(n_intervals, pathname):
    """Pause OptiSLang project."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.selected_actor_command:
        if problem_setup_step.selected_actor_command.startswith(problem_setup_step.project_status_info['projects'][0]['system']['uid']):
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
                    False,
                )
            elif status == MethodStatus.Failed:
                problem_setup_step.lock_commands = False
                problem_setup_step.selected_actor_command = None
                return (True, f"{command.replace('_', ' ').title()} command failed.", "danger", False, False, False, False, False)
            elif status == MethodStatus.Running:
                return (False, f"{command.replace('_', ' ').title()} command is under process.", "primary", True, True, True, True, True)
    raise PreventUpdate
