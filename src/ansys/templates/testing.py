"""A collection of routines focused on testing."""

from cookiecutter.main import cookiecutter

def assert_template_renders_properly(template_path, output_path, cookiecutter_vars):
    """
    Asserts if template renders properly.

    Parameters
    ----------
    template_path: ~pathlib.Path
        Path to the project template.
    output_path: ~pathlib.Path
        Path to the output baked project.
    cookiecutter_vars: dict
        A dictionary holding cookiecutter variables and their values.

    """
    cookiecutter(
        template=str(template_path),
        overwrite_if_exists=True,
        output_dir=str(output_path),
        no_input=True,
        extra_context=cookiecutter_vars
    )
