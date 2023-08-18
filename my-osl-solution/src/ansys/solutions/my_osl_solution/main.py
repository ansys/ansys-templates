# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Entry point."""

from ansys.saf.glow.runtime import glow_main

from ansys.solutions.my_osl_solution.solution import definition
from ansys.solutions.my_osl_solution.ui import app


def main():
    """Entry point."""

    glow_main(definition, app)


if __name__ == "__main__":
    main()
