"""A collection of useful paths pointing towards each available template."""

import os
from pathlib import Path

_PATHS_MODULE = Path(os.path.dirname(os.path.abspath(__file__)))

PYPKG_TEMPLATE_PATH = _PATHS_MODULE / "pypkg"
"""Path to the Python Package template."""

