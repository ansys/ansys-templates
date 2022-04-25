{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}
import pytest

from src.stubs.pingserver_pb2 import EmptyRequest, UserRequest


@pytest.mark.smoke
class TestServer:
    def test_first_ping(self, grpc_stub):
        request = EmptyRequest()
        response = grpc_stub.PingServer(request)
        assert response.message == "Hello, the server is healthy and it had been pinged 1 times!"

    def test_who_ping(self, grpc_stub):
        request = UserRequest(name="you")
        response = grpc_stub.WhoPing(request)
        assert response.message == f"Hello, the server is pinged by {request.name}!"

    def test_third_ping(self, grpc_stub):
        request = EmptyRequest()
        response = grpc_stub.PingServer(request)
        assert response.message == "Hello, the server is healthy and it had been pinged 3 times!"
