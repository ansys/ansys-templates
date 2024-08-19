# ©2024, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""


from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.second_step import SecondStep


def layout(step: SecondStep):
    """Layout of the second step page."""
    return html.Div(
        [
            html.Div(
                [
                    html.H2("Second step"),
                    html.P(
                        "This page is empty for now.",
                        className="lead",
                        style={"fontSize": "20px", "paddingTop": "0.5rem"},
                    ),
                ],
                style={"marginLeft": "0.5rem"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
        ]
    )
