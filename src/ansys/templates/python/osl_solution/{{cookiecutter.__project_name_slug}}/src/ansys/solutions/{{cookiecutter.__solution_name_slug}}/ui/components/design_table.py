# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Provide a component to handle the design table for root and system node types."""

from dash import dash_table
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.common_functions import sorted_nicely


class DesignTable:
    """Design table component."""

    def __init__(self) -> None:
        """Constructor."""

        self.actor_info: dict = None
        self.actor_status_info: dict = None
        self._field_types = ["parameter", "constraint", "objective", "response"]
        self.font_size: str = "15px"

    def _sort_designs(self, designs: list) -> list:
        """"""

        sorted_designs = sorted_nicely(designs)
        return [designs.index(design) for design in sorted_designs]

    def _get_data(self) -> pd.DataFrame:

        design_table_data = {
            "Design": [],
            "Feasible": [],
            "Status": [],
            "Pareto": [],
        }

        if self.actor_info:
            if self.actor_info["kind"] == "system":
                for field_type in self._field_types:
                    field_name_index = field_type + "_names"
                    for field_name in self.actor_status_info["designs"][field_name_index]:
                        design_table_data[field_name] = []
                design_numbers = []
                for design_values in reversed(self.actor_status_info["designs"]["values"]):
                    design_numbers.append(design_values["hid"].split(".")[-1])
                    design_table_data["Design"].append(design_values["hid"])
                    for field_type in self._field_types:
                        field_name_index = field_type + "_names"
                        field_value_index = field_type + "_values"
                        field_names = self.actor_status_info["designs"][field_name_index]
                        field_values = design_values[field_value_index]
                        if len(field_names) != len(field_values):
                            field_values = [None for i in range(len(field_names))]
                        for field_name, field_value in zip(field_names, field_values):
                            if isinstance(field_value, dict):
                                if field_value["type"] == "xy_data":
                                    field_value = f"[1:%s]" % (field_value["num_entries"])
                            design_table_data[field_name].append(field_value)
                for design_status in reversed(self.actor_status_info["design_status"]):
                    design_table_data["Feasible"].append(design_status["feasible"])
                    design_table_data["Status"].append(design_status["status"])
                    design_table_data["Pareto"].append(design_status["pareto_design"])

                design_table_data = pd.DataFrame(design_table_data)

                # OptiSLang returns the designs in an unsorted way.
                # The following method organizes the rows in ascending order.
                design_table_data = design_table_data.loc[self._sort_designs(design_table_data["Design"].to_list())]

                for col, dtype in design_table_data.dtypes.items():
                    if dtype == "bool":
                        design_table_data[col] = design_table_data[col].astype("str")

                design_table_data = design_table_data.round(6)

        return pd.DataFrame(design_table_data)

    def render(self) -> dash_table.DataTable:
        """Generate table."""

        data = self._get_data()

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": i, "id": i, "type": "text"} for i in data.columns],
            fixed_rows={"headers": True},
            style_header={
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": self.font_size,
                "fontWeight": "bold",
            },
            style_cell={
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": self.font_size,
                "whiteSpace": "normal",
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "Status", "filter_query": '{Status} eq "Succeeded"'},
                    "backgroundColor": "rgb(223, 240, 208)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Status", "filter_query": '{Status} eq "Not succeeded"'},
                    "backgroundColor": "rgb(254, 221, 215)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Feasible", "filter_query": '{Feasible} eq "True"'},
                    "backgroundColor": "rgb(223, 240, 208)",
                    "color": "rgb(0, 0, 0)",
                },
                {
                    "if": {"column_id": "Feasible", "filter_query": '{Feasible} eq "False"'},
                    "backgroundColor": "rgb(254, 221, 215)",
                    "color": "rgb(0, 0, 0)",
                },
            ],
            style_as_list_view=True,
        )
