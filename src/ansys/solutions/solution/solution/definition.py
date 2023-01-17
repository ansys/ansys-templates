# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.solution.solution.first_step import FirstStep
from ansys.solutions.solution.solution.other_step import OtherStep

class Steps(StepsModel):
    """Workflow definition."""
    first_step: FirstStep
    other_step: OtherStep


class SolutionSolution(Solution):
    """Solution definition."""
    display_name = ""
    steps: Steps
