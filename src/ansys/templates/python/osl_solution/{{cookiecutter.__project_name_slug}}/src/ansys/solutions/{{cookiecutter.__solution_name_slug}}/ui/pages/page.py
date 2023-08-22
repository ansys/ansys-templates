# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Initialization of the frontend layout across all the steps."""

from ansys_dash_treeview import AnsysDashTreeview
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback_context, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from pathlib import Path
import webbrowser

from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.saf.glow.core.method_status import MethodStatus

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.logs_table import LogsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages import monitoring_page, problem_setup_page
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import extract_dict_by_key


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False), # represents the browser address bar and doesn't render anything
        html.Div(
            id="progress_bar",
            style={
                'margin-left': '35%', 'margin-top': '25%'
            },
        ),
        dcc.Interval(
            id="progress_bar_update",
            interval=1000,
            n_intervals=0,
            disabled=False
        ),
        dcc.Store(id='trigger_layout_display'),
        dcc.Store(id='trigger_treeview_display'),
        dcc.Store(id='trigger_body_display'),
        html.Div(id="page_layout")
    ]
)


@callback(
    Output("trigger_layout_display", "data"),
    Input("url", "pathname"),
)
def initialization(pathname):
    """Run methods to initialize the solution."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    if not project.steps.problem_setup_step.project_initialized:
        # Solution-specific code
        project_tree_path = Path(__file__).absolute().parent.parent.parent / "model" / "assets" / "project_state.json"
        if not project_tree_path.exists():
            long_running = project.steps.problem_setup_step.generate_project_state()
            long_running.wait()
        # Project-specific code
        long_running = project.steps.problem_setup_step.upload_bulk_files_to_project_directory() # to be replaced by AssetFileReference
        long_running.wait()
        long_running = project.steps.problem_setup_step.read_project_tree()
        long_running.wait()
        long_running = project.steps.problem_setup_step.get_app_metadata()
        long_running.wait()
        long_running = project.steps.problem_setup_step.get_default_placeholder_values()
        long_running.wait()
        project.steps.problem_setup_step.project_initialized = True

    raise PreventUpdate


@callback(
    Output("trigger_layout_display", "data"),
    Output("progress_bar", "children"),
    Output("progress_bar", "style"),
    Output("progress_bar_update", "disabled"),
    Input("progress_bar_update", "n_intervals"),
    State("url", "pathname"),
)
def update_progress_bar(n_intervals, pathname):
    """Track status of solution initialization."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if not problem_setup_step.project_initialized:

        completion_rate = 0
        message = None
        methods = []

        project_tree_path = Path(__file__).absolute().parent.parent.parent / "model" / "assets" / "project_state.json"
        if not project_tree_path.exists():
            methods.append("generate_project_state")
        methods.extend(["upload_bulk_files_to_project_directory", "read_project_tree", "get_app_metadata", "get_default_placeholder_values"] )

        for method in methods:
            status = problem_setup_step.get_long_running_method_state(method).status
            if status == MethodStatus.Completed:
                completion_rate += 1
            elif status == MethodStatus.Running:
                message = method.replace("_", " ").capitalize()
                break

        completion_rate = round(completion_rate / len(methods) * 100)

        return (
            True,
            [
                dbc.Progress(
                    value=completion_rate,
                    label=f"{completion_rate} %",
                    color="rgba(255,182,35,1)",
                    style={"width": "600px", "height": "30px"},
                ),
                dbc.Label(message),
            ],
            {'margin-left': '35%', 'margin-top': '25%'},
            False
        )

    else:
        return True, [], {"display": "none"}, True


