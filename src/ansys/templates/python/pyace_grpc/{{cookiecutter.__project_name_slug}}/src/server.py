{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
from concurrent import futures

import grpc

from observability.logger import Logger
from services.pinger import Pinger
import stubs.pingserver_pb2_grpc


def serve():
    """Serve function."""
    logger = Logger.init(__name__)
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stubs.pingserver_pb2_grpc.add_PingerServicer_to_server(Pinger(), server)
    logger.info(f"Server starting and listening on {port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
