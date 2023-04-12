# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""


from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.second_step import SecondStep


def layout(step: SecondStep):
    """Layout of the second step UI."""
    return html.Div(
        [
            dcc.Markdown("""#### Second step""", className="display-3"),
            dcc.Markdown("""###### Subtitle.""", className="display-3"),
            html.Hr(className="my-2"),
            html.Br(),
        ]
    )
