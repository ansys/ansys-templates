# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from typing import Optional, Union

from ansys.optislang.core import Optislang
from ansys.saf.glow.core.instance_manager import AbstractInstanceIdentificationClient
from ansys.saf.glow.solution import FileReference, InstanceManager
from ansys.saf.glow.storage.base import AbstractStoragePath
import httpx

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
        project_properties_file: Optional[Union[FileReference, str]] = None,
        osl_version: Optional[int] = None,
        loglevel: Optional[str] = None,
    ):
        """Initialize and start the optiSLang server."""
        self.initialize_service(SERVICE_NAME, version)

        response = httpx.post(
            f"{self._service.uri}/start",
            json={
                "project_path": project_path,
                "project_properties_file": project_properties_file,
                "osl_version": osl_version,
                "loglevel": loglevel
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
        return Optislang(host=hostname, port=response["port"])

    def _get_project_file_path(self, protected_state_directory_path: str) -> str:
        pass

    def save_state_implement(self, protected_state_directory_path: str) -> None:
        """Save the state of the product instance to the given directory."""
        pass

    def load_state_implement(self, protected_state_directory_path: str) -> None:
        """Loads the state of the product instance from the given directory."""
        pass

    def shutdown_implement(self, protected_state_directory_path: str) -> None:
        """Gracefully terminates the product instance process."""
        self.instance.shutdown()
        self.instance.dispose()
