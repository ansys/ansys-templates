from pathlib import Path

from ansys.templates.paths import TEMPLATE_PATH_FINDER  # type: ignore
from ansys.templates.utils import bake_template  # type: ignore
import click  # type: ignore


@click.command()  # type: ignore
@click.option("-o", "--output", help="Output directory of the solution.")  # type: ignore
@click.option("-p", "--project-name", help="Project name.")  # type: ignore
@click.option("-s", "--solution-name", help="Solution name.")  # type: ignore
@click.option("-d", "--display-name", help="Solution display name")  # type: ignore
@click.option("-u", "--with-dash-ui", is_flag=True, help="With Dash UI")  # type: ignore
def create_new_solution(output: str, project_name: str, solution_name: str, display_name: str, with_dash_ui: bool):
    """Sequence of operations to create a new solution."""

    cookie_cutter_vars = {
        "project_name": project_name,
        "solution_name": solution_name,
        "solution_display_name": display_name,
    }

    if with_dash_ui:
        cookie_cutter_vars["with_dash_ui"] = "yes"
    else:
        cookie_cutter_vars["with_dash_ui"] = "no"

    output_path = Path(output)
    template_path = TEMPLATE_PATH_FINDER["osl_solution"]  # type: ignore
    bake_template(template_path, output_path, overwrite_if_exists=True, no_input=True, extra_context=cookie_cutter_vars)

if __name__ == "__main__":
    create_new_solution()  # type: ignore
