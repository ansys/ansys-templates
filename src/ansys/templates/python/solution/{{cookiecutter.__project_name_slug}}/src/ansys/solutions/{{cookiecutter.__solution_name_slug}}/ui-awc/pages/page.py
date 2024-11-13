# ©2024, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Initialization of the frontend layout across all the steps."""

import webbrowser

from ansys.saf.glow.client.dashclient import DashClient, callback
import ansys_web_components_dash as AwcDash
from ansys_web_components_dash import AwcDashEnum, Tree
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, callback_context, dcc, html, State
from dash import clientside_callback, ctx


from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages import about_page, first_page, second_page

step_list = [
    {
        "id": "about_page",
        "text": "About",
        "prefixIcon": {"src": "https://s2.svgbox.net/hero-solid.svg?ic=home"},
        "expanded": True,
    },
    {
        "id": "first_page",
        "text": "First Step",
        "prefixIcon": {"src": "https://s2.svgbox.net/materialui.svg?ic=label"},
        "expanded": True,
    },
    {
        "id": "second_page",
        "text": "Second Step",
        "prefixIcon": {"src": "https://s2.svgbox.net/materialui.svg?ic=label_outline"},
        "expanded": True,
    },
]


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                html.Div(
                    [
                        AwcDash.Logo(appName="Solutions"),
                    ],
                    style={"width": "180px"},
                ),
                html.Div(
                    style={"flex": "1", "display": "flex", "justifyContent": "flex-end"},
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center"},
                            children=[
                                AwcDash.Label(
                                    id="label-name",
                                    text="Project name: ",
                                    awcSizing="hug",
                                    size=AwcDashEnum.LabelSize.MEDIUM.value,
                                ),
                                html.Div(
                                    id="project-name",
                                    style={
                                        "minWidth": "2rem",
                                        "fontSize": "16px",
                                        "paddingLeft": "0.25rem",
                                        "paddingRight": "1.25rem",
                                        "fontStyle": "bold",
                                    },
                                ),
                                AwcDash.Button(
                                    id="popout-button",
                                    text="Settings",
                                    iconOnly=True,
                                    type=AwcDashEnum.ButtonType.TERTIARY.value,
                                    size=AwcDashEnum.ButtonSize.MEDIUM.value,
                                    prefixIcon={"icon": AwcDashEnum.Icons.SETTINGS.value},
                                ),
                                AwcDash.Popout(
                                    [
                                        html.P("Theme"),
                                        html.Div(
                                            [
                                                AwcDash.Button(
                                                    id="auto-mode",
                                                    text="Auto",
                                                    icon={"icon": "magic"},
                                                    size="medium",
                                                    type="secondary",
                                                ),
                                                AwcDash.Button(
                                                    id="dark-mode",
                                                    text="Dark",
                                                    icon={"icon": "moon"},
                                                    size="medium",
                                                    type="secondary",
                                                ),
                                                AwcDash.Button(
                                                    id="light-mode",
                                                    text="Light",
                                                    icon={"icon": "lightbulb"},
                                                    size="medium",
                                                    type="secondary",
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "flexDirection": "row",
                                                "alignItems": "center",
                                                "justifyContent": "spaceBetween",
                                                "marginRight": "0.5rem",
                                                "gap": "0.125rem",
                                                "padding": "0.125rem",
                                                "border": "var(--awc-theme-border-neutral-lighter) 1px solid",
                                                "borderRadius": "0.25rem",
                                            },
                                        ),
                                    ],
                                    id="popout",
                                    anchor="popout-button",
                                    isOpen=False,
                                    padding=AwcDashEnum.Size._4x.value,
                                    elevation=AwcDashEnum.ElevationSize.X_LARGE.value,
                                    orientations=[
                                        AwcDashEnum.PopoutOrientation.BOTTOM_LEFT.value,
                                    ],
                                    borderRadius=AwcDashEnum.BorderRadius.LARGE.value,
                                ),
                                AwcDash.Button(
                                    id="access-dev-guide",
                                    text="User Guide",
                                    type=AwcDashEnum.ButtonType.TERTIARY.value,
                                    icon={"icon": AwcDashEnum.Icons.HELP.value},
                                    iconOnly=True,
                                    awcTooltip="Get access to the Solution Developer's Guide.",
                                ),
                                AwcDash.Button(
                                    id="return-to-portal",
                                    text="Back",
                                    iconOnly=True,
                                    type=AwcDashEnum.ButtonType.TERTIARY.value,
                                    icon={"icon": AwcDashEnum.Icons.ARROW_BACK.value},
                                    awcTooltip="Back to projects",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            id="header",
            style={
                "width": "100%",
                "padding": "0.5rem",
                "display": "flex",
                "justifyContent": "space-between",
                "border": "var(--awc-theme-border-neutral-lighter) 1px solid",
                "transition": "border 0.2s",
                "height": "4rem",
                "top": "0px",
                "position": "sticky !important",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            Tree(
                                id="navigation_tree",
                                multi=False,
                                height=250,
                                items=step_list,
                                selectedItemIds=["about_page"],
                            )
                        ),
                    ],
                    style={
                        "width": "15%",
                    },
                ),
                html.Div(
                    [
                        html.Div(id="page-content", style={"padding": "0.7%", "overflowY": "auto"}),
                    ],
                    style={
                        "width": "85%",
                        "borderLeft": "var(--awc-theme-border-neutral-lighter) 1px solid",
                        "transition": "border 0.2s",
                    },
                ),
            ],
            style={"display": "flex", "flexDirection": "row", "height": "calc(100vh - 4rem)"},
        ),
    ]
)


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
    Input("access-dev-guide", "clicked"),
    prevent_initial_call=True,
)
def access_dev_guide_documentation(n_clicks):
    """Open the Solution Developer's Guide in the web browser."""
    webbrowser.open_new("https://dev-docs.solutions.ansys.com/index.html")
    raise PreventUpdate

