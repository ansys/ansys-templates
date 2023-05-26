# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the monitoring step."""

from ansys.saf.glow.solution import StepModel, StepSpec, transaction
from ansys.solutions.optislang.wrapper.monitoring import Monitoring


class MonitoringStep(StepModel):
    """Step model of the monitoring step."""

    # Frontend persistence
    available_root_nodes: list = []
    available_system_nodes: dict = {}
    available_subsystem_nodes: dict = {}
    available_fields: list = []
    selected_root_node: str = None
    selected_system_node: str = None
    selected_subsystem_node: str = None
    selected_node_kind: str = None
    selected_design_id: str = None
    selected_axis_1: str = None
    selected_axis_2: str = None
    selected_axis_3: str = None
    summary: dict = None
    design_table: dict = None
    parameter_ranges: dict = None
    response_ranges: dict = None
    constraint_ranges: dict = None
    objective_ranges: dict = None
    anthill: dict = None
    history: dict = None
    parallel_coordinates: dict = None
    status_overview: dict = None
    project_state: dict = None

    @transaction(
        self=StepSpec(upload=["available_root_nodes", "available_system_nodes", "available_subsystem_nodes"]),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_system_hierarchy(self, problem_setup_step):
        """Update root nodes, system nodes and subsystem nodes."""

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        self.available_root_nodes = monitoring.get_root_node_names()
        for root_node_name in self.available_root_nodes:
            self.available_system_nodes[root_node_name] = monitoring.get_root_node_children(root_node_name)
            for system_node_name in self.available_system_nodes[root_node_name]:
                self.available_subsystem_nodes[system_node_name] = monitoring.get_system_node_children(
                    root_node_name, system_node_name
                )

        monitoring.dispose()

    @transaction(
        self=StepSpec(
            download=["selected_root_node", "selected_system_node", "selected_subsystem_node"],
            upload=["selected_node_kind"],
        ),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_node_kind(self, problem_setup_step):
        """Update root nodes, system nodes and subsystem nodes."""

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        if self.selected_subsystem_node:
            actor_name = self.selected_subsystem_node
        elif self.selected_system_node:
            actor_name = self.selected_system_node
        elif self.selected_root_node:
            actor_name = self.selected_root_node
        else:
            raise Exception("No selection.")

        self.selected_node_kind = monitoring._get_actor_type(actor_name)

        monitoring.dispose()

    @transaction(
        self=StepSpec(download=["selected_root_node"], upload=["summary"]),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_project_summary(self, problem_setup_step):
        """Get the root summary."""

        if self.selected_root_node is None:
            self.selected_root_node = self.available_root_nodes[0]

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        self.summary = monitoring.get_project_summary(self.selected_root_node)

        monitoring.dispose()

    @transaction(
        self=StepSpec(download=["selected_system_node", "selected_subsystem_node"], upload=["summary"]),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_summary(self, problem_setup_step):
        """Get the design table of a system."""

        if self.selected_subsystem_node:
            actor_name = self.selected_subsystem_node
        elif self.selected_system_node:
            actor_name = self.selected_system_node
        else:
            raise Exception("No actor selected.")

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        self.summary = monitoring.get_summary(actor_name)

        monitoring.dispose()

    @transaction(
        self=StepSpec(
            download=["selected_root_node", "selected_system_node", "selected_subsystem_node"], upload=["design_table"]
        ),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_design_table(self, problem_setup_step):
        """Get the design table of a system."""

        is_root = False
        if self.selected_subsystem_node:
            actor_name = self.selected_subsystem_node
        elif self.selected_system_node:
            actor_name = self.selected_system_node
        elif self.selected_root_node:
            is_root = True
            actor_name = self.selected_root_node
        else:
            raise Exception("No actor selected.")

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        if is_root:
            self.design_table = monitoring.get_root_design_table(actor_name, to_dataframe=False)
        else:
            self.design_table = monitoring.get_design_table(actor_name, to_dataframe=False)

        monitoring.dispose()

    @transaction(
        self=StepSpec(
            download=[
                "selected_system_node",
                # "selected_design_id",
                # "selected_axis_1",
                # "selected_axis_2",
                # "selected_axis_3",
            ],
            upload=[
                "selected_design_id",
                "selected_axis_1",
                "selected_axis_2",
                "selected_axis_3",
                "design_table",
                "parameter_ranges",
                "response_ranges",
                "constraint_ranges",
                "objective_ranges",
                "anthill",
                "history",
                "parallel_coordinates",
            ],
        ),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_visualization_data(self, problem_setup_step):
        """Get visualization data."""

        if self.selected_system_node:
            actor_name = self.selected_system_node
        else:
            raise Exception("No actor selected.")

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        self.design_table = monitoring.get_design_table(actor_name, to_dataframe=False)

        if not self.selected_design_id:
            self.selected_design_id = self.design_table["Design"][0]

        self.parameter_ranges = monitoring.get_field_ranges(
            actor_name, "parameter", selected_design_id=self.selected_design_id
        )
        self.response_ranges = monitoring.get_field_ranges(
            actor_name, "response", selected_design_id=self.selected_design_id
        )
        self.constraint_ranges = monitoring.get_field_ranges(
            actor_name, "constraint", selected_design_id=self.selected_design_id
        )
        self.objective_ranges = monitoring.get_field_ranges(
            actor_name, "objective", selected_design_id=self.selected_design_id
        )

        if not self.selected_axis_1:
            self.selected_axis_1 = list(self.parameter_ranges.keys())[0]
        if not self.selected_axis_2:
            if len(self.parameter_ranges.keys()) >= 2:
                self.selected_axis_2 = list(self.parameter_ranges.keys())[1]
            else:
                self.selected_axis_2 = self.selected_axis_1
        if not self.selected_axis_3:
            if len(self.parameter_ranges.keys()) >= 3:
                self.selected_axis_3 = list(self.parameter_ranges.keys())[2]
            else:
                self.selected_axis_3 = self.selected_axis_1

        self.anthill = monitoring.get_anthill(
            actor_name,
            selected_design_id=self.selected_design_id,
            axis_1=self.selected_axis_1,
            axis_2=self.selected_axis_2,
            to_dataframe=False,
        )
        self.history = monitoring.get_history(
            actor_name, selected_design_id=self.selected_design_id, axis_1=self.selected_axis_1, to_dataframe=False
        )
        self.parallel_coordinates = monitoring.get_parallel_coordinates(actor_name)

        monitoring.dispose()

    @transaction(
        self=StepSpec(
            download=["selected_root_node", "selected_system_node", "selected_subsystem_node"],
            upload=["status_overview"],
        ),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_status_overview(self, problem_setup_step):
        """Get the design table of a system."""

        if self.selected_subsystem_node:
            actor_name = self.selected_subsystem_node
        elif self.selected_system_node:
            actor_name = self.selected_system_node
        elif self.selected_root_node:
            actor_name = self.selected_root_node
        else:
            raise Exception("No actor selected.")

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()

        self.status_overview = monitoring.get_status_overview(actor_name, to_dataframe=False)

        monitoring.dispose()

    @transaction(
        self=StepSpec(upload=["project_state"]),
        problem_setup_step=StepSpec(download=["project_file", "host", "port"]),
    )
    def get_project_state(self, problem_setup_step):
        """Get project state."""

        monitoring = Monitoring(
            project_file=problem_setup_step.project_file.path,
            host=problem_setup_step.host,
            port=problem_setup_step.port,
        )

        monitoring.initialize()
        self.project_state = monitoring.get_scenery_and_node_status_view_data()
        monitoring.dispose()