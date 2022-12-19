# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.first_step import FirstStep
from dash_extensions.enrich import Input, Output, State, callback, dcc, html

def layout(step: FirstStep):
    return html.Div([
        html.Div(["First Argument: ", dcc.Input(id="first-arg", value=step.first_arg, type="number")]),
        html.Div(["Second Argument: ", dcc.Input(id="second-arg", value=step.second_arg, type="number")]),
        html.Button("Calculate", id="calculate", n_clicks=0),
        html.P(id="result", children=f"Result:{step.result}"),
    ])


# This is an example callback which stores entered data and executes a method.
# This is the only place where user entered data is persisted in this Dash app.
# Notice that the project is referenced by a call to get_project and
# the url is a State argument to the callback
@callback(
    Output("result", "children"),
    Input("calculate", "n_clicks"),
    State("first-arg", "value"),
    State("second-arg", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def calculate(n_clicks, first_arg, second_arg, pathname):
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    step = project.steps.first_step
    step.first_arg = first_arg
    step.second_arg = second_arg
    step.calculate()
    return f"Result:{step.result}"


