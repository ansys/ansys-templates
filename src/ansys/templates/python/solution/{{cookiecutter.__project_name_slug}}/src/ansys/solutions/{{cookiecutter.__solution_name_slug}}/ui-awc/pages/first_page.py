# ©2024, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the first step."""


from ansys.saf.glow.client.dashclient import DashClient, callback
import ansys_web_components_dash as AwcDash
from ansys_web_components_dash import AwcDashEnum
from dash_extensions.enrich import Input, Output, State, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep


def layout(step: FirstStep):
    """Layout of the first step page."""
    return html.Div(
        [
            html.Div(
                [
                    html.H2("First step"),
                    html.P(
                        "Compute the sum of two numbers.",
                        className="lead",
                        style={"fontSize": "20px", "paddingTop": "0.5rem"},
                    ),
                ],
                style={"marginLeft": "0.5rem"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
            html.Div(
                [
                    # First input
                    html.Div(
                        [
                            AwcDash.NumberInput(
                                id="first-arg",
                                label="First Argument",
                                loading=False,
                                placeholder="Enter a value",
                                size=AwcDashEnum.InputSize.SMALL.value,
                                disabled=False,
                                hint="Only accepts numeric input",
                                step=1,
                                value=step.first_arg,
                            )
                        ],
                        style={"width": "100%", "display": "inline-block"},
                    ),
                    html.Br(),
                    # Second input
                    html.Div(
                        [
                            AwcDash.NumberInput(
                                id="second-arg",
                                label="Second argument",
                                loading=False,
                                placeholder="Enter a value",
                                size=AwcDashEnum.InputSize.SMALL.value,
                                disabled=False,
                                hint="Only accepts numeric input",
                                step=1,
                                value=step.second_arg,
                            )
                        ],
                        style={"width": "100%", "display": "inline-block"},
                    ),
                    html.Br(),
                    # calculate button
                    html.Div(
                        [
                            AwcDash.Button(
                                text="Calculate",
                                size="medium",
                                type="primary",
                                prefixIcon={"icon": "rocket"},
                                id="calculate",
                                awcSizing="hug",
                            ),
                        ],
                        style={"width": "100%", "display": "inline-block", "paddingTop": "2%", "textAlign": "end"},
                    ),
                    html.Br(),
                    # result input box
                    html.Div(
                        [
                            AwcDash.Input(
                                id="result",
                                size=AwcDashEnum.InputSize.SMALL.value,
                                inlineEdit=False,
                                readOnly=True,
                                placeholder="Calculated result",
                                value=step.result,
                                label="Result",
                            )
                        ],
                        style={"width": "100%", "display": "inline-block"},
                    ),
                ],
                style={"width": "30%", "marginLeft": "1.5rem", "display": "flex", "flexDirection": "column"},
            ),
        ],
        style={"width": "100%"},
    )


@callback(
    Output("result", "value"),
    Input("calculate", "clicked"),
    State("first-arg", "value"),
    State("second-arg", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def calculate(clicked, first_arg, second_arg, pathname):
    """Trigger the computation."""
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    step = project.steps.first_step
    step.first_arg = first_arg
    step.second_arg = second_arg
    step.calculate()
    return step.result
