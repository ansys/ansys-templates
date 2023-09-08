# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Solution definition module."""

from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


class Steps(StepsModel):
    """Workflow definition."""
    problem_setup_step: ProblemSetupStep
    monitoring_step: MonitoringStep


class {{ cookiecutter.__solution_definition_name }}(Solution):
    """Solution definition."""
    display_name : str = "{{ cookiecutter.__solution_display_name.replace('"', '') }}"
    steps: Steps
