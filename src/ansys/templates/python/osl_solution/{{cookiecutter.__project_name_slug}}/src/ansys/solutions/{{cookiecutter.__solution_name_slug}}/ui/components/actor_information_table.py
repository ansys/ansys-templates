# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the actor information for system and actor node types."""

from dash import dash_table
import pandas as pd


class ActorInformationTable:
    """Actor information component."""

    def __init__(self) -> None:
        """Constructor."""

        self.actor_info: dict = None
        self.actor_status_info: dict = None
        self.font_size: str = "15px"

    def _get_data(self) -> pd.DataFrame:

        actor_information_data = {
            "column_a": ["Working directory", "Processing state", "Execution duration"],
            "column_b": [None, None, None],
        }

        if self.actor_info and self.actor_status_info:
            actor_information_data["column_b"] = [
                self.actor_status_info["working dir"],
                self.actor_status_info["state"],
                "-",
            ]
            if self.actor_info["kind"] == "system":
                succeeded_designs = self.actor_status_info["succeeded_designs"]
                failed_designs = self.actor_status_info["failed_designs"]
                pending_designs = self.actor_status_info["pending_designs"]
                total_designs = self.actor_status_info["total_designs"]
                processed_designs = total_designs - pending_designs
                status = int(processed_designs / total_designs * 100)
                actor_information_data["column_a"].extend(["Processed", "Status", "Succeeded", "Not succeeded"])
                actor_information_data["column_b"].extend(
                    [f"{processed_designs} / {total_designs}", f"{status}%", succeeded_designs, failed_designs]
                )

        return pd.DataFrame(actor_information_data)

    def render(self):
        """Generate table."""

        data = self._get_data()

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": i, "id": i, "type": "text"} for i in data.columns],
            fixed_rows={"headers": True},
            style_header={
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": self.font_size,
                "fontWeight": "bold",
                "border": "none",
                "display": "none",
            },
            style_cell={"textAlign": "left", "font_family": "Roboto", "font_size": self.font_size, "border": "none"},
            style_as_list_view=True,
            style_table={"border": "none"},  # Hide table borders
        )
