# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the monitoring step."""


from dash_extensions.enrich import dcc, html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep):
    """Layout of the second step UI."""
    return html.Div(
        [
            dcc.Markdown("""#### Monitoring step""", className="display-3"),
            dcc.Markdown("""###### Subtitle.""", className="display-3"),
            html.Hr(className="my-2"),
            html.Br(),
        ]
    )
