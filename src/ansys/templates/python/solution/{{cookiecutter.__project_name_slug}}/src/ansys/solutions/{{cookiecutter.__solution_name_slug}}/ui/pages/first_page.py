# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the first step."""


from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.solutions.dash_components.table import InputRow, OutputRow
from dash_extensions.enrich import Input, Output, State, dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep


def layout(step: FirstStep):
    """Layout of the first step UI."""
    return html.Div(
        [
            dcc.Markdown("""#### First step""", className="display-3"),
            dcc.Markdown("""###### Compute the sum of two numbers.""", className="display-3"),
            html.Hr(className="my-2"),
            html.Br(),
            InputRow(
                "number",
                "first-arg",
                "First Argument",
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
                row_description="Enter a value.",
                label_width=2,
                value_width=4,
                unit_width=1,
                description_width=4,
                font_size="16px",
            ).get(),
            InputRow(
                "button",
                "calculate",
                "Calculate",
                label_width=2,
                value_width=4,
                unit_width=1,
                description_width=4,
                class_name="button",
                font_size="16px",
            ).get(),
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


# This is an example callback which stores entered data and executes a method.
# This is the only place where user entered data is persisted in this Dash app.
# Notice that the project is referenced by a call to get_project and
# the url is a State argument to the callback
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
    """Callback function to trigger the computation."""
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    step = project.steps.first_step
    step.first_arg = first_arg
    step.second_arg = second_arg
    step.calculate()
    return step.result, True
