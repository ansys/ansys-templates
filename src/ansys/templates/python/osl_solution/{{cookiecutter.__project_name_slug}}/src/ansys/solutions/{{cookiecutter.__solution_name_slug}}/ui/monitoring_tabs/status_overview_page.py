# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the node status overview tab."""

from dash_extensions.enrich import html
import optislang_dash_lib

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the node status overview tab."""

    monitoring_step.get_project_state() # fetches data on page load

    return html.Div(
        id="node-status-view",
        children=[
            optislang_dash_lib.Nodestatusviewcomponent(
                id="node-status-view-component",
                project_state=monitoring_step.project_state,
            ),
        ],
    )