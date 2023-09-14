# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import sys

from pathlib import Path
from typing import List

from ansys.saf.glow.desktop.orchestration.pim_configurations import PimProductConfigurationBuilder
from ansys.saf.glow.desktop.orchestration.pim_process import PimProductConfiguration


class OptislangConfigBuilder(PimProductConfigurationBuilder):
    def get_configurations(self) -> List[PimProductConfiguration]:
        uvicorn_exe = Path(sys.executable).parent / "uvicorn"
        return [
            PimProductConfiguration(
                "optislang",
                str(uvicorn_exe),
                arguments=["ansys.solutions.{{ cookiecutter.__solution_name_slug }}.pim_configurations.osl_wrapper:app", "--port", "${AENEID_PORT_HTTP}"],
                service_name="http",
                service_type="http",
            )
        ]
