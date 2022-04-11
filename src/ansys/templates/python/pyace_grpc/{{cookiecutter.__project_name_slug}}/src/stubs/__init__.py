{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, 'stubs'))