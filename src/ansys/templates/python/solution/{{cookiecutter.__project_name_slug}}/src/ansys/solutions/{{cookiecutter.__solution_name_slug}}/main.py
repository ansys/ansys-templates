# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Entry point."""

from ansys.saf.glow.runtime import glow_main

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution import definition
{% if cookiecutter.no_ui == "False" %}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui import app
{% endif %}


def main():
    """Entry point."""

    {% if cookiecutter.no_ui == "False" %}
    glow_main("{{ cookiecutter.__solution_name_slug }}", definition, app)
    {% else %}
    glow_main("{{ cookiecutter.__solution_name_slug }}", definition)
    {% endif %}


if __name__ == "__main__":
    main()
