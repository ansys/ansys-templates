# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


class ButtonGroup:
    def __init__(self, options, disabled=False):
        self.options = options
        self.disabled = disabled
        self.buttons = self._create_button_group()

    def _create_button_group(self):
        btn_group = []
        for option in self.options:
            icon = option['icon']
            tooltip = option['tooltip']
            id = option['id']
            button = ButtonWithTooltip(id, icon, self.disabled, tooltip)
            btn_group.append(button)
        return btn_group

class ButtonWithTooltip(html.Div):

    def __init__(self, id, button_icon, is_disabled, tooltip):

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

        super().__init__(
            [
                dbc.Button(
                    id=id,
                    children=html.Div(
                        [
                            html.I(className=button_icon, style={"display": "inline-block"}),
                        ],
                        ),
                    style=button_style,
                    disabled=is_disabled,
                ),
                dbc.Tooltip(
                    id=f"tooltip-{id}",
                    target=id,
                    placement="bottom",
                    children=tooltip
                ),
            ]
        )
