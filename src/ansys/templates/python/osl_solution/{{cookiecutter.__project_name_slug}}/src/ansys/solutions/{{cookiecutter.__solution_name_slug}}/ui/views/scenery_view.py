# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the scenery view."""

import json
import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the scenery view."""

    project_status_info = json.loads(monitoring_step.project_status_info_file.read_text())

    if project_status_info:
        return html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        optislang_dash_lib.SceneryComponent(
                            id="input",
                            project_state=project_status_info,
                        ),
                    ]
                ),
            ]
        )
    else:
        return html.Div([])
