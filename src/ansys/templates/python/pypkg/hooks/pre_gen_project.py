"""The present script is executed before running the pypkg template."""

import os

from ansys.templates.utils import inherit_from_template
from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH



def main():
    """Entry point of the hook script."""

    # Copy the whole Python template common directory 
    pwd = os.getcwd() + "/{{cookiecutter.__project_name_slug}}"
    inherit_from_template(PYTHON_TEMPLATES_COMMON_PATH, pwd)


if __name__ == "__main__":
    main()
