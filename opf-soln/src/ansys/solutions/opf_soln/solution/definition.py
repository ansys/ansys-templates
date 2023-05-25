# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Solution definition module."""


from ansys.saf.glow.solution import Solution, StepsModel

from ansys.solutions.opf_soln.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.opf_soln.solution.monitoring_step import MonitoringStep


class Steps(StepsModel):
    """Workflow definition."""
    problem_setup_step: ProblemSetupStep
    monitoring_step: MonitoringStep


class Opf_SolnSolution(Solution):
    """Solution definition."""
    display_name = "opf_soln"
    steps: Steps
