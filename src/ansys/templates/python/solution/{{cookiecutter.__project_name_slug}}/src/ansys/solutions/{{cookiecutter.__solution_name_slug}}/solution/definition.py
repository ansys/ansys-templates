# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Solution definition module."""


from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.second_step import SecondStep


class Steps(StepsModel):
    """Workflow definition."""

    first_step: FirstStep
    second_step: SecondStep


class {{ cookiecutter.__solution_definition_name }}(Solution):
    """Solution definition."""

    display_name: str = "{{ cookiecutter.__solution_display_name.replace('"', '') }}"
    version: int = 1
    steps: Steps
