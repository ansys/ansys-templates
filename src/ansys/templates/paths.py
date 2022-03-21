"""A collection of useful paths pointing towards each available template."""

import os
from pathlib import Path

_PATHS_MODULE = Path(os.path.dirname(os.path.abspath(__file__)))

LICENSES_TEMPLATES_PATH = _PATHS_MODULE / "licenses"
"""Path to the software licenses templates."""

PYTHON_TEMPLATES_PATH = _PATHS_MODULE / "python"
"""Path to the Python templates."""

PYTHON_TEMPLATES_COMMON_PATH = PYTHON_TEMPLATES_PATH / "common"
"""Path to the Python common template."""

PYTHON_TEMPLATES_PYBASIC_PATH = PYTHON_TEMPLATES_PATH / "pybasic"
"""Path to the basic Python Package template."""

PYTHON_TEMPLATES_PYANSYS_PATH = PYTHON_TEMPLATES_PATH / "pyansys"
"""Path to the basic PyAnsys Python Package template."""

PYTHON_TEMPLATES_PYANSYS_ADVANCED_PATH = PYTHON_TEMPLATES_PATH / "pyansys_advanced"
"""Path to the advanced PyAnsys Python Package template."""

TEMPLATE_PATH_FINDER = {
    "pybasic": PYTHON_TEMPLATES_PYBASIC_PATH,
    "pyansys": PYTHON_TEMPLATES_PYANSYS_PATH,
    "pyansys_advanced": PYTHON_TEMPLATES_PYANSYS_ADVANCED_PATH,
}
"""A dictionary relating templates names with their paths."""
