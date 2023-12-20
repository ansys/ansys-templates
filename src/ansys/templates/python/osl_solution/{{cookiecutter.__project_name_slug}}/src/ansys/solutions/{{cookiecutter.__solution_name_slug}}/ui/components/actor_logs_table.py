# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import pandas as pd
import uuid

from dash_extensions.enrich import html, dash_table


class ActorLogsTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ActorLogsTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, data: dict, store_value: int= None, aio_id: str = None):
        """ActorLogsTableAIO is an All-in-One component that is composed
        of a `dash_table.DataTable` component.

        - `data` - Data to be displayed in the datatable component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        data = pd.DataFrame(data)

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
            "style_as_list_view": True,
            "page_current": store_value
        }

        super().__init__([
            html.H5("Actor Log", className="card-title"),
            html.Hr(className="my-2"),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                        ],
                        className="border-0 bg-transparent"
                    ),
                ],
                className="border-0 bg-transparent"
            )
        ])
