# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the actor statistics for system and actor node types."""

from dash import dash_table
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import convert_microseconds


class ActorStatisticsTable:
    """Actor statistics component."""

    def __init__(self) -> None:
        """Constructor."""

        self.actor_info: dict = None
        self.font_size: str = "15px"

    def _get_data(self) -> pd.DataFrame:

        actor_statistics_data = {
            "row_names": ["Usages", "Accumulated", "Minimum", "Maximum", "Mean", "std_dev"],
            "Current Run": [None, None, None, None, None, None],
            "All Runs": [None, None, None, None, None, None],
        }

        if self.actor_info:
            for column_name in ["Current Run", "All Runs"]:
                key = column_name.split()[0].lower()
                actor_statistics_data[column_name][0] = self.actor_info["usage_stats"][key]["num_usages"]
                for index, row_name in enumerate(actor_statistics_data["row_names"]):
                    if row_name != "Usages":
                        duration = self.actor_info["usage_stats"][key]["exec_duration_us"][row_name.lower()]
                        duration = convert_microseconds(duration)
                        actor_statistics_data[column_name][index] = duration

        return pd.DataFrame(actor_statistics_data)

    def render(self):
        """Generate table."""

        data = self._get_data()

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[
                {"name": i, "id": i, "type": "text"} if i != "row_names" else {"name": "", "id": i, "type": "text"}
                for i in data.columns
            ],
            fixed_rows={"headers": True},
            style_header={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
                "fontWeight": "bold",
            },
            style_cell={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
            },
            style_cell_conditional=[
                {"if": {"column_id": "row_names"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
                {"if": {"column_id": "Current Run"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
                {"if": {"column_id": "All Runs"}, "minWidth": "50px", "maxWidth": "50px", "width": "50px"},
            ],
            style_data_conditional=[
                {
                    "if": {"column_id": "row_names", "filter_query": '{Level} eq "std_dev"'},
                    "backgroundColor": "rgb(227, 245, 252)",
                    "color": "rgb(0, 0, 0)",
                    "textAlign": "center",
                    # "text": dcc.Markdown('$Area (m^{2})$', mathjax=True),
                }
            ],
            style_as_list_view=True,
            # markdown_options={"html": True},
        )
