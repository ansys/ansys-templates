# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

from ansys.solutions.dash_components.table import OutputRow
import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the second step UI."""

    monitoring_step.get_project_summary()

    font_size = "15px"

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dcc.Markdown("**Project Information**", style={"font-size": "20px"}),
                    OutputRow(
                        "label",
                        "project-state",
                        "State",
                        row_default_value=monitoring_step.summary["state"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-id",
                        "Id",
                        row_default_value=monitoring_step.summary["project_id"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-name",
                        "Name",
                        row_default_value=monitoring_step.summary["name"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-machine",
                        "Machine",
                        row_default_value=monitoring_step.summary["machine"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-location",
                        "Location",
                        row_default_value=monitoring_step.summary["location"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-directory",
                        "Project directory",
                        row_default_value=monitoring_step.summary["working_dir"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "project-owner",
                        "Owner",
                        row_default_value=monitoring_step.summary["user"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "registered",
                        "Registered",
                        row_default_value=None,
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                    OutputRow(
                        "label",
                        "lock-info",
                        "Lock info",
                        row_default_value=None,
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get(),
                ],
            ),
        ]
    )
