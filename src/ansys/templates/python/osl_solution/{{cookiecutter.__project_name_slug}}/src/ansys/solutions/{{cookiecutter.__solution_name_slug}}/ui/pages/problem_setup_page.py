# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the problem setup step."""

import os
import time
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
from ansys.saf.glow.solution import MethodStatus
from dash_extensions.enrich import Input, Output, State, dcc, html, callback, ALL, MATCH, no_update
from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.dash_components.table import InputRow
from ansys.solutions.optislang.frontend_components.load_sections import to_dash_sections

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.alerts import update_alerts


def layout(problem_setup_step: ProblemSetupStep) -> html.Div:
    """Layout of the problem setup step."""

    # Upload placeholders and assets
    if problem_setup_step.placeholders == {}:
        problem_setup_step.get_default_placeholder_values()
    project_properties_sections = to_dash_sections(problem_setup_step.placeholders, problem_setup_step.registered_files)

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
                [
                    dbc.Col(
                        [
                            dbc.Stack(
                                update_alerts(problem_setup_step),
                                id="alert_messages",
                                direction="horizontal",
                                gap=3,
                            ),
                        ],
                        width=12,
                    )
                ]
            ),
            html.Br(),
            # Input form
            dbc.Row(id="osl-dash-sections",children=project_properties_sections),
            dbc.Row(
                [
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    # InputRow(
                                    #     "button",
                                    #     "check_ansys_ecosystem",
                                    #     "Check Ansys ecosystem",
                                    #     disabled=False,
                                    #     label_width=2,
                                    #     value_width=4,
                                    #     unit_width=1,
                                    #     description_width=4,
                                    #     class_name="button",
                                    # ).get(),
                                    # dcc.Loading(
                                    #     type="circle",
                                    #     fullscreen=True,
                                    #     color="#ffb71b",
                                    #     style={
                                    #         "background-color": "rgba(55, 58, 54, 0.1)",
                                    #     },
                                    #     children=html.Div(id="wait_ecosystem_ckeck"),
                                    # ),
                                    # html.Br(),
                                    InputRow(
                                        "button",
                                        "start_analysis",
                                        "Start analysis",
                                        disabled=problem_setup_step.analysis_locked,
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                        class_name="button",
                                    ).get(),
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
                                ],
                                title="Start Analysis",
                                item_id="start_analysis_accordion",
                            ),
                            dbc.Button(
                                id="dummy_button_2",
                                style={"display": "none"},
                                n_clicks=0,
                                color="dark"
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


for alert in ["optislang_version", "optislang_solve"]:

    @callback(
        Output(f"popover_{alert}", "is_open"),
        [Input(f"popover_{alert}_target", "n_clicks")],
        [State(f"popover_{alert}", "is_open")],
    )
    def toggle_popover(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open


# @callback(
#     Output("alert_messages", "children"),
#     Output("wait_ecosystem_ckeck", "children"),
#     Output("start_analysis", "disabled"),
#     Input("check_ansys_ecosystem", "n_clicks"),
#     State("url", "pathname"),
#     prevent_initial_call=True,
# )
# def check_ansys_ecosystem(n_clicks, pathname):
#     """Start optiSLang and run the simulation. Wait for the process to complete."""

#     project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
#     problem_setup_step = project.steps.problem_setup_step

#     if n_clicks:
#         problem_setup_step.check_ansys_ecosystem()
#         return update_alerts(problem_setup_step), True, False if problem_setup_step.ansys_ecosystem_ready else True
#     else:
#         raise PreventUpdate


@callback(
    Output("alert_messages", "children"),
    Output("wait_start_analysis", "children"),
    Output("start_analysis", "disabled"),
    Input("start_analysis", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def start_analysis(n_clicks, pathname):
    """Start optiSLang and run the simulation. Wait for the process to complete."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if n_clicks:
        ui_data=problem_setup_step.ui_placeholders
        ui_data.update({"start_analysis_requested": True})
        problem_setup_step.ui_placeholders=ui_data
        # Update project properties file prior to the solve
        problem_setup_step.write_updated_properties_file()
        # Start analysis
        problem_setup_step.start_analysis()
        # Lock start analysis
        problem_setup_step.analysis_locked = True
        # Wait until the analysis effectively starts
        while problem_setup_step.optislang_solve_status == "initial":
            time.sleep(1)
        return update_alerts(problem_setup_step), True, True
    else:
        raise PreventUpdate


@callback(
    Output("alert_messages", "children"),
    Output("start_analysis", "disabled"),
    Input("solve_interval_component", "n_intervals"),
    Input("start_analysis", "n_clicks"),
    State("url", "pathname"),
)
def update_alert_messages(n_intervals, n_clicks, pathname):
    """Display status badges."""

    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.ansys_ecosystem_ready:
        status = problem_setup_step.get_long_running_method_state("start_analysis").status
        if status == MethodStatus.Running:
            problem_setup_step.analysis_running = True
            problem_setup_step.analysis_locked = True
        return update_alerts(problem_setup_step), problem_setup_step.analysis_locked
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
        ui_data=problem_setup_step.ui_placeholders
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
            elif "ParameterManager" in ids[index]["placeholder"]:
                split_values = ids[index]["placeholder"].split("#")
                pm_name = split_values[0]
                key = split_values[1]
                parameters[key] = data[index]
                ui_data.update({pm_name:parameters})
            elif "Bool" in ids[index]["placeholder"] and type(data[index])==list:
                value=data[index]
                if True in value:
                    new_value = True
                else:
                    new_value = False
                ui_data.update({ids[index]["placeholder"]: new_value})
            else:
                ui_data.update({ids[index]["placeholder"]:data[index]})
            ui_data.update({"StartDesigns":designs})
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
    Output({"container": "placeholders", "placeholder": MATCH}, "id"),
    Input({"container": "placeholders", "placeholder": MATCH}, "value"),
    State({"container": "placeholders", "placeholder": MATCH}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_ui_placeholders(value, id, pathname):
    """This updates the dictionary of ui placeholders each time the ui data changes in the Placeholders section"""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    name=id["placeholder"]
    ui_data=problem_setup_step.ui_placeholders
    if name.startswith("StartDesigns"):
        split_values = id["placeholder"].split("##")
        values = split_values[1:]
        rowId = values[0].split("#")[1]
        key = values[1].split("#")[1]
        ui_data["StartDesigns"][rowId][key]=value
    elif "ParameterManager" in name:
        split_values = id["placeholder"].split("#")
        pm_name = split_values[0]
        key = split_values[1]
        ui_data[pm_name][key]=value
    elif "Bool" in name and type(value)==list:
        if True in value:
            value = True
        else:
            value = False
        ui_data.update({name: value})
    else:
        ui_data.update({name: value})
    problem_setup_step.ui_placeholders=ui_data
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
def upload(is_completed, filenames, upload_id, component_id, pathname):
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
        ui_data=problem_setup_step.ui_placeholders
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


def check_empty_strings(lst):
    for sublist in lst:
        for item in sublist:
            if not item.strip():  # Using strip() to remove leading/trailing whitespaces
                return False
    return True