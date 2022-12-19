# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys_dash_treeview import AnsysDashTreeview
from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import (
    {{ cookiecutter.__solution_definition_name }},
)
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui import first
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui import other
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, callback, callback_context, dcc, html
from dash_iconify import DashIconify


step_list = [
    {
        "key": "first",
        "text": "First",
        "depth": 0,
    },
    {
        "key": "other",
        "text": "Other",
        "depth": 0,
    }
]

layout = html.Div(
    [
        # represents the browser address bar and doesn't render anything
        dcc.Location(id="url", refresh=False),
        html.Img(src=r"/assets/Graphics/ansys-solutions-horizontal-logo.png"),
        # here we are rendering the step in its non-persisted form
        # just to initialize the layout so the callbacks can function
        # you could avoid this by suppressing callback errors - that's your call!
        html.Div(id="return-to-portal"),
        dbc.Row(
            children=[
                dbc.Col(
                    AnsysDashTreeview(
                        id="navigation_tree",
                        items=step_list,
                        children=[
                            DashIconify(icon="bi:caret-right-square-fill"),
                            DashIconify(icon="bi:caret-down-square-fill"),
                        ],
                        style={"showButtons": True, "focusColor": "#ffb71b", "itemHeight": "32"},  # Ansys gold
                    ),
                    width=2,
                    style={"background-color": "rgba(242, 242, 242, 0.6)"},  # Ansys grey
                ),
                dbc.Col(html.Div(id="page-content", style={"padding-right": "4%", "padding-top": "1%"}), width=10),
            ],
        ),
    ]
)


@callback(
    Output("return-to-portal", "children"),
    Input("url", "pathname"),
)
def return_to_portal(pathname):
    """Display Solution Portal when back-to-portal button gets selected."""
    portal_ui_url = DashClient.get_portal_ui_url()
    children = (
        []
        if portal_ui_url is None
        else [
            html.P(
                className="back-link",
                children=[
                    html.A(
                        href=portal_ui_url,
                        children=dbc.Button(
                            "Back to Projects",
                            id="return-button",
                            className="me-2",
                            n_clicks=0,
                            style={"background-color": "rgba(0, 0, 0, 1)", "border-color": "rgba(0, 0, 0, 1)"},
                        ),
                    )
                ],
            )
        ]
    )
    return children


# this callback is essential for initializing the step based on the persisted
# state of the project when the browser first displays the project to the user
# given the project's URL
@callback(
    Output("page-content", "children"),
    [
        Input("url", "pathname"),
        Input("navigation_tree", "focus"),
    ],
    prevent_initial_call=True,
)
def display_page(pathname, value):
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    error_message = None

    if triggered_id == "url":
        return first.layout(project.steps.first_step)

    if triggered_id == "navigation_tree":

        if value is None:
            page_layout = html.H1("Welcome!")

        elif value == "first":
            page_layout = first.layout(project.steps.first_step)
        elif value == "other":
            page_layout = other.layout()
     
        return page_layout


