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

"""A collection of useful utilities and routines."""
import json
import os
from pathlib import Path
import shutil
import tempfile

from cookiecutter.main import cookiecutter

from ansys.templates.licenses import MIT_LICENSE


def _copytree(input_path, output_path):
    """
    Recursively copy all the contents of a directory into desired one.

    Parameters
    ----------
    input_path : ~pathlib.Path
        Path of the source directory to be copied.
    output_path : ~pathlib.Path
        Path of the destination directory.

    """
    # Create output directory if it does not exist and ensure permission bits
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        shutil.copystat(input_path, output_path)

    # Get all file directories from the input directory
    files_list = os.listdir(input_path)

    for file in files_list:
        # Create source and destination file paths
        source_path = os.path.join(input_path, file)
        dest_path = os.path.join(output_path, file)

        # Recursion is used in case a directory is found
        if os.path.isdir(source_path):
            _copytree(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)


def _copy_common_template_files(common_path, project_path):
    """
    Copy common template files into desired project directory.

    Parameters
    ----------
    common_path : ~pathlib.Path
        Path to the common template directory.
    project_path : ~pathlib.Path
        Path to the baked project directory.

    """
    _copytree(
        common_path / "{{cookiecutter.__project_name_slug}}",
        project_path / "{{cookiecutter.__project_name_slug}}",
    )


def _copy_all_template_files(template_path, project_path):
    """
    Copy all template files including cookiecutter.json and hooks/ directory.

    Parameters
    ----------
    template_path : ~pathlib.Path
        Path to the template directory.
    project_path : ~pathlib.Path
        Path to the baked project directory.

    """
    _copytree(
        template_path,
        project_path,
    )


def _include_license(license_path, project_path):
    """
    Include a desired license into the baked project.

    Parameters
    ----------
    license_path : ~pathlib.Path
        Path to the license template.
    project_path : ~pathlib.Path
        Path to the baked project directory.

    Notes
    -----
    This function is intended to be used during the pre_gen_project.py hook.

    """
    shutil.copyfile(license_path, project_path / "{{cookiecutter.__project_name_slug}}/LICENSE")


def remove_file(filename, project_path=Path(os.getcwd())):
    """Remove desired file being given its relative path to project.

    Parameters
    ----------
    filename : str
        Filename relative to project root directory.
    project_path : Path
        Project's root directory.

    """
    filepath = project_path / filename
    filepath.unlink()


def keep_files(files_list, project_path=Path(os.getcwd())):
    """Remove undesired files except given ones from project.

    Parameters
    ----------
    files_list : list
        Desired file names relative to project's root directory.
    project_path : Path
        Project's root directory.

    """
    # Collect all the files in the project
    all_project_files = project_path.glob("**/*")

    # Fix path name according to OS flavor
    separator, new_separator = ("/", "\\") if os.name != "posix" else ("/", "/")
    desired_files = [file.replace(separator, new_separator) for file in files_list]

    folders = []
    # Removing undesired files
    for file in all_project_files:
        if str(file.relative_to(project_path)).replace(separator, new_separator) not in desired_files:
            file.unlink() if file.is_file() else folders.append(file)

    folders = sorted(folders, reverse=True)

    # Removing undesired empty folders
    [folder.rmdir() for folder in folders if not os.listdir(str(folder))]


def bake_template(template_path, output_path, license_path=MIT_LICENSE, **cookiecutter_kwargs):
    """
    Bakes project using desired template and common files.

    Parameters
    ----------
    template_path: ~pathlib.Path
        Path to the template.
    output_path: ~pathlib.Path
        Output path for the baked template.
    license_path: ~pathlib.Path
        Path to license file. Default is MIT.
    **cookiecutter_kwargs: dict
        Additional cookiecutter keyword arguments.

    Notes
    -----
    Files from the common directory need to be copied before the cookiecutter
    context initializes. Otherwise, copied files by a hook will not be
    rendered. This function creates a temporary directory where the common and
    desired template are combined so then cookiecutter can be executed.

    """
    # Create a temporary directory to be used as the final template source
    with tempfile.TemporaryDirectory() as tmp_template_path:

        # The common directory can be obtained from the template path
        common_path = template_path / "../common"

        # Copy the common and desired template files
        _copy_common_template_files(common_path, Path(str(tmp_template_path)))
        _copy_all_template_files(template_path, Path(str(tmp_template_path)))

        # Copy license file
        _include_license(license_path, Path(str(tmp_template_path)))

        # Bake the temporary project using cookiecutter with desired options
        cookiecutter(str(tmp_template_path), output_dir=str(output_path), **cookiecutter_kwargs)


def load_inputs_from_configuration_file(template_path):
    """
    Read the cookiecutter.json file and return the inputs only.

    Parameters
    ----------
    template_path: ~pathlib.Path
        Path to the template.
    """
    with open(template_path / "cookiecutter.json", 'r') as json_file:
        configuration = json.load(json_file)

    inputs = {}
    for key, value in configuration.items():
        if key.startswith("_"):
            continue
        if isinstance(value, list):
            inputs[key] = value[0]
        else:
            inputs[key] = value

    return inputs
