"""Sphinx documentation configuration file."""
from datetime import datetime
import os

from ansys_sphinx_theme import get_version_match
{%- if cookiecutter.__logo == "ansys" and cookiecutter.__logo_color == "white" %}
from ansys_sphinx_theme import ansys_logo_white as logo
{%- elif cookiecutter.__logo == "ansys" and cookiecutter.__logo_color == "black" %}
from ansys_sphinx_theme import ansys_logo_black as logo
{%- elif cookiecutter.__logo == "pyansys" and cookiecutter.__logo_color == "white" %}
from ansys_sphinx_theme import pyansys_logo_white as logo
{%- elif cookiecutter.__logo == "pyansys" and cookiecutter.__logo_color == "black" %}
from ansys_sphinx_theme import pyansys_logo_black as logo
{%- endif %}

{%- if cookiecutter.__template_name != "doc-project" %}
from {{cookiecutter.__pkg_namespace}} import __version__
{%- endif %}


# Project information
{%- if cookiecutter.__template_name in ["doc-project"] %}
project = "{{ cookiecutter.__project_name_slug }}"
{%- else %}
project = "{{ cookiecutter.__pkg_name }}"
{%- endif %}
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
{%- if cookiecutter.__template_name != "doc-project" %}
release = version = __version__
{%- elif cookiecutter.__template_name == "doc-project" %}
release = version = "{{ cookiecutter.__version }}"
{%- endif %}
cname = os.getenv("DOCUMENTATION_CNAME", "docs.pyansys.com")

# Select desired logo, theme, and declare the html title
html_logo = logo
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "{{ cookiecutter.__project_name_slug }}"

# specify the location of your github repo
html_theme_options = {
    "github_url": "{{ cookiecutter.__repository_url }}",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        {%- if cookiecutter.__logo == "ansys" %}
        ("Ansys", "https://dev.docs.ansys.com/"),
        {%- elif cookiecutter.__logo == "pyansys" %}
        ("PyAnsys", "https://docs.pyansys.com/"),
        {%- endif %}
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
    "check_switcher": False,
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

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
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"
