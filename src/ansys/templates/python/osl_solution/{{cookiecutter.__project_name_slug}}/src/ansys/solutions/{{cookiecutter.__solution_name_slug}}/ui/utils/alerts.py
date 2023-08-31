# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.utils.constants import PROJECT_STATES


def update_alerts(problem_setup_step: ProblemSetupStep) -> list:
    """Update all Alerts."""

    alerts = []

    # Product version alerts
    for product_name, product_data in problem_setup_step.ansys_ecosystem.items():
        alerts.append(
            html.Div(
                [
                    dbc.Button(
                        f"{product_data['alias']} Version",
                        id=f"popover_{product_name}_version_target",
                        disabled=False,
                        color=product_data["alert_color"],
                        n_clicks=0,
                    ),
                    dbc.Popover(
                        [
                            dbc.PopoverBody(product_data["alert_message"]),
                        ],
                        id=f"popover_{product_name}_version",
                        target=f"popover_{product_name}_version_target",
                        placement="top",
                        is_open=False,
                    ),
                ]
            ),
        )

    # optiSLang solve alert
    if problem_setup_step.project_state in PROJECT_STATES.keys():
        solve_message, solve_color = PROJECT_STATES[problem_setup_step.project_state]["alert"], PROJECT_STATES[problem_setup_step.project_state]["color"]
    else:
        raise ValueError(f"Unknown optiSLang state: {problem_setup_step.project_state}.")

    alerts.append(
        html.Div(
            [
                dbc.Button(
                    "optiSLang Solve",
                    id="popover_optislang_solve_target",
                    disabled=False,
                    color=solve_color,
                    n_clicks=0,
                ),
                dbc.Popover(
                    [
                        dbc.PopoverBody(solve_message),
                    ],
                    id="popover_optislang_solve",
                    target="popover_optislang_solve_target",
                    placement="top",
                    is_open=False,
                ),
            ]
        ),
    )

    return alerts


def update_monitoring_alert(problem_setup_step: ProblemSetupStep) -> dbc.Alert:

    if problem_setup_step.project_state == "NOT STARTED":
        return dbc.Alert(
            "No analysis started. No data to display.",
            color="warning",
        )
