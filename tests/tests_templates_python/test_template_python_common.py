from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from ansys.templates.paths import PYTHON_TEMPLATES_COMMON_PATH
from ansys.templates.testing import assert_template_renders_properly


def test_template_python_common(tmpdir):

    # Main variables for of the common template
    cookiecutter_vars = {
      "__project_name_slug": "",
      "__version": "",
      "__pkg_name": "",
      "__pkg_namespace": "",
      "__requires_python": "",
      "__repository_url": "",
      "__max_linelength": "",
    }

    # Assert no errors were raised during template rendering process
    assert_template_renders_properly(
        PYTHON_TEMPLATES_COMMON_PATH, tmpdir, cookiecutter_vars
    )
