from concurrent import futures
import grpc

try:
    import plugin_pb2
    import plugin_pb2_grpc
except ModuleNotFoundError:
    print("Please run setup.py before calling this script")
    quit()


class PluginServicer(plugin_pb2_grpc.PluginServicer):
    def Identify(self, request: plugin_pb2.PluginRequest, context) -> plugin_pb2.PluginResponse:
        print(f"Identify was called with [{request}]")
        response = plugin_pb2.PluginResponse(plugin_hash = "ExamplePythonPlugin", version = "0.0.1")
        return response


class SimplifyServicer(plugin_pb2_grpc.SimplifyServicer):
    def Simplify(self, request: plugin_pb2.SimplifyRequest, context) -> plugin_pb2.SimplifyResponse:
        print(f"Simplify was called with [{request}]")
        # Since this is just an example, we just return the polygon we received without modifying it
        return plugin_pb2.SimplifyResponse(polygons = request.polygons)


def serve() -> None:
    # The plugin should only ever talk to a single instance, so we only need one worker.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    plugin_pb2_grpc.add_PluginServicer_to_server(PluginServicer(), server)
    plugin_pb2_grpc.add_SimplifyServicer_to_server(SimplifyServicer(), server)

    # Connect on local host with port 500010
    server.add_insecure_port("[::]:50010")
    server.start()

    # Wait until plugin is closed.
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
