# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the about page."""

import base64
import os
from pathlib import Path

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
import dash_mantine_components as dmc


def layout():
    """Layout of the about page."""
    solution_workflow_sketch_encoded = base64.b64encode(
        open(
            os.path.join(Path(__file__).parent.parent.absolute(), "assets", "images", "solution-workflow-sketch.png"),
            "rb",
        ).read()
    )

    return html.Div(
        dbc.Container(
            [
                html.H1("{{cookiecutter.solution_display_name}}", className="display-3", style={"font-size": "48px", "fontWeight": "bold"}),
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
                                        dmc.Space(h=30),
                                        html.H4("Description", style={"font-size": "24px", "fontWeight": "bold"}),
                                        html.P(
                                            "Put here a short description of the solution.",
                                            style={"font-size": "16px", "textAlign": "justify"},
                                        ),
                                        dmc.Space(h=30),
                                        html.H4("Customer Goals", style={"font-size": "24px", "fontWeight": "bold"}),
                                        html.P(
                                            "What are the benefits for the customer?",
                                            style={"font-size": "16px", "textAlign": "justify"},
                                        ),
                                        dmc.Space(h=30),
                                        html.H4("Engineering Goals", style={"font-size": "24px", "fontWeight": "bold"}),
                                        html.P(
                                            "What is the engineering problem to solve? What are the Key Performance "
                                            "Indicators (KPIs) to monitor?",
                                            style={"font-size": "16px", "textAlign": "justify"},
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
        ),
    )
