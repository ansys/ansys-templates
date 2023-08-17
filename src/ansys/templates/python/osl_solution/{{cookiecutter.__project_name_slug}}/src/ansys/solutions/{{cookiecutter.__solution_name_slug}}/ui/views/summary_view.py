# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, Input, Output, State

from ansys.saf.glow.client.dashclient import callback

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_information_table import ActorInformationTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.commands import ActorCommandsAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.system_files import SystemFilesAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_logs_table import ActorLogsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_statistics_table import ActorStatisticsTableAIO
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import extract_dict_by_key


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the summary view."""

    actor_info = extract_dict_by_key(problem_setup_step.step_list, "uid", problem_setup_step.selected_actor_from_treeview, expect_unique=True, return_index=False)

    content = [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(ActorInformationTableAIO(problem_setup_step, aio_id="actor_information_table"), width=12),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(ActorCommandsAIO(problem_setup_step, aio_id="actor_commands"), width=12),
            ]
        ),
    ]

    if actor_info:
        if actor_info["kind"] == "system":
            content.extend(
                [
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(SystemFilesAIO(problem_setup_step, aio_id="system_files"), width=12),
                        ]
                    ),
                ]
            )

    content.extend(
            [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(ActorLogsTableAIO(problem_setup_step, aio_id="actor_logs_table"), width=12),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(ActorStatisticsTableAIO(problem_setup_step, aio_id="actor_statistics_table"), width=12),
                    ]
                ),
            ]
        )

    return html.Div(content)


@callback(
    Output({'component': 'ActorInformationTableAIO', 'subcomponent': 'interval', 'aio_id': 'actor_information_table'}, "disabled"),
    Output({'component': 'ActorLogsTableAIO', 'subcomponent': 'interval', 'aio_id': 'actor_logs_table'}, "disabled"),
    Output({'component': 'ActorStatisticsTableAIO', 'subcomponent': 'interval', 'aio_id': 'actor_statistics_table'}, "disabled"),
    Input("activate_auto_update", "on"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def activate_auto_update(on, pathname):

    return not on, not on, not on
