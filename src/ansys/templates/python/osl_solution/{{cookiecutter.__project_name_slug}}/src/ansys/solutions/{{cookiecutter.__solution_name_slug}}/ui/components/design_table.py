# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import sorted_nicely


class DesignTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'DesignTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, data: dict, aio_id: str = None):
        """DesignTableAIO is an All-in-One component that is composed
        of a `dash_table.DataTable` component.

        - `data` - Data to be displayed in the datatable component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        data = self.transform_data(data)

        datatable_props = {
            "data": data.to_dict('records'),
            "columns": [{"name": i, "id": i, "type": "text"} for i in data.columns],
            "editable": True, # user can select and copy data
            "fixed_rows": {"data": 0},
            "fixed_columns": {"data": 0},
            "style_header": {
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": "15px",
                "fontWeight": "bold",
            },
            "style_data_conditional":
            [
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
            "style_cell": {
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": "15px",
                "overflowX": "scroll", # Scroll through overflow
                "maxWidth": 1,
            },
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


    def transform_data(self, data: dict) -> pd.DataFrame:

        data = pd.DataFrame(data)

        if len(data["Design"]):

            # OptiSLang returns the designs in an unsorted way.
            # The following method organizes the rows in ascending order.
            data = data.loc[self.sort_designs(data["Design"].to_list())]

            for col, dtype in data.dtypes.items():
                if dtype == "bool":
                    data[col] = data[col].astype("str")
                elif dtype == "object":
                    data[col] = data[col].astype("str")

            data = data.round(6)

        return data
