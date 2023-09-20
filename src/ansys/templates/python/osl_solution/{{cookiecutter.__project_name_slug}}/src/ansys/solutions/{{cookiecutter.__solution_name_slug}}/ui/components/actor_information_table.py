# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import plotly.express as px
import uuid

from dash_extensions.enrich import html, dcc


class ActorInformationTableAIO(html.Div):

    class ids:
        pie_chart = lambda aio_id: {
            'component': 'ActorStatisticsTableAIO',
            'subcomponent': 'pie_chart',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, data: dict, aio_id: str = None):
        """ActorInformationTableAIO is an All-in-One component that is composed
        of a `px.pie` component (plotly express pie chart) and additional components
        which are not exposed but only configured internally.

        - `data` - Data to be displayed in the table and pie chart components.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self._style: dict = {
            "textAlign": "left",
            "fontSize": 12,
            "fontFamily": "Roboto",
            "color": "rgba(0, 0, 0, 1)",
            "backgroundColor": "rgba(255, 255, 255, 0)"
        }

        table_data, pie_chart_data = self.to_dash(data)

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
            html.H5("Actor information", className="card-title"),
            html.Hr(className="my-2"),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    table_data,
                                    className="border-0 bg-transparent"
                                ),
                            ],
                            className="border-0 bg-transparent"
                        ),
                        width=8
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    dcc.Graph(id=self.ids.pie_chart(aio_id), **pie_chart_props) if pie_chart_data else None,
                                    className="border-0 bg-transparent"
                                ),
                            ],
                            className="border-0 bg-transparent"
                        ),
                        width=4
                    ),

                ]
            )
        ])

    def to_dash(self, data: dict) -> list:

        # Collect table data
        table_data = []
        for key, value in data.items():
            table_data.append(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Label(
                                key,
                                style = self._style
                            ),
                            width=2
                        ),
                        dbc.Col(
                            html.Label(
                                value,
                                style = self._style
                            ),
                            width=10
                        ),
                    ]
                )
            )

        # Collect pie chart data
        pie_chart_data = {}
        if "Processed" in data.keys():
            pie_chart_data = {'Category': ['Success', 'Failure', 'Pending'], 'Count': [0, 0, 0]}
            for index, state in enumerate(["Succeeded", "Not succeeded", "Pending"]):
                pie_chart_data["Count"][index] = data[state]

        return table_data, pie_chart_data
