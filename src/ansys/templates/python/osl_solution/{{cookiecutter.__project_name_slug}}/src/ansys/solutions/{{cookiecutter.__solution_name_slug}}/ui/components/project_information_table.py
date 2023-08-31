# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dash_table
import uuid
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}


class ProjectInformationTableAIO(html.Div):

    class ids:
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

        data = self.get_data(problem_setup_step)

        datatable_props = {
            "data": data.to_dict('records'),
            "columns": [{"name": i, "id": i, "type": "text"} for i in data.columns],
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

    def get_data(self, problem_setup_step) -> pd.DataFrame:

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

        if problem_setup_step.project_status_info:
            project_summary_data["column_b"] = [
                problem_setup_step.project_status_info["projects"][0]["state"],
                problem_setup_step.project_status_info["projects"][0]["project_id"],
                problem_setup_step.project_status_info["projects"][0]["name"],
                problem_setup_step.project_status_info["projects"][0]["machine"],
                problem_setup_step.project_status_info["projects"][0]["location"],
                problem_setup_step.project_status_info["projects"][0]["working_dir"],
                problem_setup_step.project_status_info["projects"][0]["user"],
                "",
                "",
            ]

        return pd.DataFrame(project_summary_data)
