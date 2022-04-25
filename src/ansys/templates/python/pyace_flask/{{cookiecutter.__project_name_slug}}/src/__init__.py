"""{{ cookiecutter.__project_name_slug }}."""
{%- if cookiecutter.copyright != "None" %}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

import os
import sys

from ._version import __version__

sys.path.append(os.path.join(os.path.dirname(__file__)))
