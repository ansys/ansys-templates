# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Solution definition module."""


from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.solution.solution.first_step import FirstStep
from ansys.solutions.solution.solution.second_step import SecondStep


class Steps(StepsModel):
    """Workflow definition."""

    first_step: FirstStep
    second_step: SecondStep


class SolutionSolution(Solution):
    """Solution definition."""

    display_name: str = "My Solution"
    steps: Steps