@callback(
    Output("navigation_tree", "focusRequested"),
    Output("page-content", "children"),
    [
        Input("url", "pathname"),
        Input("navigation_tree", "treeItemClicked"),
    ],
    prevent_initial_call=True,
)
def display_page(pathname, value):
    """Display page content."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    focusRequested = ""
    if triggered_id == "url":
        return "", about_page.layout()
    if triggered_id == "navigation_tree" and value:
        if value["id"] is None:
            page_layout = html.H1("Welcome!")
        elif value["id"] == "about_page":
            focusRequested = "about_page"
            page_layout = about_page.layout()
        elif value["id"] == "first_page":
            focusRequested = "first_page"
            page_layout = first_page.layout(project.steps.first_step)
        elif value["id"] == "second_page":
            focusRequested = "second_page"
            page_layout = second_page.layout(project.steps.second_step)
        return focusRequested, page_layout

# Manages the Open / close popup of settings
@callback(
    Output("popout", "isOpen"),
    Input("popout-button", "clicked"),
    State("popout", "isOpen"),
)
def popout_button_event_inside(popout_button, isOpen):
    if popout_button:
        return not isOpen
    raise PreventUpdate

# Manages the selection of the Modes buttons
@callback(
    [Output("auto-mode", "selected"), Output("dark-mode", "selected"), Output("light-mode", "selected")],
    [Input("auto-mode", "clicked"), Input("dark-mode", "clicked"), Input("light-mode", "clicked")],
)
def modes_on_callback(auto, dark, light):
    if ctx.triggered_id:
        if "light-mode" in ctx.triggered_id:
            return False, False, True
        elif "dark-mode" in ctx.triggered_id:
            return False, True, False
        elif "auto-mode" in ctx.triggered_id:
            return True, False, False
    else:
        raise PreventUpdate

clientside_callback(
    """
    (autoOn) => {
        document.documentElement.id = 'root';
        let browserMode = window.matchMedia("(prefers-color-scheme: dark)");
        console.log('Browser modeOn: ', browserMode.media, browserMode.matches)
        if(browserMode.matches){
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }
        return autoOn;
    }
    """,
    Output("auto-mode", "clicked"),
    Input("auto-mode", "clicked"),
)


clientside_callback(
    """
    (lightOn) => {
        if (lightOn){
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }
        return lightOn;
    }
    """,
    Output("light-mode", "clicked"),
    Input("light-mode", "clicked"),
)

clientside_callback(
    """
    (darkOn) => {
        if (darkOn){
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
        }
        return darkOn;
    }
    """,
    Output("dark-mode", "clicked"),
    Input("dark-mode", "clicked"),
)

clientside_callback(
    """
    (backOn) => {
        if (backOn){
            console.log('Return to the app')
            window.history.back();
        }
        return backOn;
    }
    """,
    Output("return-to-portal", "clicked"),
    Input("return-to-portal", "clicked"),
)