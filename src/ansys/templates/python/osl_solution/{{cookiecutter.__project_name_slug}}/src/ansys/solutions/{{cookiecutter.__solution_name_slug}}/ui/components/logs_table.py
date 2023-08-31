# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Logs table"""

import pandas as pd

from dash_extensions.enrich import dash_table
from typing import Union


class LogsTable:
    """Logs table."""

    def __init__(self, data: Union[dict, list]) -> None:
        """Constructor."""

        self._data = data
        self.font_size: str = "15px"

    def _reshape_data(self):

        if isinstance(self._data, dict):
            pass
        elif not any(isinstance(i, list) for i in self._data):
            # This is a non-nested list.
            self._data = {"column_a": self._data}
        else:
            raise ValueError("Unprocessable data. Expect a non-nested list or a dictionary.")

    def render(self):
        """Generate table."""

        self._reshape_data()

        data = pd.DataFrame(self._data)

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": i, "id": i, "type": "text"} for i in data.columns],
            fixed_rows={"headers": True},
            style_header={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
                "fontWeight": "bold",
                "display": "none",
            },
            style_cell={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(242, 242, 242)",
                },
                {
                    "if": {"row_index": "even"},
                    "backgroundColor": "rgb(255, 255, 255)",
                },
            ],
            style_as_list_view=True,
        )
