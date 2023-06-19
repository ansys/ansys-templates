# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Solution definition module."""


from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.my_osl_solution.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.my_osl_solution.solution.monitoring_step import MonitoringStep


class Steps(StepsModel):
    """Workflow definition."""
    problem_setup_step: ProblemSetupStep
    monitoring_step: MonitoringStep


class My_Osl_SolutionSolution(Solution):
    """Solution definition."""
    display_name = "My optiSLang Solution"
    steps: Steps
