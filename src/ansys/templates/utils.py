"""A collection of useful utilities and routines."""
from cookiecutter.main import cookiecutter
import tempfile
from pathlib import Path
from shutil import copytree, copyfile, rmtree

def bake_template(template_path, output_path, **cookiecutter_kwargs):
    """
    Bakes project using desired template and common files.

    Parameters
    ----------
    template_path: ~pathlib.Path
        Path to the template.
    output_path: ~pathlib.Path
        Output path for the baked template.
    **cookiecutter_kwargs: dict
        Additional cookiecutter keyword arguments.

    Notes
    -----
    Files from the common directory need to be copied before the cookiecutter
    context initializes. Otherwhise, copied files by a hook will not be
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
        
        # Bake the temporary project using cookiecutter with desired options
        cookiecutter(
            str(tmp_template_path), 
            output_dir=str(output_path), 
            **cookiecutter_kwargs
        )


def _copy_common_template_files(common_path, project_path):
    """
    Copy common template files into desired project directory.

    Parameters
    ----------
    common_path: ~pathlib.Path
        Path to the common template directory.
    project_path: ~pathlib.Path
        Path to the baked project directory.

    """
    copytree(
        common_path / "{{cookiecutter.__project_name_slug}}", 
        project_path / "{{cookiecutter.__project_name_slug}}", 
        dirs_exist_ok=True
    )


def _copy_all_template_files(template_path, project_path):
    """
    Copy all template files including cookiecutter.json and hooks/ directory.

    Parameters
    ----------
    template_path: ~pathlib.Path
        Path to the template directory.
    project_path: ~pathlib.Path
        Path to the baked project directory.

    """
    copytree(template_path, project_path, dirs_exist_ok=True)


def include_license(license_path, project_dirpath):
    """
    Include a desired license into the baked project.

    Parameters
    ----------
    license_path: ~pathlib.Path
        Path to the license template.
    project_dirpath: ~pathlib.Path
        Path to the baked project directory.

    Notes
    -----
    This function is intended to be used during the pre_gen_project.py hook.

    """
    copyfile(license_path, project_dirpath + "/" + license_path.name)
