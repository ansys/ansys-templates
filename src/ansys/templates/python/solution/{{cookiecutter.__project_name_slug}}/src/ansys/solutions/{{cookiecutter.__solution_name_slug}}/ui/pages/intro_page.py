# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the first step."""

import base64
import os
from pathlib import Path

import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.intro_step import IntroStep


def layout(step: IntroStep):
    """Layout of the first step UI."""

    solution_workflow_sketch_encoded = base64.b64encode(
        open(
            os.path.join(Path(__file__).parent.parent.absolute(), "assets", "images", "solution-workflow-sketch.png"),
            "rb",
        ).read()
    )

    return html.Div(
        dbc.Container(
            [
                html.H1("Add a title.", className="display-3", style={"font-size": "35px"}),
                html.P(
                    "Add a short sentence to describe the goal of the solution.",
                    className="lead",
                    style={"font-size": "20px"},
                ),
                html.Hr(className="my-2"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dcc.Markdown(
                                            """
                                            **Description**

                                            Information needed.
                                            """,
                                            className="lead",
                                            style={
                                                "textAlign": "left",
                                                "marginLeft": "auto",
                                                "marginRight": "auto",
                                                "font-size": "15px",
                                            },
                                        ),
                                        html.Br(),
                                        dcc.Markdown(
                                            """
                                            **Customer goals**

                                            Information needed.
                                            """,
                                            className="lead",
                                            style={
                                                "textAlign": "left",
                                                "font-size": "15px",
                                            },
                                        ),
                                        html.Br(),
                                        dcc.Markdown(
                                            """
                                            **Engineering goals**

                                            Information needed.
                                            """,
                                            className="lead",
                                            style={
                                                "textAlign": "left",
                                                "font-size": "15px",
                                            },
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardImg(
                                                    src="data:image/png;base64,{}".format(
                                                        solution_workflow_sketch_encoded.decode()
                                                    ),
                                                ),
                                                dbc.CardFooter("This is the introduction image."),
                                            ],
                                            style={"width": "50rem"},
                                        )
                                    ]
                                )
                            ],
                            width=6,
                        ),
                    ]
                ),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )
