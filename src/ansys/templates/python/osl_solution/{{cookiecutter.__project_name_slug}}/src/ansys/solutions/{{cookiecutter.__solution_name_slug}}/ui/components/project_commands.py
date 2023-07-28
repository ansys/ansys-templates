# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Component to display the system files view."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


class ProjectCommands(object):
    """Project commands."""

    def __init__(self, lock_project_commands: bool) -> None:
        """Constructor."""

        self._lock_project_commands: bool = lock_project_commands
        self.font_size: str = "15px"

    def render(self) -> html.Div:
        """Generate view."""

        button_style = {
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "fontSize": "150%",
            "color": "rgba(0, 0, 0, 1)",
            "background-color": "rgba(255, 255, 255, 1)",
            "border-color": "rgba(0, 0, 0, 1)",
            "height": "40px",
            "width": "70px",
        }

        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Stack(
                                [
                                    dbc.Button(
                                        html.I(className="fas fa-play", style={"display": "inline-block"}),
                                        id="restart_command",
                                        disabled=self._lock_project_commands,
                                        style=button_style,
                                    ),
                                    dbc.Button(
                                        html.I(className="fa fa-hand-paper", style={"display": "inline-block"}),
                                        id="stop_gently_command",
                                        disabled=self._lock_project_commands,
                                        style=button_style,
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-stop", style={"display": "inline-block"}),
                                        id="stop_command",
                                        disabled=self._lock_project_commands,
                                        style=button_style,
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-fast-backward", style={"display": "inline-block"}),
                                        id="reset_command",
                                        disabled=self._lock_project_commands,
                                        style=button_style,
                                    ),
                                    dbc.Button(
                                        html.I(className="fas fa-power-off", style={"display": "inline-block"}),
                                        id="shutdown_command",
                                        disabled=self._lock_project_commands,
                                        style=button_style,
                                    ),
                                ],
                                direction="horizontal",
                                gap=1,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Alert(
                                "",
                                color="light",
                                id="project_commands_alert",
                                dismissable=True,
                                is_open=False,
                                fade=False,
                                style={
                                    "width": "600px",
                                    "height": "40px",
                                    "display": "flex",
                                    "justify-content": "left",
                                    "align-items": "center",
                                },
                            ),
                            width="auto",
                        ),
                    ]
                )
            ]
        )
