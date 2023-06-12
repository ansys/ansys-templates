# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the visualization tab."""

from dash_extensions.enrich import html
import optislang_dash_lib

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the visualization tab UI."""

    monitoring_step.get_project_state()

    return html.Div(
        [
            optislang_dash_lib.VisualizationComponent(
                id="visualization-component",
                project_state=monitoring_step.project_state,
                system_id=monitoring_step.system_uid,
                state_idx=0,
            ),
        ]
    )
