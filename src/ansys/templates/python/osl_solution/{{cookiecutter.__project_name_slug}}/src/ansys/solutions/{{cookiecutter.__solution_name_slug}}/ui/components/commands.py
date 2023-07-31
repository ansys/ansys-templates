# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Enable raw commands execution on optiSLang server."""

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


class Commands(object):
    """OSL server commands."""

    def __init__(self, lock_commands: bool) -> None:
        """Constructor."""

        self._lock_commands: bool = lock_commands
        self._enable_restart: bool = True
        self._enable_stop_gently: bool = True
        self._enable_stop: bool = True
        self._enable_reset: bool = True
        self._enable_shutdown: bool = True
        self._property_suffix: str = None

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

        buttons = []

        if self._enable_restart:
            buttons.append(
                dbc.Button(
                    html.I(className="fas fa-play", style={"display": "inline-block"}),
                    id=f"restart_{self._property_suffix}",
                    disabled=self._lock_commands,
                    style=button_style,
                )
            )
        if self._enable_stop_gently:
            buttons.append(
                dbc.Button(
                    html.I(className="fa fa-hand-paper", style={"display": "inline-block"}),
                    id=f"stop_gently_{self._property_suffix}",
                    disabled=self._lock_commands,
                    style=button_style,
                )
            )
        if self._enable_stop:
            buttons.append(
                dbc.Button(
                    html.I(className="fas fa-stop", style={"display": "inline-block"}),
                    id=f"stop_{self._property_suffix}",
                    disabled=self._lock_commands,
                    style=button_style,
                )
            )
        if self._enable_reset:
            buttons.append(
                dbc.Button(
                    html.I(className="fas fa-fast-backward", style={"display": "inline-block"}),
                    id=f"reset_{self._property_suffix}",
                    disabled=self._lock_commands,
                    style=button_style,
                )
            )
        if self._enable_shutdown:
            buttons.append(
                dbc.Button(
                    html.I(className="fas fa-power-off", style={"display": "inline-block"}),
                    id=f"shutdown_{self._property_suffix}",
                    disabled=self._lock_commands,
                    style=button_style,
                ),
            )

        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Stack(
                                buttons,
                                direction="horizontal",
                                gap=1,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Alert(
                                "",
                                color="light",
                                id="commands_alert",
                                dismissable=False if self._lock_commands else True,
                                is_open=True if self._lock_commands else False,
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


class ProjectCommands(Commands):

    def __init__(self, lock_commands: bool):
        super().__init__(lock_commands)
        self._property_suffix = "project"


class ActorCommands(Commands):

    def __init__(self, lock_commands: bool):
        super().__init__(lock_commands)
        self._enable_shutdown = False
        self._property_suffix = "actor"
