{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
from stubs.pingserver_pb2 import PingReply
from stubs.pingserver_pb2_grpc import PingerServicer

NumberPing = 0


class Pinger(PingerServicer):
    """Pinger class."""

    def PingServer(self, request, context):
        """Ping the server."""
        global NumberPing
        NumberPing += 1
        return PingReply(
            message=f"Hello, the server is healthy and it had been pinged {NumberPing} times!"
        )

    def WhoPing(self, request, context):
        """Check who ping the server."""
        global NumberPing
        NumberPing += 1
        return PingReply(message=f"Hello, the server is pinged by {request.name}!")
