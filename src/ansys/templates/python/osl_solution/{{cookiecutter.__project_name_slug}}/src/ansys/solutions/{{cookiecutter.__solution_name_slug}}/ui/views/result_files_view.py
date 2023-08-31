# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the results file view."""

from dash_extensions.enrich import html
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the result files view."""

    return html.Div([])
