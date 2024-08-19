# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Initialization of the frontend layout across all the steps."""


import json
import webbrowser

from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.solutions.dash_super_components import Tree
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, callback_context, dcc, html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages import about_page, first_page, second_page

step_list = [
    {
        "id": "about_page",
        "text": "About",
        "prefixIcon": "material-symbols:home",
        "expanded": True,
    },
    {
        "id": "first_page",
        "text": "First Step",
        "prefixIcon": "game-icons:crossed-air-flows",
        "expanded": True,
    },
    {
        "id": "second_page",
        "text": "Second Step",
        "prefixIcon": "carbon:ibm-engineering-workflow-mgmt",
        "expanded": True,
    },
]


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        children=[
                            html.Div(
                                html.Img(src=r"/assets/logos/ansys_solutions_logo_white.png", height="36px"),
                                style={
                                    "flex": "1",
                                    "text-align": "left",
                                },
                            ),
                            html.Div(
                                dmc.Group(
                                    [
                                        dmc.Text(
                                            "Project name:",
                                            id="project-name",
                                            size="sm",
                                            color="#FFFFFF",
                                            style={"font-size": "16px"},
                                        ),
                                        dmc.ActionIcon(
                                            DashIconify(icon="ph:code-fill", width=36),
                                            id="access-dev-guide",
                                            size=36,
                                            variant="transparent",
                                            style={"color": "#FFFFFF"},
                                        ),
                                        dbc.Popover(
                                            "Get access to the Solution's Developer Guide.",
                                            target="access-dev-guide",
                                            body=True,
                                            trigger="hover",
                                        ),
                                        html.Div(id="return-to-portal"),
                                    ],
                                    spacing=10,
                                ),
                                style={
                                    "display": "flex",
                                    "align-items": "flex-end",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justify-content": "space-between",
                            "width": "100%",
                        },
                    )
                ],
                style={"max-width": "inherit"},
                fluid=True,
            ),
            color="#000000",
            sticky="top",
            style={"height": "80px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dmc.Space(h=10),
                        dbc.Row(
                            Tree(
                                aio_id="navigation_tree",
                                items=step_list,
                                active_item_id="about_page",
                            )
                        ),
                    ],
                    width=2,
                ),
                dbc.Col(html.Div(id="page-content", style={"padding-right": "0.7%"}), width=10),
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
            html.A(
                [
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:return", width=36),
                        id="back-to-projects-icon",
                        size=36,
                        variant="transparent",
                        style={"color": "#FFFFFF"},
                    ),
                    dbc.Popover(
                        "Back to Projects.",
                        target="back-to-projects-icon",
                        body=True,
                        trigger="hover",
                    ),
                ],
                href=portal_ui_url,
            )
        ]
    )
    return children


@callback(
    Output("project-name", "children"),
    Input("url", "pathname"),
)
def display_poject_name(pathname):
    """Display current project name."""
    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    return f"Project Name: {project.project_display_name}"


@callback(
    Output("access-dev-guide", "children"),
    Input("access-dev-guide", "n_clicks"),
    prevent_initial_call=True,
)
def access_dev_guide_documentation(n_clicks):
    """Open the Developer's Guide home page in the web browser."""
    webbrowser.open_new("https://dev-docs.solutions.ansys.com/index.html")
    raise PreventUpdate


@callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input(Tree.ids.selected_item("navigation_tree"), "data"),
    prevent_initial_call=True,
)
def display_page(pathname, value):
    """Display page content."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "url":
        return about_page.layout()
    else:
        triggered_id = json.loads(triggered_id)
        if isinstance(triggered_id, dict):
            if triggered_id["aio_id"] == "navigation_tree":
                if value["index"] == "about_page":
                    return about_page.layout()
                elif value["index"] == "first_page":
                    return first_page.layout(project.steps.first_step)
                elif value["index"] == "second_page":
                    return second_page.layout(project.steps.second_step)
                else:
                    raise ValueError(f"Unknown page selection: {value['index']}")
    raise PreventUpdate
