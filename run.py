from concurrent import futures
import grpc

try:
    import plugin_pb2
    import plugin_pb2_grpc
except ModuleNotFoundError:
    print("Please run setup.py before calling this script")
    quit()


class PluginServicer(plugin_pb2_grpc.PluginServicer):
    def Identify(self, request, context):
        print("Identify was called", request, context)



def serve() -> None:
    # The plugin should only ever talk to a single instance, so we only need one worker.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    plugin_pb2_grpc.add_PluginServicer_to_server(PluginServicer(), server)

    server.add_insecure_port("[::]:50010")
    server.start()

    # Wait until someone called us!
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
