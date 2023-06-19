# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the visualization view."""

from dash_extensions.enrich import html
import optislang_dash_lib


def layout(project_status_info: dict, uid: str) -> html.Div:
    """Layout of the visualization view."""

    return html.Div(
        [
            optislang_dash_lib.VisualizationComponent(
                id="visualization-component",
                project_state=project_status_info,
                system_id=uid,
                state_idx=0,
            ),
        ]
    )
