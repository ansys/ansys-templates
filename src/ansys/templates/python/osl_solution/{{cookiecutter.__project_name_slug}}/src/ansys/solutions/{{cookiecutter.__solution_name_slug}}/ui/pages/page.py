# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Initialization of the frontend layout across all the steps."""

from ansys.saf.glow.client.dashclient import DashClient
from ansys_dash_treeview import AnsysDashTreeview
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, callback_context, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_loading_spinners as dls
from pathlib import Path

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages import monitoring_page, problem_setup_page
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import extract_dict_by_key, read_system_hierarchy


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),  # represents the browser address bar and doesn't render anything
        dls.Pulse(
            color="#FFB71B",
            speed_multiplier=0.4,
            margin=4,
            width=57,
            fullscreen=True,
            fullscreen_style={
                "background-color": "rgba(255, 255, 255, 0)",
                "position": "relative"
            },
            children=html.Div(id="wait_app_initialization"),
        ),
        html.Div(
            id="page_content",
        ),
        dbc.Button(
            id="dummy_button",
            style={"display": "none"},
            n_clicks=0,
            color="dark"
        ),
    ]
)


@callback(
    Output("return_to_portal", "children"),
    Input("url", "pathname"),
)
def return_to_portal(pathname):
    """Display Solution Portal when back-to-portal button gets selected."""
    portal_ui_url = DashClient.get_portal_ui_url()
    children = (
        []
        if portal_ui_url is None
        else [
            dbc.Button(
                "Back to Projects",
                id="return_to_portal",
                className="me-2",
                n_clicks=0,
                href=portal_ui_url,
                style={"background-color": "rgba(0, 0, 0, 1)", "border-color": "rgba(0, 0, 0, 1)"},
            )
        ]
    )
    return children


@callback(
    Output("page_content", "children"),
    Output("dummy_button", "n_clicks"),
    Output("wait_app_initialization", "children"),
    Input("url", "pathname"),
    State("dummy_button", "n_clicks")
)
def project_initialization(pathname, n_clicks):

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    if not project.steps.problem_setup_step.project_initialized:
        # Solution-specific code
        project_tree_path = Path(__file__).absolute().parent.parent.parent / "model" / "assets" / "project_state.json"
        if not project_tree_path.exists():
            project.steps.problem_setup_step.generate_project_state()
        # Project-specific code
        project.steps.problem_setup_step.upload_bulk_files_to_project_directory()
        project.steps.problem_setup_step.read_project_tree()
        project.steps.problem_setup_step.get_app_metadata()
        project.steps.problem_setup_step.check_ansys_ecosystem()
        return [
            dbc.Stack(
                [
                    html.Div(
                        [html.Img(src=r"/assets/logos/ansys-solutions-horizontal-logo.png", style={"width": "80%"})],
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                f"Project Name: {project.project_display_name}",
                                id="project-name",
                                disabled=True,
                                style={
                                    "color": "rgba(0, 0, 0, 1)",
                                    "background-color": "rgba(255, 255, 255, 1)",
                                    "border-color": "rgba(0, 0, 0, 1)",
                                },
                            )
                        ],
                        className="ms-auto",
                    ),
                    html.Div(id="return_to_portal"),
                ],
                direction="horizontal",
                gap=3,
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
                    dbc.Col(html.Div(id="page_body", style={"padding-right": "1%"}), width=10),
                ],
            ),
        ], n_clicks + 1, True
    else:
        raise PreventUpdate


@callback(
    Output("navigation_tree", "items"),
    Input("dummy_button", "n_clicks"),
    Input("url", "pathname"),
)
def display_step_list(n_clicks, pathname):
    """Display current project name."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    return project.steps.problem_setup_step.step_list


@callback(
    Output("page_body", "children"),
    [
        Input("url", "pathname"),
        Input("navigation_tree", "focus"),
        Input("dummy_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def display_page_body(pathname, value, n_clicks):
    """
    Display page content.

    this callback is essential for initializing the step based on the persisted
    state of the project when the browser first displays the project to the user
    given the project's URL
    """

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "url" or triggered_id == "dummy_button":
        return problem_setup_page.layout(project.steps.problem_setup_step)
    if triggered_id == "navigation_tree":
        if value is None:
            page_layout = html.H1("Welcome!")
        elif value == "problem_setup_step":
            page_layout = problem_setup_page.layout(project.steps.problem_setup_step)
        else:
            node_info = extract_dict_by_key(project.steps.problem_setup_step.step_list, "key", value, expect_unique=True)
            page_layout = monitoring_page.layout(
                project.steps.problem_setup_step, project.steps.monitoring_step, node_info
            )
        return page_layout
