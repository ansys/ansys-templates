# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import uuid

from dash_extensions.enrich import html, dcc


class SystemFilesAIO(html.Div):

    class ids:
        button_omdb = lambda aio_id: {
            'component': 'SystemFilesAIO',
            'subcomponent': 'button_omdb',
            'aio_id': aio_id
        }
        button_csv = lambda aio_id: {
            'component': 'SystemFilesAIO',
            'subcomponent': 'button_csv',
            'aio_id': aio_id
        }
        download_omdb = lambda aio_id: {
            'component': 'SystemFilesAIO',
            'subcomponent': 'download_omdb',
            'aio_id': aio_id
        }
        download_csv = lambda aio_id: {
            'component': 'SystemFilesAIO',
            'subcomponent': 'download_csv',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, data: dict, aio_id: str = None):
        """SystemFilesAIO is an All-in-One component that is composed
        of multiple components which are not exposed but only configured internally.

        - `data` - Data to be displayed.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        button_props = {}
        download_props = {}

        super().__init__([
            html.H5("System Files", className="card-title"),
            html.Hr(className="my-2"),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Stack(
                                [
                                    html.Div(
                                        [
                                            dbc.Button(
                                                children="Download OMDB",
                                                id=self.ids.button_omdb(aio_id),
                                                **button_props
                                            ),
                                            dcc.Download(id=self.ids.download_omdb(aio_id), **download_props),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                children="Download CSV",
                                                id=self.ids.button_csv(aio_id),
                                                **button_props
                                            ),
                                            dcc.Download(id=self.ids.download_csv(aio_id), **download_props),
                                        ]
                                    ),
                                ],
                                direction="horizontal",
                                gap=3,
                            )
                        ]
                    )
                ],
                className="border-0 bg-transparent"
            )
        ])
