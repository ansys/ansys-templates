# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import json
import pandas as pd
import plotly.express as px
import uuid

from dash_extensions.enrich import html, dash_table, dcc

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


class ActorInformationTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ActorInformationTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }
        pie_chart = lambda aio_id: {
            'component': 'ActorStatisticsTableAIO',
            'subcomponent': 'pie_chart',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, monitoring_step: MonitoringStep, aio_id: str = None):
        """ActorInformationTableAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `monitoring_step` - The StepModel object of the monitoring step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        table_data, pie_chart_data = self.get_data(monitoring_step)

        datatable_props = {
            "data": table_data.to_dict('records'),
            "columns": [{"name": i, "id": i, "type": "text"} for i in table_data.columns],
            "fixed_rows": {"headers": True},
            "style_header": {
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": "15px",
                "fontWeight": "bold",
                "border": "none",
                "display": "none",
            },
            "style_cell": {"textAlign": "left", "font_family": "Roboto", "font_size": "15px", "border": "none"},
            "style_as_list_view": True,
            "style_table": {"border": "none"},  # Hide table borders
        }

        if pie_chart_data:
            pie_chart_props = {
                "figure": px.pie(
                    pie_chart_data,
                    values='Count',
                    names='Category',
                    color='Category',
                    color_discrete_map={
                        'Success': 'rgba(173, 191, 11, 1)',
                        'Failure': 'rgba(248, 105, 80, 1)',
                        'Pending': 'rgba(251, 201, 93, 1)'
                    },
                ).update_traces(textinfo='none', hole=0.8, showlegend=True),
                "style": {
                    "width": "300px",
                    "height": "300px",
                    "display": "inline-block",
                },
            }

        super().__init__([
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4("Actor information", className="card-title"),
                                    dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                                ],
                                width=8
                            ),
                            dbc.Col(
                                [
                                    dcc.Graph(id=self.ids.pie_chart(aio_id), **pie_chart_props) if pie_chart_data else None,
                                ],
                                width=2
                            ),
                        ]
                    )
                ],
                color="warning",
                outline=True,
            )
        ])

    def get_data(self, monitoring_step: MonitoringStep) -> pd.DataFrame:

        actors_info = json.loads(monitoring_step.actors_info_file.read_text())
        actors_status_info = json.loads(monitoring_step.actors_status_info_file.read_text())

        if monitoring_step.selected_actor_from_treeview in actors_info.keys():
            actor_info = actors_info[monitoring_step.selected_actor_from_treeview]
        else:
            actor_info = {}

        if monitoring_step.selected_actor_from_treeview in actors_status_info.keys():
            actor_status_info = actors_status_info[monitoring_step.selected_actor_from_treeview][0]
        else:
            actor_status_info = {}

        actor_information_data = {
            "column_a": ["Working directory", "Processing state", "Execution duration"],
            "column_b": [None, None, None],
        }

        pie_chart_data = None

        if actor_info and actor_status_info:
            actor_information_data["column_b"] = [
                actor_status_info["working dir"],
                actor_status_info["state"],
                "-",
            ]
            if actor_info["kind"] == "system":
                succeeded_designs = actor_status_info["succeeded_designs"]
                failed_designs = actor_status_info["failed_designs"]
                pending_designs = actor_status_info["pending_designs"]
                total_designs = actor_status_info["total_designs"]
                processed_designs = total_designs - pending_designs
                status = int(processed_designs / total_designs * 100)
                actor_information_data["column_a"].extend(["Processed", "Status", "Succeeded", "Not succeeded"])
                actor_information_data["column_b"].extend(
                    [f"{processed_designs} / {total_designs}", f"{status}%", succeeded_designs, failed_designs]
                )

                pie_chart_data = {'Category': ['Success', 'Failure', 'Pending'], 'Count': [0, 0, 0]}
                for index, state in enumerate(["succeeded_designs", "failed_designs", "pending_designs"]):
                    pie_chart_data["Count"][index] = actor_status_info[state]

        return pd.DataFrame(actor_information_data), pie_chart_data
