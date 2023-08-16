# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid
import pandas as pd

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}


class ProjectInformationTableAIO(html.Div): 

    class ids:
        interval = lambda aio_id: {
            'component': 'ProjectInformationTableAIO',
            'subcomponent': 'interval',
            'aio_id': aio_id
        }
        datatable = lambda aio_id: {
            'component': 'ProjectInformationTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, datatable_props: dict = None, interval_props: dict = None, aio_id: str = None):
        """ProjectInformationTableAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.
        
        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        if interval_props:
            interval_props = interval_props.copy()
        else:
            interval_props = {
                "interval": problem_setup_step.auto_update_frequency,
                "n_intervals": 0,
                "disabled": not problem_setup_step.auto_update_activated
            }

        if datatable_props:
            datatable_props = datatable_props.copy()
        else:
            datatable_props = {
                "fixed_rows": {"headers": True},
                "style_header": {
                    "textAlign": "left",
                    "font_family": "Roboto",
                    "font_size": "15px",
                    "fontWeight": "bold",
                    "border": "none",
                    "display": "none",
                },
                "style_cell": {
                    "textAlign": "left",
                    "font_family": "Roboto",
                    "font_size": "15px",
                    "border": "none"
                },
                "style_as_list_view": True,
                "style_table": {"border": "none"}, # Hide table borders
            }

        super().__init__([ 
            dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Project information", className="card-title"),
                            dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                        ]
                    ),
                ],
                color="warning",
                outline=True,
            )
        ])

    def get_data(project_status_info: dict) -> pd.DataFrame:

        project_summary_data = {
            "column_a": [
                "State",
                "Id",
                "Name",
                "Machine",
                "Location",
                "Project directory",
                "Owner",
                "Registered",
                "Lock info",
            ],
            "column_b": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        }

        if project_status_info:
            project_summary_data["column_b"] = [
                project_status_info["projects"][0]["state"],
                project_status_info["projects"][0]["project_id"],
                project_status_info["projects"][0]["name"],
                project_status_info["projects"][0]["machine"],
                project_status_info["projects"][0]["location"],
                project_status_info["projects"][0]["working_dir"],
                project_status_info["projects"][0]["user"],
                "",
                "",
            ]

        return pd.DataFrame(project_summary_data)

    @callback(
        Output(ids.datatable(MATCH), 'data'),
        Output(ids.datatable(MATCH), 'columns'),
        Input(ids.interval(MATCH), 'n_intervals'),
        State("url", "pathname"),
    )
    def auto_update(n_intervals, pathname):

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step
        
        data = ProjectInformationTableAIO.get_data(problem_setup_step.project_status_info)

        return data.to_dict('records'), [{"name": i, "id": i, "type": "text"} for i in data.columns]
