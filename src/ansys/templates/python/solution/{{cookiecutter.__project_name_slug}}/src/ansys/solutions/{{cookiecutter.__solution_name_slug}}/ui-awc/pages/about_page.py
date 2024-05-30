# ©2024, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the about page."""

import base64
import os
from pathlib import Path

import ansys_web_components_dash as AwcDash
from ansys_web_components_dash import AwcDashEnum
from dash_extensions.enrich import html


def layout():
    """Layout of the about page."""
    solution_workflow_sketch_encoded = base64.b64encode(
        open(
            os.path.join(Path(__file__).parent.parent.absolute(), "assets", "images", "solution-workflow-sketch.png"),
            "rb",
        ).read()
    )

    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        html.H2("testApp"),
                        html.P(
                            "Add a short sentence to describe the goal of the solution.",
                            className="lead",
                            style={"fontSize": "20px", "paddingTop": "0.5rem"},
                        ),
                    ],
                    style={"marginLeft": "0.5rem"},
                ),
                html.Hr(className="my-2"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Description", style={"paddingTop": "2rem"}),
                                html.P("Add a short description of the solution."),
                                html.H4("Customer goals", style={"paddingTop": "2rem"}),
                                html.P("What are the benefits for the customer?"),
                                html.H4("Engineering goals", style={"paddingTop": "2rem"}),
                                html.P("What is the engineering problem to solve?"),
                                html.P("What are the Key Performance Indicators (KPIs) to monitor?"),
                            ],
                            style={"width": "50%", "marginLeft": "1.5rem", "marginBottom": "1.5rem"},
                        ),
                        html.Div(
                            [
                                AwcDash.Card(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="data:image/png;base64,{}".format(
                                                        solution_workflow_sketch_encoded.decode()
                                                    ),
                                                    style={"width": "100%", "height": "auto"},
                                                ),
                                                html.Hr(className="my-2"),
                                                html.Div(
                                                    "This is the introduction image.",
                                                    style={"fontSize": "15px"},
                                                ),
                                            ],
                                        ),
                                    ],
                                    elevation=AwcDashEnum.ElevationSize.SMALL.value,
                                    borderRadius=AwcDashEnum.BorderRadius.LARGE.value,
                                    padding=AwcDashEnum.Size._4x.value,
                                    awcSizing="fill",
                                )
                            ],
                            style={"width": "46%"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "flexWrap": "wrap",
                        "justifyConten": "spaceEvenly",
                    },
                ),
            ],
        ),
    )
