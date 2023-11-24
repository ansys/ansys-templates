# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the visualization view."""

import json
import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(problem_setup_step: ProblemSetupStep, monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the visualization view."""

    full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())

    return html.Div(
        [
            html.Div(
                id="visualization-component-div1"
            ),
            html.Div(
                id="visualization-component-div2"
            ),
            dcc.Interval(
                id="visualization_auto_update",
                interval=monitoring_step.auto_update_frequency,  # in milliseconds
                n_intervals=0,
                disabled=False if monitoring_step.auto_update_activated else True,
            )
            
        ]
    )



    @callback(
        Output("visualization-component-div1", "children"),
        Output("visualization-component-div2", "children"),
        Output("visualization-component-div1", "style"),
        Output("visualization-component-div2", "style"),
        Input("visualization_auto_update", "n_intervals"),
        State("url", "pathname"),
    )
    def update_view(n_intervals, pathname):
        """Update design table."""
    
        # Get project
        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        # Get problem setup step
        problem_setup_step = project.steps.problem_setup_step
        # Get monitoring step
        monitoring_step = project.steps.monitoring_step
    
        if monitoring_step.auto_update_activated:
            print("Interval call in visualization view")
            # Get project data
            full_project_status_info = json.loads(problem_setup_step.full_project_status_info_file.read_text())
            
            visualization_status_view_1_child = None
            visualization_status_view_1_style = None
            visualization_status_view_2_child = None
            visualization_status_view_2_style = None
            
            if n_intervals % 2==0: #(even)
                visualization_status_view_1_child = optislang_dash_lib.VisualizationComponent(
                            id="visualization-component1",
                            project_state=full_project_status_info,
                            system_id=monitoring_step.selected_actor_from_treeview,
                            state_idx=0,
                        )
                visualization_status_view_1_style = {'display': 'block'}
                visualization_status_view_2_style = {'display': 'none'}
            else:
                visualization_status_view_2_child = optislang_dash_lib.VisualizationComponent(
                            id="visualization-component1",
                            project_state=full_project_status_info,
                            system_id=monitoring_step.selected_actor_from_treeview,
                            state_idx=0,
                        )
                visualization_status_view_2_style = {'display': 'block'}
                visualization_status_view_1_style = {'display': 'none'}
            
    
            return visualization_status_view_1_child, visualization_status_view_1_style, visualization_status_view_2_child, visualization_status_view_2_style
    
        else:
            raise PreventUpdate
