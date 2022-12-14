# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.saf.glow.solution import Solution, StepsModel
from ansys.solutions.{{cookiecutter.solution_package_name}}.solution.first_step import FirstStep
from ansys.solutions.{{cookiecutter.solution_package_name}}.solution.other_step import OtherStep


class Steps(StepsModel):
    first_step: FirstStep
    other_step: OtherStep


class {{cookiecutter.solution_class_name}}(Solution):
    display_name = "{{cookiecutter.solution_display_name.replace('"', '')}}"
    steps: Steps
