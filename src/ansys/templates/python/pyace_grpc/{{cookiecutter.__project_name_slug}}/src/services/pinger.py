{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

"""
{{ cookiecutter.project_name }}.

{{ cookiecutter.library_name }}
"""
import pingserver_pb2
import pingserver_pb2_grpc

NumberPing = 0


class Pinger(pingserver_pb2_grpc.PingerServicer):
    """Pinger class."""

    def PingServer(self, request, context):
        """Ping the server."""
        global NumberPing
        NumberPing += 1
        return pingserver_pb2.PingReply(
            message=f"Hello, the server is healthy and it had been pinged {NumberPing} times!"
        )

    def WhoPing(self, request, context):
        """Check who ping the server."""
        global NumberPing
        NumberPing += 1
        return pingserver_pb2.PingReply(message=f"Hello, the server is pinged by {request.name}!")
