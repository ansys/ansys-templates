# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the scenery view."""

from dash_extensions.enrich import html
import optislang_dash_lib


def layout(project_status_info: dict) -> html.Div:
    """Layout of the scenery view."""

    if project_status_info:
        return html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        optislang_dash_lib.SceneryComponent(
                            id="input",
                            project_state=project_status_info,
                        ),
                    ]
                ),
            ]
        )
    else:
        return html.Div([])
