# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Sphinx documentation configuration file."""

# ==================================================== [Imports] ==================================================== #

from datetime import datetime
import os
from pathlib import Path

from ansys_sphinx_theme import ansys_favicon, get_version_match
import toml

# ============================================== [Project Information] ============================================== #

package_configuration = toml.load(Path(__file__).parent.parent.parent.absolute() / "pyproject.toml")

# Project information
project = package_configuration["tool"]["poetry"]["name"]
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = package_configuration["tool"]["poetry"]["version"]
cname = os.getenv("DOCUMENTATION_CNAME", "nocname.com")
repository = package_configuration["tool"]["poetry"].get("repository")

# ============================================ [Options for HTML output] ============================================ #

# Select desired logo, theme, and declare the html title
html_logo = str(Path(__file__).parent.absolute() / "_static" / "ansys-solutions-logo-black-background.png")
html_theme = "ansys_sphinx_theme"
html_favicon = ansys_favicon
html_short_title = html_title = package_configuration["tool"]["poetry"]["name"]

# specify the location of your github repo
html_theme_options = {
    "github_url": repository if repository is not None else "",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"{cname}/release/versions.json",
        "version_match": get_version_match(version),
    },
    "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_tabs.tabs"
]

# Intersphinx mapping
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"
