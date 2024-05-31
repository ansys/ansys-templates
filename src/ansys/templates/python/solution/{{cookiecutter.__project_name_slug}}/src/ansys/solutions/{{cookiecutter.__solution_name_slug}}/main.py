# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Entry point."""

from ansys.saf.glow.runtime import glow_main

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution import definition
{% if cookiecutter.dash_ui != "no" -%}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui import app
{%- endif %}


def main():
    """Entry point."""
    glow_main(definition{% if cookiecutter.dash_ui != "no" %}, app{% elif cookiecutter.dash_ui == "no" %}, None{% endif %})


if __name__ == "__main__":
    main()
