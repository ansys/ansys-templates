# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

import json
import os
from pathlib import Path
import platform
import tempfile
from typing import List, Optional

from ansys.optislang.core import Optislang, utils
from ansys.saf.glow.solution import (
    FileGroupReference,
    FileReference,
    AssetFileReference,
    StepModel,
    StepSpec,
    create_instance,
    long_running,
    transaction,
)
from ansys.solutions.optislang.frontend_components.project_properties import (
    ProjectProperties,
    apply_placeholders_to_properties_file,
    write_properties_file,
)
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.solution.optislang_manager import OptislangManager
from ansys.solutions.{{cookiecutter.__solution_name_slug}}.utilities.common_functions import (
    get_treeview_items_from_project_tree,
)


class ProblemSetupStep(StepModel):
    """Step model of the problem setup step."""

    # Parameters ------------------------------------------------------------------------------------------------------

    # Frontend persistence
    ansys_ecosystem_ready: bool = False
    project_initialized: bool = False
    analysis_locked: bool = True
    project_locked: bool = False

    # Backend data model
    osl_server_host: Optional[str] = None
    osl_server_port: Optional[int] = None
    ansys_ecosystem: dict = {
        "optislang": {
            "authorized_versions": [],
            "installed_versions": [],
            "compatible_versions": [],
            "selected_version": None,
            "alert_message": "optiSLang install not checked.",
            "alert_color": "warning",
            "alias": "optiSLang",
        }
    }
    placeholders: dict = {}
    registered_files: List = []
    settings: dict = {}
    parameter_manager: dict = {}
    criteria: dict = {}
    ui_placeholders: dict = {}
    app_metadata: dict = {}
    project_tree: list = []
    treeview_items: list = [
        {
            "id": "problem_setup_step",
            "text": "Problem Setup",
            "expanded": True,
            "level": 0
        },
    ]
    optislang_log_level: str = "INFO"

    # File storage ----------------------------------------------------------------------------------------------------

    # Inputs
    project_file: AssetFileReference = AssetFileReference(relative_path="Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.opf", encrypted=False)
    properties_file: AssetFileReference = AssetFileReference(relative_path="Problem_Setup/{{ cookiecutter.__optiSLang_application_archive_stem }}.json", encrypted=False)
    metadata_file: AssetFileReference = AssetFileReference(relative_path="Problem_Setup/metadata.json", encrypted=False)
    input_files: FileGroupReference = FileGroupReference("Problem_Setup/Input_Files/*.*")
    # If folder doesn't exist, it will be created later
    upload_directory: str = os.path.join(tempfile.gettempdir(), "GLOW")

    # Outputs
    working_properties_file: FileReference = FileReference("Problem_Setup/working_properties_file.json")

    # Methods ---------------------------------------------------------------------------------------------------------

    @transaction(
        self=StepSpec(
            download=["metadata_file"],
            upload=["app_metadata"]
        )
    )
    @long_running
    def get_app_metadata(self) -> None:
        """Read OWA metadata file."""
        with open(self.metadata_file.path) as f:
            self.app_metadata = json.load(f)

    @transaction(
        self=StepSpec(
            download=["properties_file"],
            upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"]
        )
    )
    @long_running
    def get_default_placeholder_values(self):
        """Get placeholder values and definitions using the ProjectProperties class."""
        pp = ProjectProperties()
        pp.read_file(self.properties_file.path)
        self.placeholders = pp._placeholders
        self.registered_files = pp._registered_files
        self.settings = pp._settings
        self.parameter_manager = pp._parameter_manager
        self.criteria = pp._criteria

    @transaction(
        self=StepSpec(
            download=["properties_file", "ui_placeholders"],
            upload=[
                "working_properties_file",
                "placeholders",
                "registered_files",
                "settings",
                "parameter_manager",
                "criteria",
            ],
        )
    )
    def write_updated_properties_file(self) -> None:
        """Write updated optiSLang project properties file."""
        Path(self.working_properties_file.path).parent.mkdir(parents=True, exist_ok=True)
        properties = apply_placeholders_to_properties_file(self.ui_placeholders, self.properties_file.path)
        self.placeholders = properties["placeholders"]
        self.registered_files = properties["registered_files"]
        self.settings = properties["settings"]
        self.parameter_manager = properties["parameter_manager"]
        self.criteria = properties["criteria"]
        write_properties_file(properties, Path(self.working_properties_file.path))

    @transaction(
        self=StepSpec(
            download=["properties_file", "ui_placeholders"],
            upload=["placeholders", "registered_files", "settings", "parameter_manager", "criteria"],
        )
    )
    def update_osl_placeholders_with_ui_values(self) -> None:
        """Update placeholders with values selected by the user in the UI."""
        properties = apply_placeholders_to_properties_file(self.ui_placeholders, self.properties_file.path)
        self.placeholders = properties["placeholders"]
        self.registered_files = properties["registered_files"]
        self.settings = properties["settings"]
        self.parameter_manager = properties["parameter_manager"]
        self.criteria = properties["criteria"]

    @transaction(
        self=StepSpec(
            upload=["ansys_ecosystem", "ansys_ecosystem_ready"],
        )
    )
    def check_ansys_ecosystem(self) -> None:
        """Check if Ansys Products are installed and if the appropriate versions are available."""
        self.ansys_ecosystem_ready = True

        # Collect optiSLang installations
        self.ansys_ecosystem["optislang"]["installed_versions"] = sorted(list(dict(utils.find_all_osl_exec()).keys()))
        if len(self.ansys_ecosystem["optislang"]["authorized_versions"]) > 0:
            self.ansys_ecosystem["optislang"]["compatible_versions"] = [
                product_version
                for product_version in self.ansys_ecosystem["optislang"]["installed_versions"]
                if product_version in self.ansys_ecosystem["optislang"]["authorized_versions"]
            ]
        else:
            self.ansys_ecosystem["optislang"]["compatible_versions"] = self.ansys_ecosystem["optislang"]["installed_versions"]

        # Check ecosystem
        for product_name in self.ansys_ecosystem.keys():
            if len(self.ansys_ecosystem[product_name]["installed_versions"]) == 0:
                alert_message = f"No installation of {product_name.title()} found in the machine {platform.node()}."
                alert_color = "danger"
                self.ansys_ecosystem_ready = False
            elif len(self.ansys_ecosystem[product_name]["compatible_versions"]) == 0:
                alert_message = (
                    f"None of the authorized versions of {product_name.title()} "
                    f"is installed in the machine {platform.node()}.\n"
                )
                alert_message += "At least one of these versions is required:"
                for authorized_version in self.ansys_ecosystem[product_name]["authorized_versions"]:
                    self.ansys_ecosystem[product_name][
                        "alert_message"
                    ] += f" {authorized_version}"
                alert_message += "."
                alert_color = "danger"
                self.ansys_ecosystem_ready = False
            else:
                self.ansys_ecosystem[product_name]["selected_version"] = self.ansys_ecosystem[product_name][
                    "compatible_versions"
                ][
                    -1
                ]  # Latest
                alert_message = f"{product_name.title()} install detected. Compatible versions are:"
                for compatible_version in self.ansys_ecosystem[product_name]["compatible_versions"]:
                    alert_message += f" {compatible_version}"
                alert_message += ".\n"
                alert_message += "Selected version is %s." % (self.ansys_ecosystem[product_name]["selected_version"])
                alert_color = "success"
            self.ansys_ecosystem[product_name]["alert_message"] = alert_message
            self.ansys_ecosystem[product_name]["alert_color"] = alert_color

    @transaction(
        self=StepSpec(
            download=[
                "project_file",
            ],
            upload=[
                "project_tree",
                "treeview_items"
            ],
        )
    )
    @long_running
    def get_project_tree(self) -> None:
        """Get the project tree of the optiSLang project."""
        # Start optiSLang instance.
        osl = Optislang(
            project_path=self.project_file.path,
            reset=True,
            shutdown_on_finished=True,
            ini_timeout=300,
        )

        # Get project tree
        self.project_tree = osl.project._get_project_tree()

        # Update treeview items
        self.treeview_items = get_treeview_items_from_project_tree(self.project_tree)

    @transaction(
        self=StepSpec(
            download=[
                "input_files",
                "project_file",
                "working_properties_file",
                "optislang_log_level"
            ],
            upload=[
                "osl_server_host",
                "osl_server_port",
            ],
        )
    )
    @create_instance("osl", OptislangManager)
    def start(self, osl: OptislangManager) -> None:
        """Start optiSLang and run the project."""
        # Start optiSLang instance.
        osl.initialize(
            project_path=self.project_file.path,
            project_properties_file=self.working_properties_file.path
        )
        # Get server host
        self.osl_server_host = osl.instance.get_osl_server().get_host()
        # Get server port
        server_info = osl.instance.get_osl_server().get_server_info()
        self.osl_server_port = server_info["server"]["server_port"]
        # Start optiSLang project
        osl.instance.start(wait_for_started=True, wait_for_finished=False)
