# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Backend of the problem setup step."""

from pathlib import Path

from ansys.saf.glow.solution import StepModel, StepSpec, transaction, FileReference
from ansys.solutions.optislang.parser.placeholder import ProjectProperties

class ProblemSetupStep(StepModel):
    """Step definition of the first step."""

    placeholder_values = {}
    placeholder_definitions = {}

    # File storage
    project_file: FileReference = FileReference("Problem_Setup/hook_optimization.opf") # WARNING! Must be defined for specific use case
    properties_file: FileReference = FileReference("Problem_Setup/hook_optimization.json") # WARNING! Must be defined for specific use case

    
    @transaction(self=StepSpec(download=["properties_file"], upload=["placeholder_values", "placeholder_definitions"]))
    def get_default_placeholder_values(self):
        """Get placeholder values and definitions using the ProjectProperties class."""

        pp = ProjectProperties()
        pp.read_file(self.properties_file.path)
        placeholders = pp.get_properties()['placeholders']
        self.placeholder_values = placeholders.get('placeholder_values')
        self.placeholder_definitions = placeholders.get('placeholder_definitions')
        

    @transaction(self=StepSpec(upload=["project_file"]))
    def upload_project_file_to_project_directory(self) -> None:
        """Upload OptiSLang project file to project directory."""

        original_project_file = (
            Path(__file__).parent.absolute().parent / "model" / "assets" / "hook_optimization.opf"  # WARNING! Must be defined for specific use case
        )
        self.project_file.write_bytes(original_project_file.read_bytes())
    
    @transaction(self=StepSpec(upload=["properties_file"]))
    def upload_properties_file_to_project_directory(self) -> None:
        """Upload OptiSLang properties to project directory."""

        original_properties_file = (
            Path(__file__).parent.absolute().parent / "model" / "assets" / "hook_optimization.json" # WARNING! Must be defined for specific use case
        )
        self.properties_file.write_bytes(original_properties_file.read_bytes())