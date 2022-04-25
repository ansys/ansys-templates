{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""

import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, "stubs"))
