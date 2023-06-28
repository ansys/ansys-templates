# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the actor logs for system and actor node types."""

from datetime import datetime

from dash import dash_table
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import (
    remove_key_from_dictionaries,
    sort_dict_by_ordered_keys,
)


class ActorLogsTable:
    """Actor logs component."""

    def __init__(self) -> None:
        """Constructor."""

        self.actor_info: dict = None
        self.font_size: str = "15px"

    def _get_data(self) -> pd.DataFrame:

        has_data = False

        if self.actor_info:
            if "log_messages" in self.actor_info.keys():
                if len(self.actor_info["log_messages"]):
                    has_data = True
                    # Remove hid key from list dictionaries because it is useless for UI
                    # and prevent transformation to DataFrame.
                    actor_logs_data = remove_key_from_dictionaries(self.actor_info["log_messages"], "hid")
                    # Transform list of dictionaries into dictionary
                    actor_logs_data = {
                        key: [d[key] for d in self.actor_info["log_messages"]]
                        for key in self.actor_info["log_messages"][0]
                    }
                    # Sort keys in order
                    actor_logs_data = sort_dict_by_ordered_keys(actor_logs_data, ["time_stamp", "level", "message"])
                    # Rename keys
                    actor_logs_data["Time"] = actor_logs_data.pop("time_stamp")
                    actor_logs_data["Level"] = actor_logs_data.pop("level")
                    actor_logs_data["Message"] = actor_logs_data.pop("message")
                    # Convert timestamp
                    for index, value in enumerate(actor_logs_data["Time"]):
                        dt = datetime.strptime(value, "%Y%m%dT%H%M%S.%f")
                        actor_logs_data["Time"][index] = dt.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]

        if not has_data:
            actor_logs_data = {"Time": [], "Level": [], "Message": []}

        return pd.DataFrame(actor_logs_data)

    def render(self):
        """Generate table."""

        data = self._get_data()

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": i, "id": i, "type": "text"} for i in data.columns],
            fixed_rows={"headers": True},
            style_header={"font_family": "Roboto", "font_size": self.font_size, "fontWeight": "bold"},
            style_cell={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
            },
            style_cell_conditional=[
                {"if": {"column_id": "Time"}, "minWidth": "60px", "maxWidth": "60px", "width": "60px"},
                {
                    "if": {"column_id": "Level"},
                    "minWidth": "30px",
                    "maxWidth": "30px",
                    "width": "30px",
                    "textAlign": "center",
                },
                {"if": {"column_id": "Message"}, "minWidth": "200px", "maxWidth": "200px", "width": "200px"},
            ],
            style_data_conditional=[
                {
                    "if": {"column_id": "Level", "filter_query": '{Level} eq "INFO"'},
                    "backgroundColor": "rgb(227, 245, 252)",
                    "color": "rgb(0, 0, 0)",
                    "textAlign": "center",
                }
            ],
            style_as_list_view=True,
        )
