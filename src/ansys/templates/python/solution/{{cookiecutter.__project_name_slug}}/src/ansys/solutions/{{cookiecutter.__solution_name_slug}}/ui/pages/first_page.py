# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the first step."""


from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.solutions.dash_components.table import InputRow, OutputRow
from dash_extensions.enrich import Input, Output, State, dcc, html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep


def layout(step: FirstStep):
    """Layout of the first step page."""
    return html.Div(
        [
            html.H1("First Step", className="display-3", style={"font-size": "48px", "fontWeight": "bold"}),
            html.P(
                "Compute the sum of two numbers.",
                className="lead",
                style={"font-size": "20px"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
            InputRow(
                "number",
                "first-arg",
                "First Argument",
                row_default_value=step.first_arg,
                row_description="Enter a value.",
                label_width=2,
                value_width=4,
                unit_width=1,
                description_width=4,
                font_size="16px",
            ).get(),
            InputRow(
                "number",
                "second-arg",
                "Second Argument",
                row_default_value=step.second_arg,
                row_description="Enter a value.",
                label_width=2,
                value_width=4,
                unit_width=1,
                description_width=4,
                font_size="16px",
            ).get(),
            html.Br(),
            html.Div(
                dmc.Button(
                    "Calculate",
                    id="calculate",
                    leftIcon=DashIconify(icon="streamline:startup-solid"),
                    radius="xl",
                    disabled=False,
                    className="mantine-button",
                    style={"color": "#FFFFFF", "width": "100%", "background-color": "#000000", "font-size": "14px"},
                ),
                style={
                    "textAlign": "center",
                    "margin-left": "275px",
                    "width": "500px",
                },
            ),
            html.Br(),
            OutputRow(
                "number",
                "result",
                "Result",
                row_default_value=step.result,
                label_width=2,
                value_width=4,
                unit_width=1,
                description_width=4,
                class_name="button",
                font_size="16px",
            ).get(),
            dcc.Loading(
                type="circle",
                fullscreen=True,
                color="#ffb71b",
                style={
                    "background-color": "rgba(55, 58, 54, 0.1)",
                },
                children=html.Div(id="wait_completion"),
            ),
        ]
    )


@callback(
    Output("result", "value"),
    Output("wait_completion", "children"),
    Input("calculate", "n_clicks"),
    State("first-arg", "value"),
    State("second-arg", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def calculate(n_clicks, first_arg, second_arg, pathname):
    """Trigger the computation."""
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    step = project.steps.first_step
    step.first_arg = first_arg
    step.second_arg = second_arg
    step.calculate()
    return step.result, True
