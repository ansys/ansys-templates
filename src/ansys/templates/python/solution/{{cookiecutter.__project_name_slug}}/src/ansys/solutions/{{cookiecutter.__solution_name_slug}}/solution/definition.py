# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.saf.glow.solution import Solution, StepsModel
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.other_step import OtherStep

class Steps(StepsModel):
    first_step: FirstStep
    other_step: OtherStep


class {{ cookiecutter.__solution_definition_name }}(Solution):
    display_name = "{{ cookiecutter.solution_display_name.replace('"', '') }}"
    steps: Steps
