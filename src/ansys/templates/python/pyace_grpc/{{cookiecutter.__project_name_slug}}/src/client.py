{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
from __future__ import print_function

import logging
import os
from pathlib import Path
import sys

import grpc

sys.path.insert(0, os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, "stubs"))

import stubs.pingserver_pb2 as pb2
import stubs.pingserver_pb2_grpc as pb2_grpc


def run():
    """Run client."""
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.PingerStub(channel)
        response = stub.WhoPing(pb2.UserRequest(name="you"))
    print(response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
