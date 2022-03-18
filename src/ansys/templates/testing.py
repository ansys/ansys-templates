"""A collection of routines focused on testing."""


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
