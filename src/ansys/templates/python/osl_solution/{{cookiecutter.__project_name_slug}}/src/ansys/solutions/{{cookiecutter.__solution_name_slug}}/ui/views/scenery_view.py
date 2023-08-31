# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the scenery view."""

from dash_extensions.enrich import html
import optislang_dash_lib
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the scenery view."""

    if problem_setup_step.project_status_info:
        return html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        optislang_dash_lib.SceneryComponent(
                            id="input",
                            project_state=problem_setup_step.project_status_info,
                        ),
                    ]
                ),
            ]
        )
    else:
        return html.Div([])
