# Copyright (c) 2022, My Company. Unauthorised use, distribution or duplication is prohibited

from fastapi.testclient import TestClient

from src._version import __version__
from src.server import app


class TestServer:
    def setup_class(self):
        self.client = TestClient(app)

    def test_get_version(self):
        response = self.client.get("/version")
        assert response.status_code == 200
        assert response.json() == {"version": __version__}

    def test_get_health_status(self):
        response = self.client.get("/health")
        assert response.status_code == 200
