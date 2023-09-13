# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import httpx

from ansys.optislang.core import Optislang
from pathlib import Path
from typing import Optional, Union

from ansys.saf.glow.core.instance_manager import AbstractInstanceIdentificationClient
from ansys.saf.glow.solution import FileReference
from ansys.saf.glow.solution import InstanceManager
from ansys.saf.glow.storage.base import AbstractStoragePath


PRODUCT_NAME = "optislang"
SERVICE_NAME = "http"


class OptislangManager(InstanceManager[Optislang]):
    def __init__(
        self,
        instance_identification: AbstractInstanceIdentificationClient,
        method_directory: Optional[AbstractStoragePath] = None,
    ):
        super().__init__(instance_identification, method_directory)

    def initialize(
        self,
        version: Optional[str] = None,
        project_path: Optional[Union[FileReference, str]] = None,
        project_properties_file: Optional[Union[FileReference, str]] = None
    ):
        """Initialize and start the optiSLang server."""
        self.initialize_service(SERVICE_NAME, version)

        if project_path:
            self._upload_file(
                project_path,
                str(Path(self.protected_instance_state_directory_name) / "project.opf"),
                protected=False
            )

        response = httpx.post(
            f"{self._service.uri}/start",
            json={
                "project_path": project_path,
                "project_properties_file": project_properties_file
            },
            timeout=300
        ).json()

    @classmethod
    def get_product_name_implement(cls) -> str:
        """Return the name of the product in the PIM environment."""
        return PRODUCT_NAME

    def implement_get_client_object(self, hostname: str, port: int) -> Optislang:
        """Return an instance of the custom product's client given the host and port of the shared product instance."""
        response = httpx.get(f"http://{hostname}:{port}").json()
        return Optislang(host=hostname, port=response["port"], shutdown_on_finished=False)

    def _get_project_file_path(self, protected_state_directory_path: str) -> str:
        return str(Path(protected_state_directory_path) / "project.opf")

    def save_state_implement(self, protected_state_directory_path: str) -> None:
        """Save the state of the product instance to the given directory."""
        pass

    def load_state_implement(self, protected_state_directory_path: str) -> None:
        """Loads the state of the product instance from the given directory."""
        pass

    def shutdown_implement(self, protected_state_directory_path: str) -> None:
        """Gracefully terminates the product instance process."""
        self.save_state_implement(protected_state_directory_path)
        self.shutdown()
