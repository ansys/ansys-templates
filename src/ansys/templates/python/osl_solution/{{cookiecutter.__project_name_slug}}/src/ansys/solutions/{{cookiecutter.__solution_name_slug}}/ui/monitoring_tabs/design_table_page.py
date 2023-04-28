# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

from dash import dash_table
from dash_extensions.enrich import html
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


class DesignTable(object):
    """"""

    def __init__(self, data):
        """Constructor."""

        self.data = data

    def render(self):
        """Generate table."""

        data = self.data.copy()

        for col, dtype in data.dtypes.items():
            if dtype == "bool":
                data[col] = data[col].astype("str")

        data = data.round(6)

        return dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": i, "id": i, "type": "text"} for i in data.columns],
            fixed_rows={"headers": True},
            sort_action="native",
            row_selectable="multi",
            page_action="native",
            style_header={"textAlign": "center", "font_family": "Roboto", "font_size": "15px", "fontWeight": "bold"},
            style_cell={
                "textAlign": "center",
                "font_family": "Roboto",
                "font_size": "15px",
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
        )


def layout(monitoring_step: MonitoringStep):
    """Layout of the second step UI."""

    monitoring_step.get_design_table()

    design_table = DesignTable(pd.DataFrame(monitoring_step.design_table))

    return html.Div([design_table.render()])
