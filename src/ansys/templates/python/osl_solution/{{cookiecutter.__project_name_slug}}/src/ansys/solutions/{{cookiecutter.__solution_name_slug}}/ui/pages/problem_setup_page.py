# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the problem setup step."""

import dash_bootstrap_components as dbc
import os
import time

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, dcc, html, ALL, MATCH, no_update, callback_context

from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.saf.glow.core.method_status import MethodStatus
from ansys.solutions.optislang.frontend_components.load_sections import to_dash_sections, update_designs_to_dash_section

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import check_empty_strings


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the problem setup step."""

    project_properties_sections = to_dash_sections(
            problem_setup_step.placeholders, problem_setup_step.registered_files, problem_setup_step.project_locked
        )

    return html.Div(
        [
            # Header
            html.H1(
                problem_setup_step.app_metadata["title"].strip().title(),
                className="display-3",
                style={"font-size": "45px"},
            ),
            html.P(
                problem_setup_step.app_metadata["description"].strip(),
                className="lead",
                style={"font-size": "25px"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
            # Alerts
            dbc.Row(
                id="project-locked-alert",
                children=[
                    dbc.Alert(
                        "The selected inputs are locked. To set new inputs, create a new project.",
                        color="info",
                    )
                ],
                style={"display": "block"} if problem_setup_step.project_locked else {"display": "none"},
            ),
            html.Br(),
            # Input form
            html.H1("Input Form", style={"font-size": "20px"}),
            html.Hr(className="my-2"),
            dbc.Row(id="osl-dash-sections",children=project_properties_sections),
            html.Br(),
            # Start analysis
            html.H1("Start Analysis", style={"font-size": "20px"}),
            html.Hr(className="my-2"),
            dbc.Row(
                [
                    html.Div(
                        [
                            dbc.Button(
                                html.I(className="fas fa-play", style={"display": "inline-block"}),
                                id="start_analysis",
                                disabled=problem_setup_step.analysis_locked,
                                style = {
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "fontSize": "150%",
                                    "background-color": "rgba(0, 0, 0, 1)",
                                    "border-color": "rgba(0, 0, 0, 1)",
                                    "height": "30px",
                                }
                            ),
                            dbc.Tooltip(
                                "Start optiSLang project execution.",
                                target="start_analysis",
                            ),
                        ],
                        className="d-grid gap-2 col-5 mx-auto",
                    ),
                    dcc.Loading(
                        type="circle",
                        fullscreen=True,
                        color="#ffb71b",
                        style={
                            "background-color": "rgba(55, 58, 54, 0.1)",
                        },
                        children=html.Div(id="wait_start_analysis"),
                    ),
                    dcc.Interval(
                        id="solve_interval_component",
                        interval=1 * 3000,  # in milliseconds
                        n_intervals=0,
                    ),
                    dbc.Button(
                        id="dummy_button_2",
                        style={"display": "none"},
                        n_clicks=0,
                        color="dark"
                    ),
                ]
            ),
        ]
    )


@callback(
    Output("trigger_treeview_display", "data"),
    Output("navigation_tree", "items"),
    Output("wait_start_analysis", "children"),
    Output("start_analysis", "disabled"),
    Output("osl-dash-sections", "children"),
    Output("project-locked-alert", "style"),
    Input("start_analysis", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def start_analysis(n_clicks, pathname):
    """Start optiSLang and run the project."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    monitoring_step = project.steps.monitoring_step

    if n_clicks:
        ui_data = problem_setup_step.ui_placeholders
        ui_data.update({"start_analysis_requested": True})
        problem_setup_step.ui_placeholders = ui_data
        # Check if Ansys products are available
        project.steps.problem_setup_step.check_ansys_ecosystem()
        if problem_setup_step.ansys_ecosystem_ready:
            # Read project tree and update treeview
            problem_setup_step.get_project_tree()
            # Update project properties file prior to the solve
            problem_setup_step.write_updated_properties_file()
            # Start analysis
            problem_setup_step.start()
            # Lock start analysis and ui data
            problem_setup_step.analysis_locked = True
            problem_setup_step.project_locked = True
            # Start monitoring
            monitoring_step.upload_project_data()
            # Wait until the analysis effectively starts
            while monitoring_step.project_state == "NOT STARTED":
                time.sleep(1)
            return (
                True,
                problem_setup_step.treeview_items,
                True,
                True,
                to_dash_sections(
                    problem_setup_step.placeholders, problem_setup_step.registered_files, problem_setup_step.project_locked
                ),
                {"display": "block"},
            )
        else:
            return (
                True,
                problem_setup_step.treeview_items,
                True,
                False,
                to_dash_sections(
                    problem_setup_step.placeholders, problem_setup_step.registered_files, problem_setup_step.project_locked
                ),
                {"display": "block"},
            )
    else:
        raise PreventUpdate


