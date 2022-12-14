# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.saf.glow.runtime import glow_main
from ansys.solutions.{{cookiecutter.solution_package_name}}.solution import definition
from ansys.solutions.{{cookiecutter.solution_package_name}}.ui import app


def main():
    glow_main("{{cookiecutter.solution_package_name}}", definition, app)


if __name__ == "__main__":
    main()
