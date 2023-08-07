# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.summary_view import SummaryView
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the summary view."""

    summary_view = SummaryView()

    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
        summary_view.actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
    if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
        summary_view.actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

    return summary_view.render()