@callback(
    Output("start_analysis", "disabled"),
    Input("dummy_button_2", "n_clicks"),
    State({"container": "placeholders", "placeholder": ALL}, "value"),
    State({"container": "placeholders", "placeholder": ALL}, "id"),
    State({"type": "upload", "placeholder": ALL}, "id"),
    State("dummy_button_2", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def initialize_dictionary_of_ui_placeholders(n_clicks, data, ids, input_file_ids, dummy_clicks, pathname):
    """This initializes the dictionary of ui placeholders using only the values in the Placeholders section."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    designs = {}
    parameters = {}
    if problem_setup_step.ui_placeholders == {}:
        ui_data = problem_setup_step.ui_placeholders
        for index in range(len(data)):
            if ids[index]["placeholder"].startswith("StartDesigns"):
                split_values = ids[index]["placeholder"].split("##")
                values = split_values[1:]
                rowId = values[0].split("#")[1]
                key = values[1].split("#")[1]
                value = values[2].split("#")[1]
                if rowId in designs:
                    designs[rowId].update({key: value})
                else:
                    designs[rowId] = {key: value}
            elif ids[index]["placeholder"].startswith("ParameterManager"):
                split_values = ids[index]["placeholder"].split("##")
                values = split_values[1:]
                placeholder_name = values[0].split("#")[0]
                key = values[0].split("#")[1]
                if isinstance(data[index], list) and True in data[index]:
                    parameters[key] = True
                elif isinstance(data[index], list) and False in data[index]:
                    parameters[key] = False
                else:
                    parameters[key] = data[index]
                ui_data.update({placeholder_name: parameters})
            elif "Bool" in ids[index]["placeholder"] and type(data[index]) == list:
                value = data[index]
                if True in value:
                    new_value = True
                else:
                    new_value = False
                ui_data.update({ids[index]["placeholder"]: new_value})
            else:
                ui_data.update({ids[index]["placeholder"]: data[index]})
            ui_data.update({"StartDesigns": designs})
            ui_data["start_analysis_requested"] = False
        if input_file_ids:
            problem_setup_step.analysis_locked = True
        else:
            problem_setup_step.analysis_locked = False
        for index in range(len(input_file_ids)):
            ui_data.update({input_file_ids[index]["placeholder"]: ""})

        problem_setup_step.ui_placeholders = ui_data
        return problem_setup_step.analysis_locked
    else:
        return no_update


@callback(
    Output({"container": "placeholders", "placeholder": MATCH}, "value"),
    Input({"container": "placeholders", "placeholder": MATCH}, "value"),
    State({"container": "placeholders", "placeholder": MATCH}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_ui_placeholders(value, id, pathname):
    """This updates the dictionary of ui placeholders each time the ui data changes in the Placeholders section. If the value entered is None, "", or invalid, the last value entered in the component is returned."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    name = id["placeholder"]
    ui_data = problem_setup_step.ui_placeholders
    if value is None or value == "":
        if name.startswith("StartDesigns"):
            split_values = id["placeholder"].split("##")
            values = split_values[1:]
            rowId = values[0].split("#")[1]
            key = values[1].split("#")[1]
            last_value = ui_data["StartDesigns"][rowId][key]
        elif name.startswith("ParameterManager"):
            split_values = id["placeholder"].split("##")
            values=split_values[1:]
            pm_name = values[0].split("#")[0]
            key = values[0].split("#")[1]
            last_value = ui_data[pm_name][key]
        else:
            last_value = ui_data[name]
        return last_value
    else:

        if name.startswith("StartDesigns"):
            split_values = id["placeholder"].split("##")
            values = split_values[1:]
            rowId = values[0].split("#")[1]
            key = values[1].split("#")[1]
            ui_data["StartDesigns"][rowId][key] = value
        elif name.startswith("ParameterManager"):
            split_values = id["placeholder"].split("##")
            values=split_values[1:]
            pm_name = values[0].split("#")[0]
            key = values[0].split("#")[1]
            if isinstance(value, list) and True in value:
                value = True
            elif isinstance(value, list) and False in value:
                value = False
            ui_data[pm_name][key] = value
        elif "Bool" in name and type(value) == list:
            if True in value:
                value = True
            else:
                value = False
            ui_data.update({name: value})
        else:
            ui_data.update({name: value})
        problem_setup_step.ui_placeholders = ui_data
        while problem_setup_step.get_method_state("update_osl_placeholders_with_ui_values").status == MethodStatus.Running: # current workaround to avoid raising ConflictError: {"detail":"update_osl_placeholders_with_ui_values is already running"}
            time.sleep(0.1)
        problem_setup_step.update_osl_placeholders_with_ui_values()
        return no_update


@callback(
    Output({"type": "upload", "placeholder": MATCH}, "children"),
    Input({"type": "upload", "placeholder": MATCH}, "isCompleted"),
    State({"type": "upload", "placeholder": MATCH}, "fileNames"),
    State({"type": "upload", "placeholder": MATCH}, "upload_id"),
    State({"type": "upload", "placeholder": MATCH}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def upload_input_files_to_project_and_update_ui_placeholders(is_completed, filenames, upload_id, component_id, pathname):
    """This uploads an Input file to the project directory and updates the dictionary of ui placeholders every time
    the ui data changes in the Input files section."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    name = component_id["placeholder"]
    if is_completed and filenames and len(filenames):
        filename = filenames[0]
        filepath = os.path.join(problem_setup_step.upload_directory, upload_id, filename)
        file_data = open(filepath, mode="rb")

        project.upload_file(f"Problem_Setup/Input_Files/{filename}", file_data)
        ui_data = problem_setup_step.ui_placeholders
        ui_data.update({name: filename})
        problem_setup_step.ui_placeholders = ui_data

        return no_update
    else:
        raise PreventUpdate


@callback(
    Output("start_analysis", "disabled"),
    Input({"type": "upload", "placeholder": ALL}, "isCompleted"),
    State({"type": "upload", "placeholder": ALL}, "fileNames"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_status_of_start_analysis_button(is_completed, filenames, pathname):
    """This enables the start analysis button if a file has been uploaded for all input files."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    if all(filenames):
        problem_setup_step.analysis_locked = False
    else:
        problem_setup_step.analysis_locked = True
    if filenames == True:
        result = check_empty_strings(filenames)

    return problem_setup_step.analysis_locked


@callback(
    Output("dummy_button_2", "n_clicks"),
    Input("url", "pathname"),
    State("dummy_button_2", "n_clicks"),
)
def on_page_load_initialize_dictionary_of_ui_placeholder_values(pathname, n_clicks):
    return n_clicks + 1


@callback(
    Output("start-designs-view", "children"),
    Input({"type": "button-add", "index": ALL}, "n_clicks"),
    Input({"type": "button-del", "index": ALL}, "n_clicks"),
    State({"type": "button-del", "index": ALL}, "disabled"),
    State({"type": "row", "index": ALL}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_start_designs_table(n_clicks_add, n_clicks_del, disabled_states, row_id, pathname):
    """This updates the StartDesigns table every time the '+' or '-' button is clicked."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    ctx = callback_context
    triggered_button = ctx.triggered[0]["prop_id"].split(".")[0]
    if (
        ctx.triggered
        and not all(n_click is None for n_click in n_clicks_del)
        or not all(n_click is None for n_click in n_clicks_add)
    ):
        ui_data = problem_setup_step.ui_placeholders
        designs = ui_data["StartDesigns"]
        button_type = triggered_button.split('"type":"')[1].split('"}')[0]
        row_id = triggered_button.split('"index":')[1].split(",")[0]
        if button_type == "button-add":
            designs = add_row(designs, row_id)
        elif button_type == "button-del":
            designs = delete_row(designs, row_id)

        # Rebuild the dictionary with updated keys
        new_designs = {str(index): value for index, (_, value) in enumerate(designs.items(), start=1)}
        ui_data.update({"StartDesigns": new_designs})

        problem_setup_step.ui_placeholders = ui_data
        while problem_setup_step.get_method_state("update_osl_placeholders_with_ui_values").status == MethodStatus.Running: # current workaround to avoid raising ConflictError: {"detail":"update_osl_placeholders_with_ui_values is already running"}
            time.sleep(0.1)
        problem_setup_step.update_osl_placeholders_with_ui_values()

        return update_designs_to_dash_section(problem_setup_step.placeholders, problem_setup_step.project_locked)
    else:
        raise PreventUpdate


def add_row(designs, id_):
    new_value = designs[id_]  # Value from the target key
    new_designs = {}
    for key, value in designs.items():
        new_designs[key] = value
        if key == id_:
            new_designs["temp"] = new_value
    return new_designs


def delete_row(designs, id_):
    del designs[id_]
    return designs
