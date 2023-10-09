# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import pandas as pd
import uuid

from dash_extensions.enrich import html, Output, Input, State, dash_table, callback, MATCH
from typing import Union


class CollapsibleTableAIO(html.Div):

    class ids:
        button = lambda aio_id: {
            "component": "CollapsibleTableAIO",
            "subcomponent": "button",
            "aio_id": aio_id
        }
        table = lambda aio_id: {
            "component": "CollapsibleTableAIO",
            "subcomponent": "table",
            "aio_id": aio_id
        }
        collapse = lambda aio_id: {
            "component": "CollapsibleTableAIO",
            "subcomponent": "collapse",
            "aio_id": aio_id
        }

    ids = ids

    def __init__(self, data: Union[dict, list] = None, button_props: dict = None, table_props: dict = None, aio_id=None):
        """CollapsibleTableAIO is an All-in-One component that is composed of the following components:
        - `dbc.Button`
        - `dbc.Collapse`
        - `dash_table.DataTable`

        When the button is clicked a table is displayed. If the button is clicked again the table is hidden.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        button_props_default = {
            "n_clicks": 0,
            "size": "sm",
            "style": {
                "background-color": "rgba(242, 242, 242, 0.6)",
                "borderColor": "rgba(242, 242, 242, 0.6)",
                "color": "rgba(0, 0, 0, 1)"
            }
        }

        if button_props:
            button_props = button_props.copy()
        for key, value in button_props_default.items():
            if key not in button_props:
                button_props[key] = value

        data = self._reshape_data(data)

        if not table_props:
            table_props = {
                "data": data.to_dict("records"),
                "columns": [{"name": i, "id": i, "type": "text"} for i in data.columns],
                "fixed_rows": {"headers": True},
                "style_header": {
                    "textAlign": "left",
                    "font_family": "Roboto",
                    "font_size": "15px",
                    "fontWeight": "bold",
                    "display": "none",
                },
                "style_cell": {
                    "textAlign": "left",
                    "font_family": "Roboto",
                    "font_size": "15px",
                },
                "style_data_conditional": [
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(242, 242, 242)",
                    },
                    {
                        "if": {"row_index": "even"},
                        "backgroundColor": "rgb(255, 255, 255)",
                    },
                ],
                "style_as_list_view": True,
            }

        super().__init__([
            html.Div(
                [
                    dbc.Button(id=self.ids.button(aio_id), **button_props),
                    dbc.Collapse(
                        id=self.ids.collapse(aio_id),
                        is_open=False,
                        children=dash_table.DataTable(id=self.ids.table(aio_id), **table_props)
                    ),
                ]
            ),
        ])

    def _reshape_data(self, data: Union[dict, list]) -> pd.DataFrame:
        """Transform input data into DataFrame."""

        if isinstance(data, dict):
            pass
        elif not any(isinstance(i, list) for i in data):
            # This is a non-nested list.
            data = {"column_a": data}
        else:
            raise ValueError("Unprocessable data. Expect a non-nested list or a dictionary.")

        return pd.DataFrame(data)

    @callback(
        Output(ids.collapse(MATCH), "is_open"),
        Input(ids.button(MATCH), "n_clicks"),
        State(ids.collapse(MATCH), "is_open"),
    )
    def toggle_collapse(n_clicks, is_open):
        """Collapse/Expand callback."""
        if n_clicks:
            return not is_open
        return is_open
