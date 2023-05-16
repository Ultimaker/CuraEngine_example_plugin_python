from grpc_tools import protoc

if __name__ == "__main__":
    """Run protoc with the gRPC plugin to generate messages and gRPC stubs."""
    protoc.main(("", "-I.", "--python_out=.", "--grpc_python_out=.", "plugin.proto"))
