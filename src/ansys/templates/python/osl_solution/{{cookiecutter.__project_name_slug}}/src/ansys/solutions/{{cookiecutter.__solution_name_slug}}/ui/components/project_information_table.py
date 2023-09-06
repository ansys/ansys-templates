# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import json
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


class ProjectInformationTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ProjectInformationTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, monitoring_step: MonitoringStep, datatable_props: dict = None, interval_props: dict = None, aio_id: str = None):
        """ProjectInformationTableAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `monitoring_step` - The StepModel object of the monitoring step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        data = self.get_data(monitoring_step)

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

    def get_data(self, monitoring_step: MonitoringStep) -> pd.DataFrame:

        project_status_info = json.loads(monitoring_step.project_status_info_file.read_text())

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
