# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the node status overview view."""

from dash_extensions.enrich import html
import optislang_dash_lib


def layout(project_status_info: dict) -> html.Div:
    """Layout of the status overview view."""

    if project_status_info:
        return html.Div(
            id="node-status-view",
            children=[
                optislang_dash_lib.Nodestatusviewcomponent(
                    id="node-status-view-component",
                    project_state=project_status_info,
                ),
            ],
        )
    else:
        return html.Div([])
