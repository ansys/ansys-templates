# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the node status overview view."""

import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the status overview view."""

    if monitoring_step.project_status_info:
        return html.Div(
            id="node-status-view",
            children=[
                optislang_dash_lib.Nodestatusviewcomponent(
                    id="node-status-view-component",
                    project_state=monitoring_step.project_status_info,
                ),
            ],
        )
    else:
        return html.Div([])
