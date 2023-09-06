# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import json
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import convert_microseconds


class ActorStatisticsTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ActorStatisticsTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, monitoring_step: MonitoringStep, aio_id: str = None):
        """ActorStatisticsTableAIO is an All-in-One component that is composed
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
            },
            "style_cell": {
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": "15px",
            },
            "style_cell_conditional": [
                {"if": {"column_id": "row_names"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
                {"if": {"column_id": "Current Run"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
                {"if": {"column_id": "All Runs"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
            ],
            "style_data_conditional": [
                {
                    "if": {"column_id": "row_names", "filter_query": '{Level} eq "std_dev"'},
                    "backgroundColor": "rgb(227, 245, 252)",
                    "color": "rgb(0, 0, 0)",
                    "textAlign": "center",
                }
            ],
            "style_as_list_view": True,
        }

        super().__init__([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Actor Statistics", className="card-title"),
                            dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                        ]
                    ),
                ],
                color="warning",
                outline=True,
            )
        ])

    def get_data(self, monitoring_step: MonitoringStep) -> pd.DataFrame:

        actors_info = json.loads(monitoring_step.actors_info_file.read_text())

        if monitoring_step.selected_actor_from_treeview in actors_info.keys():
            actor_info = actors_info[monitoring_step.selected_actor_from_treeview]
        else:
            actor_info = {}

        actor_statistics_data = {
            "row_names": ["Usages", "Accumulated", "Minimum", "Maximum", "Mean", "std_dev"],
            "Current Run": [None, None, None, None, None, None],
            "All Runs": [None, None, None, None, None, None],
        }

        if actor_info:
            for column_name in ["Current Run", "All Runs"]:
                key = column_name.split()[0].lower()
                actor_statistics_data[column_name][0] = actor_info["usage_stats"][key]["num_usages"]
                for index, row_name in enumerate(actor_statistics_data["row_names"]):
                    if row_name != "Usages":
                        duration = actor_info["usage_stats"][key]["exec_duration_us"][row_name.lower()]
                        duration = convert_microseconds(duration)
                        actor_statistics_data[column_name][index] = duration

        return pd.DataFrame(actor_statistics_data)
