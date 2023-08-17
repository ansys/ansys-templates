# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid
import pandas as pd

from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import convert_microseconds


class ActorStatisticsTableAIO(html.Div): 

    class ids:
        interval = lambda aio_id: {
            'component': 'ActorStatisticsTableAIO',
            'subcomponent': 'interval',
            'aio_id': aio_id
        }
        datatable = lambda aio_id: {
            'component': 'ActorStatisticsTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, datatable_props: dict = None, interval_props: dict = None, aio_id: str = None):
        """ActorStatisticsTableAIO is an All-in-One component that is composed
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
            dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
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

    def get_data(actor_info: dict) -> pd.DataFrame:

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

    @callback(
        Output(ids.datatable(MATCH), 'data'),
        Output(ids.datatable(MATCH), 'columns'),
        Input(ids.interval(MATCH), 'n_intervals'),
        State("url", "pathname"),
    )
    def auto_update(n_intervals, pathname):

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step

        if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
            actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
        else:
            actor_info = {}
               
        data = ActorStatisticsTableAIO.get_data(actor_info)

        return data.to_dict('records'), [{"name": i, "id": i, "type": "text"} for i in data.columns]
