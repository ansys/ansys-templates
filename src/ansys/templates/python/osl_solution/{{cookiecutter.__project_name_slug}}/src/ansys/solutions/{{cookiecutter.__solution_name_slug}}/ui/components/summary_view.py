# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the summary view for system and actor node types."""

from dash import dash_table
import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_information_table import ActorInformationTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_logs_table import ActorLogsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.actor_statistics_table import ActorStatisticsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.system_files import SystemFiles


class SummaryView:
    """Summary view component."""

    def __init__(self) -> None:
        """Constructor."""

        self.actor_info: dict = None
        self.actor_status_info: dict = None
        self.result_files: dict = None
        self.font_size: str = "15px"

    def _get_actor_information_table(self) -> dash_table.DataTable:

        table = ActorInformationTable()

        if self.actor_info:
            table.actor_info = self.actor_info
        if self.actor_status_info:
            table.actor_status_info = self.actor_status_info

        return table.render()

    def _get_system_files(self) -> html.Div:

        system_files = SystemFiles()

        if self.actor_info:
            system_files.node_name = self.actor_info["name"]
        if self.result_files:
            system_files.omdb_file = self.result_files["omdb"]

        return system_files.render()

    def _get_actor_logs_table(self) -> dash_table.DataTable:

        table = ActorLogsTable()

        if self.actor_info:
            table.actor_info = self.actor_info

        return table.render()

    def _get_actor_statistics_table(self) -> dash_table.DataTable:

        table = ActorStatisticsTable()

        if self.actor_info:
            table.actor_info = self.actor_info

        return table.render()

    def render(self):
        """Generate layout."""

        # Actor information ---------------------------------------------------

        actor_information_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Actor information", className="card-title"),
                        self._get_actor_information_table(),
                    ]
                ),
            ],
            color="warning",
            outline=True,
        )

        # Actor commands ------------------------------------------------------

        actor_commands_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Actor commands", className="card-title"),
                        dcc.Markdown("🚧 Under construction!", style={"font-size": "20px"}),
                    ]
                ),
            ],
            color="warning",
            outline=True,
        )

        # System Files --------------------------------------------------------

        system_files_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("System Files", className="card-title"),
                        self._get_system_files(),
                    ]
                ),
            ],
            color="warning",
            outline=True,
        )

        # Actor log -----------------------------------------------------------

        actor_log_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Actor Log", className="card-title"),
                        self._get_actor_logs_table(),
                    ]
                ),
            ],
            color="warning",
            outline=True,
        )

        # Actor statistics -----------------------------------------------------------

        actor_statistics_card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Actor Statistics", className="card-title"),
                        self._get_actor_statistics_table(),
                    ]
                ),
            ],
            color="warning",
            outline=True,
        )

        # Assembly -------------------------------------------------------------------

        content = [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(actor_information_card, width=12),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(actor_commands_card, width=12),
                ]
            ),
        ]

        if self.actor_info:
            if self.actor_info["kind"] == "system":
                content.extend(
                    [
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(system_files_card, width=12),
                            ]
                        ),
                    ]
                )

        content.extend(
            [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(actor_log_card, width=12),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(actor_statistics_card, width=12),
                    ]
                ),
            ]
        )

        return html.Div(content)
