# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid
import pandas as pd
import dash_daq as daq


from ansys.saf.glow.client.dashclient import DashClient
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep


class AutoUpdateSwitchAIO(html.Div): 

    class ids:
        switch = lambda aio_id: {
            'component': 'AutoUpdateSwitchAIO',
            'subcomponent': 'switch',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, aio_id: str = None):
        """AutoUpdateSwitchAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.
        
        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        switch_props = {
            "on": problem_setup_step.activate_auto_update,
            "color": "#FFB71B",
            "className": "ms-auto",
        }
        
        super().__init__([ 
            dcc.Interval(id=self.ids.interval(aio_id), **switch_props),
            dbc.Stack(
                [
                    daq.BooleanSwitch(id=self.ids.switch(aio_id), **switch_props),
                    html.Div("Auto update")
                ],
                direction="horizontal",
                gap=1,
            ),   
        ])

    @callback(
        Output(ids.switch(MATCH), 'disabled'),
        Input(ids.switch(MATCH), 'on'),
        State("url", "pathname"),
    )
    def auto_update(on, pathname):

        project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
        problem_setup_step = project.steps.problem_setup_step

        problem_setup_step.auto_update_activated = on

        return False
