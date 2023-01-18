# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Entry point."""

from ansys.saf.glow.runtime import glow_main

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution import definition
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui import app


def main():
    """Entry point."""
    glow_main("{{ cookiecutter.__solution_name_slug }}", definition, app)


if __name__ == "__main__":
    main()
