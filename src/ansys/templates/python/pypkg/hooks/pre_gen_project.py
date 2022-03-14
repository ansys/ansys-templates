"""The present script is executed before running the pypkg template."""

import os
from pathlib import Path

from ansys.templates.licenses import MIT_LICENSE
from ansys.templates.utils import inherit_from_template, include_license
from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH



def main():
    """Entry point of the hook script."""

    # Baked project directory path is always current one
    project_dirpath = os.getcwd()

    # Copy the whole Python template common directory 
    inherit_from_template(PYTHON_TEMPLATES_COMMON_PATH, project_dirpath)

    # Include the MIT license
    include_license(MIT_LICENSE, project_dirpath)


if __name__ == "__main__":
    main()
