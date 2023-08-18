# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the visualization view."""

from dash_extensions.enrich import html
import optislang_dash_lib
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep



def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the visualization view."""

    return html.Div(
        [
            optislang_dash_lib.VisualizationComponent(
                id="visualization-component",
                project_state=problem_setup_step.project_status_info,
                system_id=problem_setup_step.selected_actor_from_treeview,
                state_idx=0,
            ),
        ]
    )
