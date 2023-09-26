# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import json
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import sorted_nicely


class DesignTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'DesignTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, monitoring_step: MonitoringStep, aio_id: str = None):
        """DesignTableAIO is an All-in-One component that is composed
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
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": "15px",
                "fontWeight": "bold",
            },
            "style_cell": {
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": "15px",
                "whiteSpace": "normal",
            },
            "style_data_conditional": [
                {
                    "if": {"column_id": "Status", "filter_query": '{Status} eq "Succeeded"'},
                    "backgroundColor": "rgb(223, 240, 208)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Status", "filter_query": '{Status} eq "Not succeeded"'},
                    "backgroundColor": "rgb(254, 221, 215)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Feasible", "filter_query": '{Feasible} eq "True"'},
                    "backgroundColor": "rgb(223, 240, 208)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Feasible", "filter_query": '{Feasible} eq "False"'},
                    "backgroundColor": "rgb(254, 221, 215)",
                    "color": "rgb(0, 0, 0)",
                },
            ],
            "style_as_list_view": True,
        }

        super().__init__([
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                        width=12
                    ),
                ]
            )
        ])

    def sort_designs(self, designs: list) -> list:

        sorted_designs = sorted_nicely(designs)
        return [designs.index(design) for design in sorted_designs]

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

        design_table_data = {
            "Design": [],
            "Feasible": [],
            "Status": [],
            "Pareto": [],
        }

        field_types = ["parameter", "constraint", "objective", "response"]

        if actor_info:
            if actor_info["kind"] == "system":
                for field_type in field_types:
                    field_name_index = field_type + "_names"
                    for field_name in actor_status_info["designs"][field_name_index]:
                        design_table_data[field_name] = []
                design_numbers = []
                for design_values in reversed(actor_status_info["designs"]["values"]):
                    design_numbers.append(design_values["hid"].split(".")[-1])
                    design_table_data["Design"].append(design_values["hid"])
                    for field_type in field_types:
                        field_name_index = field_type + "_names"
                        field_value_index = field_type + "_values"
                        field_names = actor_status_info["designs"][field_name_index]
                        field_values = design_values[field_value_index]
                        if len(field_names) != len(field_values):
                            field_values = [None for i in range(len(field_names))]
                        for field_name, field_value in zip(field_names, field_values):
                            if isinstance(field_value, dict):
                                if field_value["type"] == "xy_data":
                                    field_value = f"[1:%s]" % (field_value["num_entries"])
                            design_table_data[field_name].append(field_value)
                for design_status in reversed(actor_status_info["design_status"]):
                    design_table_data["Feasible"].append(design_status["feasible"])
                    design_table_data["Status"].append(design_status["status"])
                    design_table_data["Pareto"].append(design_status["pareto_design"])

                design_table_data = pd.DataFrame(design_table_data)

                # OptiSLang returns the designs in an unsorted way.
                # The following method organizes the rows in ascending order.
                design_table_data = design_table_data.loc[self.sort_designs(design_table_data["Design"].to_list())]

                for col, dtype in design_table_data.dtypes.items():
                    if dtype == "bool":
                        design_table_data[col] = design_table_data[col].astype("str")

                design_table_data = design_table_data.round(6)

        return pd.DataFrame(design_table_data)
