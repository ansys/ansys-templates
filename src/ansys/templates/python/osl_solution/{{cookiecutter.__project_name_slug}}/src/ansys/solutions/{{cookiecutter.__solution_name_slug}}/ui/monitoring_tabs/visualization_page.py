# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the second step."""


from ansys.saf.glow.client.dashclient import DashClient
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, callback, dcc, html
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{cookiecutter.__solution_definition_name}}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.colorscale import ANSYS_COLORSCALE
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.monitoring_tabs.design_table_page import DesignTable


def layout(monitoring_step: MonitoringStep):
    """Layout of the visualization tab UI."""

    monitoring_step.get_visualization_data()

    axes_selection = dbc.CardBody(
        dbc.Card(
            [
                dcc.Markdown("""Axes"""),
                html.Div(
                    [
                        dcc.Markdown("""1st"""),
                        dcc.Dropdown(
                            [
                                key
                                for key in monitoring_step.design_table.keys()
                                if key not in ["Design", "Feasible", "Status", "Pareto"]
                            ],
                            monitoring_step.selected_axis_1,
                            id="axis_1",
                            multi=False,
                            clearable=True,
                            disabled=False,
                        ),
                    ],
                    style={"width": "100%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Markdown("""2nd"""),
                        dcc.Dropdown(
                            [
                                key
                                for key in monitoring_step.design_table.keys()
                                if key not in ["Design", "Feasible", "Status", "Pareto"]
                            ],
                            monitoring_step.selected_axis_2,
                            id="axis_2",
                            multi=False,
                            clearable=True,
                            disabled=False,
                        ),
                    ],
                    style={"width": "100%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Markdown("""3rd"""),
                        dcc.Dropdown(
                            [
                                key
                                for key in monitoring_step.design_table.keys()
                                if key not in ["Design", "Feasible", "Status", "Pareto"]
                            ],
                            monitoring_step.selected_axis_3,
                            id="axis_3",
                            multi=False,
                            clearable=True,
                            disabled=False,
                        ),
                    ],
                    style={"width": "100%", "display": "inline-block"},
                ),
            ]
        )
    )

    design_selection = dbc.CardBody(
        dbc.Card(
            [
                dcc.Markdown("""Designs"""),
                html.Div(
                    [
                        dcc.Markdown("""Selection"""),
                        dcc.Dropdown(
                            monitoring_step.design_table["Design"],
                            monitoring_step.selected_design_id,
                            id="design_id",
                            multi=False,
                            clearable=True,
                            disabled=False,
                        ),
                    ],
                    style={"width": "100%", "display": "inline-block"},
                ),
            ]
        )
    )

    parameter_ranges_graph = dcc.Loading(
        id="loading_parameter_ranges_graph",
        type="circle",
        color="#ffb71b",
        children=[dcc.Graph(id="parameter_ranges_graph")],
    )

    response_ranges_graph = dcc.Loading(
        id="loading_response_ranges_graph",
        type="circle",
        color="#ffb71b",
        children=[dcc.Graph(id="response_ranges_graph")],
    )

    criteria_ranges_graph = dcc.Loading(
        id="loading_criteria_ranges_graph",
        type="circle",
        color="#ffb71b",
        children=[dcc.Graph(id="criteria_ranges_graph")],
    )

    anthill_graph = (
        dcc.Loading(
            id="loading_anthill_graph",
            type="circle",
            color="#ffb71b",
            children=[dcc.Graph(id="anthill_graph")],
        ),
    )

    history_graph = dcc.Loading(
        id="loading_history_graph",
        type="circle",
        color="#ffb71b",
        children=[dcc.Graph(id="history_graph")],
    )

    parallel_coordinates_graph = dcc.Loading(
        id="load_parallel_coordinates_graph",
        type="circle",
        color="#ffb71b",
        children=[dcc.Graph(id="parallel_coordinates_graph")],
    )

    design_table = DesignTable(pd.DataFrame(monitoring_step.design_table))

    return html.Div(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([dbc.Row(axes_selection), dbc.Row(design_selection)], width=1),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(parameter_ranges_graph, md=4),
                                    dbc.Col(response_ranges_graph, md=4),
                                    dbc.Col(criteria_ranges_graph, md=4),
                                ],
                                className="g-0",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(anthill_graph, md=4),
                                    dbc.Col(history_graph, md=4),
                                    dbc.Col(parallel_coordinates_graph, md=4),
                                ],
                                className="g-0",
                            ),
                            dbc.Row([dbc.Col(design_table.render(), md=12)]),
                        ],
                        width={"size": 9, "offset": 0, "order": "2"},
                    ),
                ]
            ),
        ]
    )


@callback(
    Output("parameter_ranges_graph", "figure"),
    Output("response_ranges_graph", "figure"),
    Output("criteria_ranges_graph", "figure"),
    Output("anthill_graph", "figure"),
    Output("history_graph", "figure"),
    Output("parallel_coordinates_graph", "figure"),
    Input("axis_1", "value"),
    Input("axis_2", "value"),
    Input("axis_3", "value"),
    Input("design_id", "value"),
    State("url", "pathname"),
)
def update_graphs(selected_axis_1, selected_axis_2, selected_axis_3, selected_design_id, pathname):
    """"""

    project = DashClient[{{cookiecutter.__solution_definition_name}}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step

    monitoring_step.selected_design_id = selected_design_id
    monitoring_step.selected_axis_1 = selected_axis_1
    monitoring_step.selected_axis_2 = selected_axis_2
    monitoring_step.selected_axis_3 = selected_axis_3

    monitoring_step.get_visualization_data()

    return (
        {
            "data": [
                {
                    "x": list(monitoring_step.parameter_ranges.keys()),
                    "y": [parameter["range"] for parameter in monitoring_step.parameter_ranges.values()],
                    "type": "bar",
                    "name": "parameters",
                    "marker": {
                        "color": [parameter["range"] for parameter in monitoring_step.parameter_ranges.values()],
                        "colorscale": ANSYS_COLORSCALE,
                    },
                },
            ],
            "layout": {"title": "Parameter Ranges", "yaxis": {"title": "Relative to range", "range": [0, 100]}},
        },
        {
            "data": [
                {
                    "x": list(monitoring_step.response_ranges.keys()),
                    "y": [response["range"] for response in monitoring_step.response_ranges.values()],
                    "type": "bar",
                    "name": "responses",
                    "marker": {
                        "color": [response["range"] for response in monitoring_step.response_ranges.values()],
                        "colorscale": ANSYS_COLORSCALE,
                    },
                },
            ],
            "layout": {"title": "Response Ranges", "yaxis": {"title": "Relative to range", "range": [0, 100]}},
        },
        {
            "data": [
                {
                    "x": list(monitoring_step.objective_ranges.keys()),
                    "y": [objective["range"] for objective in monitoring_step.objective_ranges.values()],
                    "type": "bar",
                    "name": "objective",
                    "marker": {
                        "color": [objective["range"] for objective in monitoring_step.objective_ranges.values()],
                        "colorscale": ANSYS_COLORSCALE,
                    },
                },
                {
                    "x": list(monitoring_step.constraint_ranges.keys()),
                    "y": [constraint["range"] for constraint in monitoring_step.constraint_ranges.values()],
                    "type": "bar",
                    "name": "constraints",
                    "marker": {
                        "color": [constraint["range"] for constraint in monitoring_step.constraint_ranges.values()],
                        "colorscale": ANSYS_COLORSCALE,
                    },
                },
            ],
            "layout": {"title": "Criteria Ranges", "yaxis": {"title": "Relative to range", "range": [0, 100]}},
        },
        {
            "data": [
                {
                    "x": list(monitoring_step.anthill[monitoring_step.selected_axis_1]),
                    "y": list(monitoring_step.anthill[monitoring_step.selected_axis_2]),
                    "type": "scatter",
                    "name": "anthill",
                    "mode": "markers",
                },
            ],
            "layout": {
                "title": "Anthill",
                "xaxis": {"title": monitoring_step.selected_axis_1},
                "yaxis": {"title": monitoring_step.selected_axis_2},
            },
        },
        {
            "data": [
                {
                    "x": [int(design.split(".")[-1]) for design in list(monitoring_step.history["Design"])],
                    "y": list(monitoring_step.history[monitoring_step.selected_axis_1]),
                    "type": "scatter",
                    "name": "history",
                    "mode": "markers+lines",
                },
            ],
            "layout": {
                "title": "History",
                "xaxis": {"title": "Designs"},
                "yaxis": {"title": monitoring_step.selected_axis_1},
            },
        },
        {
            "data": [
                {
                    "dimensions": [
                        {
                            "range": monitoring_step.parallel_coordinates[field_name]["range"],
                            "label": field_name,
                            "values": monitoring_step.parallel_coordinates[field_name]["values"],
                        }
                        for field_name in monitoring_step.parallel_coordinates.keys()
                    ],
                    "type": "parcoords",
                    "line_color": "rgb(0, 0, 0)",
                },
            ],
            "layout": {
                "title": "Parallel Coordinates",
            },
        },
    )
