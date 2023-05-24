from concurrent import futures
import grpc

from CuraEngineGRPC.cura.plugins.slots.simplify.v0 import simplify_pb2_grpc
from CuraEngineGRPC.cura.plugins.slots.simplify.v0 import simplify_pb2

import simplify

metadata = (('cura-slot-version', '0.1.0-alpha.1'),  # REQUIRED
            ('cura-plugin-name', 'Python Simplify'),  # Optional but recommend
            ('cura-plugin-version', '0.1.0-alpha.1'))  # Optional but recommend


class SimplifyServicer(simplify_pb2_grpc.SimplifyServiceServicer):
    def Modify(self, request: simplify_pb2.SimplifyServiceModifyRequest, context) -> simplify_pb2.SimplifyServiceModifyResponse:
        context.send_initial_metadata(metadata)
        return simplify_pb2.SimplifyServiceModifyResponse(polygons = simplify.simplify(request.polygons))


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 1))
    simplify_pb2_grpc.add_SimplifyServiceServicer_to_server(SimplifyServicer(), server)
    server.add_insecure_port("localhost:33700")
    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
