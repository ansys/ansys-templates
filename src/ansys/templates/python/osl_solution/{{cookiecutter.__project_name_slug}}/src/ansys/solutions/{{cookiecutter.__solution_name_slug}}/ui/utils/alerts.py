# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


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
    if problem_setup_step.optislang_solve_status == "initial":
        solve_message, solve_color = "optiSLang simulation not started.", "warning"
    elif problem_setup_step.optislang_solve_status == "processing":
        solve_message, solve_color = "optiSLang simulation in progress.", "primary"
    elif problem_setup_step.optislang_solve_status == "stopped":
        solve_message, solve_color = "optiSLang simulation stopped.", "danger"
    elif problem_setup_step.optislang_solve_status == "aborted":
        solve_message, solve_color = "optiSLang simulation aborted.", "danger"
    elif problem_setup_step.optislang_solve_status == "finished":
        solve_message, solve_color = "optiSLang simulation completed successfully.", "success"
    else:
        raise ValueError(f"Unknown optiSLang status: {problem_setup_step.optislang_solve_status}.")

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

    if problem_setup_step.optislang_solve_status == "initial":
        return dbc.Alert(
            "No analysis started. No data to display.",
            color="warning",
        )
