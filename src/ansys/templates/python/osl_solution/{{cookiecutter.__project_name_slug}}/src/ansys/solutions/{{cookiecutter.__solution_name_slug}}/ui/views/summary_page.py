# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the summary view."""

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.summary_view import SummaryView


def layout(
    actors_info: list, actors_status_info: dict, results_files: dict, uid: str, font_size: str = "15px"
) -> html.Div:
    """Layout of the summary view."""

    summary_view = SummaryView()

    if uid in actors_info.keys():
        summary_view.actor_info = actors_info[uid]
    if uid in actors_status_info.keys():
        summary_view.actor_status_info = actors_status_info[uid][0]
    if uid in results_files.keys():
        summary_view.result_files = results_files[uid]

    return summary_view.render()
