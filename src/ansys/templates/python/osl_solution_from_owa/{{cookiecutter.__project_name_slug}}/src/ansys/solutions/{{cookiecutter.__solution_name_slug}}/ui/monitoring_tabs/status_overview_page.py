# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

from dash import dash_table
from dash_extensions.enrich import html
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


class StatusOverviewTable(object):
    """"""

    def __init__(self, data):
        """Constructor."""

        self.data = data

    def render(self):
        """Generate table."""

        if isinstance(self.data, pd.DataFrame):
            return dash_table.DataTable(
                data=self.data.to_dict("records"),
                columns=[{"name": i, "id": i, "type": "text"} for i in self.data.columns],
                fixed_rows={"headers": True},
                sort_action="native",
                row_selectable="multi",
                page_action="native",
                style_header={
                    "textAlign": "center",
                    "font_family": "Roboto",
                    "font_size": "15px",
                    "fontWeight": "bold",
                },
                style_cell={
                    "textAlign": "center",
                    "font_family": "Roboto",
                    "font_size": "15px",
                },
            )


def layout(monitoring_step: MonitoringStep):
    """Layout of the status overview tab UI."""

    monitoring_step.get_status_overview()

    status_overview_table = StatusOverviewTable(pd.DataFrame(monitoring_step.status_overview))

    return html.Div([status_overview_table.render()])
