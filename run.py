

try:
    import plugin_pb2
    import plugin_pb2_grpc
except ModuleNotFoundError:
    print("Please run setup.py before calling this script")
    quit()

