# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""


from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.second_step import SecondStep


def layout(step: SecondStep):
    """Layout of the second step page."""
    return html.Div(
        [
            html.H1("Second Step", className="display-3", style={"font-size": "48px", "fontWeight": "bold"}),
            html.P(
                "This page is empty for now.",
                className="lead",
                style={"font-size": "20px"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
        ]
    )
