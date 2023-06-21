# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Component to display the system files view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html


class SystemFiles(object):
    """Design table component."""

    def __init__(self) -> None:
        """Constructor."""

        self.node_name: str = "unknown_node"
        self.omdb_file: dict = None
        self.font_size: str = "15px"

    def render(self) -> html.Div:
        """Generate view."""

        return html.Div(
            [
                dbc.Stack(
                    [
                        html.Div(
                            [
                                html.Button(
                                    "Download OMDB",
                                    disabled=True if not self.omdb_file else False,
                                    id=f"download_button_{self.node_name}_omdb",
                                ),
                                dcc.Download(id=f"download_{self.node_name}_omdb"),
                            ]
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Download CSV",
                                    disabled=True if not self.omdb_file else False,
                                    id=f"download_button_{self.node_name}_csv",
                                ),
                                dcc.Download(id=f"download_{self.node_name}_csv"),
                            ]
                        ),
                    ],
                    direction="horizontal",
                    gap=3,
                )
            ]
        )
