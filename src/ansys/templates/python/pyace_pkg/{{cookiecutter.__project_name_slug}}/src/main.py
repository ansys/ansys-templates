{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""

from datetime import datetime

from logger import Logger

logger = Logger.init("{{ cookiecutter.project_name }}.{{ cookiecutter.library_name }}")


def get_date_and_time():
    """Compute today's datetime."""
    return datetime.today().strftime("%Y-%m-%d-%H:%M:%S")


if __name__ == "__main__":
    logger.info(f"Hello! Welcome, we are {get_date_and_time()}")
