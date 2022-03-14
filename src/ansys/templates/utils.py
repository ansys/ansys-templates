"""A collection of useful utilities and routines."""

from shutil import copytree, copyfile

def inherit_from_template(common_dirpath, project_dirpath):
    """
    Inherits current template by combining custom and common files.

    Parameters
    ----------
    common_dirpath: ~pathlib.Path
        Path to the common template directory.
    project_dirpath: ~pathlib.Path
        Path to the baked project directory.

    Notes
    -----
    This function is intended to be used during the pre_gen_project.py hook.

    """
    copytree(
        common_dirpath / "{{cookiecutter.__project_name_slug}}", 
        project_dirpath, 
        dirs_exist_ok=True
    )


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

