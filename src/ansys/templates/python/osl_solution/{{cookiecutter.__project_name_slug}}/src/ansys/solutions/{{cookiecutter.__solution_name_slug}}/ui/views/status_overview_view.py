# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the node status overview view."""

import json
import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the status overview view."""

    full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())

    if full_project_status_info:
        return html.Div(
            id="node-status-view",
            children=[
                optislang_dash_lib.Nodestatusviewcomponent(
                    id="node-status-view-component",
                    project_state=full_project_status_info,
                ),
            ],
        )
    else:
        return html.Div([])
