# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the first step."""

import dash_bootstrap_components as dbc

from ansys.saf.glow.client.dashclient import DashClient
from dash_extensions.enrich import Input, Output, State, callback, dcc, html
from ansys.solutions.dash_components.table import InputRow
from ansys.solutions.optislang.frontend_components.placeholder_table import PlaceholderTable


from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


def layout(problem_setup_step: ProblemSetupStep):
    """Layout of the problem setup step UI."""

    # Upload placeholders and assets to project directory
    if problem_setup_step.placeholder_values == {}:
        problem_setup_step.upload_project_file_to_project_directory()
        problem_setup_step.upload_properties_file_to_project_directory()
        problem_setup_step.get_default_placeholder_values()
    
    placeholder_table = PlaceholderTable(problem_setup_step.placeholder_values, problem_setup_step.placeholder_definitions)

    # Placeholder card for displaying parameters defined in the <project_name>.json
    placeholder_card = dbc.Card(
        [
            dbc.CardBody(
                [
                dbc.Accordion(
                    [   
                        dbc.AccordionItem(
                            [
                                html.Div(placeholder_table.create()),
                            ],
                            
                            title="Placeholders",
                            item_id="parameter-placeholders",
                        )
                    ]
                )
            ]
            )
        ]            
    )
    return html.Div(
        [   
            html.H1("Optislang Project Name", className="display-3", style={"font-size": "35px"}),
            html.P(
                "An optiSLang web application for the optimization of a steel hook.", # Example of DESCRIPTION_TEXT from load_wizard.py
                className="lead",
                style={"font-size": "20px"},
            ),
            html.Hr(className="my-2"),
            html.Br(),
            dbc.Row(
                [
                    # dbc.Row(image_card), 
                    dbc.Row(placeholder_card),
                ],
                style={"padding": "20px"},
            ),
            dbc.Row(
                [
                    dbc.Accordion(
                        [   
                            dbc.AccordionItem(
                                [
                                    InputRow(
                                        "input",
                                        "project_name_input",
                                        "Project settings",
                                        row_default_value=None,
                                        row_description="Enter a project name.",
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                    ).get(),
                                    html.Br(),
                                    InputRow(
                                        "button",
                                        "start_analysis",
                                        "Start analysis",
                                        disabled=False,
                                        label_width=2,
                                        value_width=4,
                                        unit_width=1,
                                        description_width=4,
                                        class_name="button",
                                    ).get(),
                                    dcc.Loading(
                                        id="optislang_wait_spinner",
                                        type="circle",
                                        fullscreen=True,
                                        color="#ffb71b",
                                        style={
                                            "background-color": "rgba(55, 58, 54, 0.1)",
                                        },
                                        children=html.Div(id="wait_optislang_process"),
                                    ),
                                    dcc.Interval(
                                        id="solve-interval-component",
                                        interval=1 * 6000,  # in milliseconds
                                        n_intervals=0,
                                    ),
                                ],
                                title="Start Analysis",
                                item_id="start-analysis-accordion",
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


