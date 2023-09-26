# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import uuid

from dash_extensions.enrich import html, dcc

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import (
    remove_key_from_dictionaries,
    sort_dict_by_ordered_keys,
)


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

    def __init__(self, monitoring_step: MonitoringStep, aio_id: str = None):
        """SystemFilesAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `monitoring_step` - The StepModel object of the monitoring step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        button_props = {}
        download_props = {}

        super().__init__([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("System Files", className="card-title"),
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
                color="warning",
                outline=True,
            )
        ])
