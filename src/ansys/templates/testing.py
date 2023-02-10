# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A collection of routines focused on testing."""

import os

from ansys.templates.utils import bake_template


def assert_template_baking_process(template_path, output_path, cookiecutter_vars):
    """
    Assert if template renders properly.

    Parameters
    ----------
    template_path : ~pathlib.Path
        Path to the project template.
    output_path : ~pathlib.Path
        Path to the output baked project.
    cookiecutter_vars : dict
        A dictionary holding cookiecutter variables and their values.

    """
    bake_template(
        template_path,
        output_path,
        overwrite_if_exists=True,
        no_input=True,
        extra_context=cookiecutter_vars,
    )


def assert_file_in_baked_project(file, project_path):
    """
    Assert if file is exists inside desired output path.

    Parameters
    ----------
    file : str
        Expected file path relative to the output project path.
    project_path : ~pathlib.Path
        Path to the output project path.
    """
    assert (project_path.joinpath(file)).is_file()


def assert_files_in_baked_project(files_list, project_path):
    """
    Assert if given files exists inside desired output path.

    Parameters
    ----------
    files_list : list
        A list of expected files path relative to the output project path.
    project_path : ~pathlib.Path
        Path to the output project path.
    """
    for file in files_list:
        assert_file_in_baked_project(file, project_path)

def assert_project_structure(expected_structure, project_path):
    """Assert if project has desired structure.

    If any additional files are encountered in the rendered project, it will
    raise an AssertionError.

    Parameters
    ----------
    expected_structure : list
        A list of expected files path relative to the output project path.
    project_path : ~pathlib.Path
        Path to the output project path.

    """
    # Fix path name according to OS flavor
    separator, new_separator = ("/", "\\") if os.name != "posix" else ("/", "/")

    # Sort expected and current structures
    expected_structure = sorted(
        [file.replace(separator, new_separator) for file in expected_structure]
    )
    current_structure = sorted(
        [
            str(file.relative_to(project_path)).replace(separator, new_separator)
            for file in project_path.glob("**/*") if file.is_file()
        ]
    )

    try:
        for current_file, expected_file in zip(current_structure, expected_structure):
            assert current_file == expected_file

        assert len(current_structure) == len(expected_structure)
    except AssertionError:
        msg = f"File {current_file} not equals to {expected_file}\n\n"
        msg += f"Current structure = {current_structure}\n"
        msg += f"Expected structure = {expected_structure}\n"
        raise AssertionError(msg)
