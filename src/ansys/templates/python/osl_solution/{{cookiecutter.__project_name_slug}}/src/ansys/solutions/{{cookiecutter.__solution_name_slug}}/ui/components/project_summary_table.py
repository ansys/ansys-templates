# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the root project information."""

from dash import dash_table
import pandas as pd


class ProjectSummaryTable:
    """Project summary component."""

    def __init__(self) -> None:
        """Constructor."""

        self.project_status_info: dict = None
        self.font_size: str = "15px"

    def _get_data(self) -> pd.DataFrame:

        project_summary_data = {
            "column_a": [
                "State",
                "Id",
                "Name",
                "Machine",
                "Location",
                "Project directory",
                "Owner",
                "Registered",
                "Lock info",
            ],
            "column_b": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        }

        if self.project_status_info:
            project_summary_data["column_b"] = [
                self.project_status_info["projects"][0]["state"],
                self.project_status_info["projects"][0]["project_id"],
                self.project_status_info["projects"][0]["name"],
                self.project_status_info["projects"][0]["machine"],
                self.project_status_info["projects"][0]["location"],
                self.project_status_info["projects"][0]["working_dir"],
                self.project_status_info["projects"][0]["user"],
                "",
                "",
            ]

        return pd.DataFrame(project_summary_data)

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
