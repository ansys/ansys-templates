# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""

from ansys.solutions.dash_components.table import OutputRow
import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the second step UI."""

    monitoring_step.get_summary()
    font_size = "15px"

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dcc.Markdown("**Actor Information**", style={"font-size": "20px"}),
                    OutputRow(
                        "label",
                        "working_directory",
                        "Working directory",
                        row_default_value=monitoring_step.summary["working_directory"],
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
                        "processing_state",
                        "Processing state",
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
                        "execution_duration",
                        "Execution duration",
                        row_default_value=monitoring_step.summary["execution_duration"],
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
                        "processed",
                        "Processed",
                        row_default_value=monitoring_step.summary["processed"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get()
                    if monitoring_step.summary["processed"]
                    else None,
                    OutputRow(
                        "label",
                        "status",
                        "Status",
                        row_default_value=monitoring_step.summary["status"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get()
                    if monitoring_step.summary["status"]
                    else None,
                    OutputRow(
                        "label",
                        "succeeded",
                        "Succeeded",
                        row_default_value=monitoring_step.summary["succeeded"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get()
                    if monitoring_step.summary["succeeded"]
                    else None,
                    OutputRow(
                        "label",
                        "not_succeeded",
                        "Not succeeded",
                        row_default_value=monitoring_step.summary["not_succeeded"],
                        row_description="",
                        label_width=2,
                        value_width=10,
                        unit_width=0,
                        description_width=0,
                        font_size=font_size,
                        text_align="left",
                    ).get()
                    if monitoring_step.summary["not_succeeded"]
                    else None,
                ],
            ),
        ]
    )