@callback(
    Output("trigger_treeview_display", "data"),
    Output("page_layout", "children"),
    Input("url", "pathname"),
    Input("trigger_layout_display", "data"),
)
def display_page_layout(pathname, trigger_layout_display):
    """Display page layout."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.project_initialized:
        return (
            True,
            [
                dbc.Stack(
                [
                    html.Div(
                        [
                            html.Img(
                            src = r"/assets/logos/ansys-solutions-horizontal-logo.png",
                            style={'width': '80%'}
                        )
                        ],
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                f"Project Name: {project.project_display_name}",
                                id = "project_name",
                                disabled = True,
                                style={
                                    "color": "rgba(0, 0, 0, 1)",
                                    "background-color": "rgba(255, 255, 255, 1)",
                                    "border-color": "rgba(0, 0, 0, 1)"
                                },
                            )
                        ],
                        className="ms-auto",
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "Back to Projects",
                                id = "return_to_portal",
                                className = "me-2",
                                n_clicks = 0,
                                href=DashClient.get_portal_ui_url(),
                                style = {"background-color": "rgba(0, 0, 0, 1)", "border-color": "rgba(0, 0, 0, 1)"},
                            )
                        ],
                    ),
                ],
                direction = "horizontal",
                gap = 3,
            ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            AnsysDashTreeview(
                                id="navigation_tree",
                                items=[
                                    {
                                        "key": "problem_setup_step",
                                        "text": "Problem Setup",
                                        "depth": 0,
                                        "uid": None,
                                        "type": None,
                                        "kind": None,
                                        "is_root": False,
                                    },
                                ],
                                children=[
                                    DashIconify(icon="bi:caret-right-square-fill"),
                                    DashIconify(icon="bi:caret-down-square-fill"),
                                ],
                                style={"showButtons": True, "focusColor": "#ffb71b", "itemHeight": "32"},  # Ansys gold
                            ),
                            width=2,
                            style={"background-color": "rgba(242, 242, 242, 0.6)"},  # Ansys grey
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    html.Div(
                                        id="body_content",
                                        style={"padding-right": "1%"}
                                    ),
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                dbc.Button(
                                                    "Open in browser",
                                                    id="open_in_browser",
                                                    style={"background-color": "rgba(242, 242, 242, 0.6)", "borderColor": "rgba(242, 242, 242, 0.6)", "color": "rgba(0, 0, 0, 1)"},
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                style={'position': 'absolute','right': '4px'}
                                            ),
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    dbc.Button(
                                                        "optiSLang logs",
                                                        id="optislang_logs_button",
                                                        n_clicks=0,
                                                        style={"background-color": "rgba(242, 242, 242, 0.6)", "borderColor": "rgba(242, 242, 242, 0.6)", "color": "rgba(0, 0, 0, 1)"},
                                                        size="sm"
                                                    ),
                                                    dbc.Collapse(
                                                        id="optislang_logs_collapse",
                                                        is_open=False,
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ],
                                )
                            ],
                            width=10
                        ),
                    ],
                ),
            ]
        )
    else:
        raise PreventUpdate


@callback(
    Output("trigger_body_display", "data"),
    Output("navigation_tree", "items"),
    Input("url", "pathname"),
    Input("trigger_treeview_display", "data"),
)
def display_tree_view(pathname, trigger_treeview_display):
    """Display treeview with all project nodes."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.project_initialized:
        return True, problem_setup_step.step_list
    else:
        raise PreventUpdate


@callback(
    Output("body_content", "children"),
    Input("navigation_tree", "focus"),
    Input("url", "pathname"),
    Input("trigger_body_display", "data"),
)
def display_body_content(value, pathname, trigger_body_display):
    """Display body content."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.project_initialized:
        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        if triggered_id == "url" or triggered_id == "trigger_body_display":
            return problem_setup_page.layout(problem_setup_step)
        if triggered_id == "navigation_tree":
            if value is None:
                page_layout = html.H1("Welcome!")
            elif value == "problem_setup_step":
                page_layout = problem_setup_page.layout(problem_setup_step)
            else:
                if not problem_setup_step.treeview_locked:
                    problem_setup_step.selected_actor_from_treeview = extract_dict_by_key(problem_setup_step.step_list, "key", value, expect_unique=True, return_index=False)["uid"]
                    page_layout = monitoring_page.layout(problem_setup_step)
                else:
                    page_layout = problem_setup_page.layout(problem_setup_step)
            return page_layout
    else:
        raise PreventUpdate


@callback(
    Output("optislang_logs_collapse", "children"),
    Output("optislang_logs_collapse", "is_open"),
    Input("optislang_logs_button", "n_clicks"),
    Input("url", "pathname"),
    State("optislang_logs_collapse", "is_open"),
    prevent_initial_call=True,
)
def display_optislang_logs(n_clicks, pathname, is_open):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if not n_clicks:
        # Button has never been clicked
        return None, False

    table = LogsTable(problem_setup_step.optislang_logs)

    return table.render(), not is_open


@callback(
    Output("open_in_browser", "children"),
    Input("open_in_browser", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def open_in_browser(n_clicks, pathname):
    """Open the Portal UI in browser view."""

    portal_ui_url = DashClient.get_portal_ui_url()
    webbrowser.open_new(portal_ui_url)

    raise PreventUpdate
