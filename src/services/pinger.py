# Copyright (c) 2022, My Company. Unauthorised use, distribution or duplication is prohibited


"""
my_company.

library
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
