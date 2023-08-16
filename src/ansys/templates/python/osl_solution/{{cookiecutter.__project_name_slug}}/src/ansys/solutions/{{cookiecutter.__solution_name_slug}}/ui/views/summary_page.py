# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

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
                dbc.Col(ActorInformationTableAIO(problem_setup_step), width=12),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(ActorCommandsAIO(problem_setup_step), width=12),
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
                            dbc.Col(SystemFilesAIO, width=12),
                        ]
                    ),
                ]
            )

    content.extend(
            [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(ActorLogsTableAIO, width=12),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(ActorStatisticsTableAIO, width=12),
                    ]
                ),
            ]
        )

    return html.Div(content)
