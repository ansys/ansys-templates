{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}
import pytest


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from src.stubs.pingserver_pb2_grpc import add_PingerServicer_to_server

    return add_PingerServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from src.services.pinger import Pinger

    return Pinger()


@pytest.fixture(scope="module")
def grpc_stub_cls(grpc_channel):
    from src.stubs.pingserver_pb2_grpc import PingerStub

    return PingerStub
