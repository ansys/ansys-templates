# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import json
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table
from datetime import datetime

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import (
    remove_key_from_dictionaries,
    sort_dict_by_ordered_keys,
)


class ActorLogsTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ActorLogsTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, monitoring_step: MonitoringStep, aio_id: str = None):
        """ActorLogsTableAIO is an All-in-One component that is composed
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
            "style_header": {"font_family": "Roboto", "font_size": "15px", "fontWeight": "bold"},
            "style_cell": {
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": "15px",
            },
            "style_cell_conditional": [
                {"if": {"column_id": "Time"}, "minWidth": "60px", "maxWidth": "60px", "width": "60px"},
                {
                    "if": {"column_id": "Level"},
                    "minWidth": "30px",
                    "maxWidth": "30px",
                    "width": "30px",
                    "textAlign": "center",
                },
                {"if": {"column_id": "Message"}, "minWidth": "200px", "maxWidth": "200px", "width": "200px"},
            ],
            "style_data_conditional": [
                {
                    "if": {"column_id": "Level", "filter_query": '{Level} eq "INFO"'},
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
                            html.H4("Actor Log", className="card-title"),
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

        has_data = False

        if actor_info:
            if "log_messages" in actor_info.keys():
                if len(actor_info["log_messages"]):
                    has_data = True
                    # Remove hid key from list dictionaries because it is useless for UI
                    # and prevent transformation to DataFrame.
                    actor_logs_data = remove_key_from_dictionaries(actor_info["log_messages"], "hid")
                    # Transform list of dictionaries into dictionary
                    actor_logs_data = {
                        key: [d[key] for d in actor_info["log_messages"]]
                        for key in actor_info["log_messages"][0]
                    }
                    # Sort keys in order
                    actor_logs_data = sort_dict_by_ordered_keys(actor_logs_data, ["time_stamp", "level", "message"])
                    # Rename keys
                    actor_logs_data["Time"] = actor_logs_data.pop("time_stamp")
                    actor_logs_data["Level"] = actor_logs_data.pop("level")
                    actor_logs_data["Message"] = actor_logs_data.pop("message")
                    # Convert timestamp
                    for index, value in enumerate(actor_logs_data["Time"]):
                        dt = datetime.strptime(value, "%Y%m%dT%H%M%S.%f")
                        actor_logs_data["Time"][index] = dt.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]

        if not has_data:
            actor_logs_data = {"Time": [], "Level": [], "Message": []}

        return pd.DataFrame(actor_logs_data)
