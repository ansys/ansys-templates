# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the scenery view."""

import json
import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the scenery view."""

    full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())

    if full_project_status_info:
        return html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        optislang_dash_lib.SceneryComponent(
                            id="input",
                            project_state=full_project_status_info,
                        ),
                    ]
                ),
            ]
        )
    else:
        return html.Div([])
