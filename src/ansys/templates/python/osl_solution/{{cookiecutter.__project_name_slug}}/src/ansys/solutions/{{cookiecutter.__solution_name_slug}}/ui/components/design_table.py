# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid
import pandas as pd

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import sorted_nicely


class DesignTableAIO(html.Div): 

    class ids:
        interval = lambda aio_id: {
            'component': 'DesignTableAIO',
            'subcomponent': 'interval',
            'aio_id': aio_id
        }
        datatable = lambda aio_id: {
            'component': 'DesignTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, datatable_props: dict = None, interval_props: dict = None, aio_id: str = None):
        """DesignTableAIO is an All-in-One component that is composed
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
            dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
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

    def sort_designs(designs: list) -> list:

        sorted_designs = sorted_nicely(designs)
        return [designs.index(design) for design in sorted_designs]

    def get_data(actor_info: dict, actor_status_info: dict) -> pd.DataFrame:

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
                design_table_data = design_table_data.loc[DesignTableAIO.sort_designs(design_table_data["Design"].to_list())]

                for col, dtype in design_table_data.dtypes.items():
                    if dtype == "bool":
                        design_table_data[col] = design_table_data[col].astype("str")

                design_table_data = design_table_data.round(6)

        return pd.DataFrame(design_table_data)

    @callback(
        Output(ids.datatable(MATCH), 'data'),
        Output(ids.datatable(MATCH), 'columns'),
        Input(ids.interval(MATCH), 'n_intervals'),
        State("url", "pathname"),
    )
    def auto_update(n_intervals, pathname):

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step
        
        actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
        actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]

        data = DesignTableAIO.get_data(actor_info, actor_status_info)

        return data.to_dict('records'), [{"name": i, "id": i, "type": "text"} for i in data.columns]
