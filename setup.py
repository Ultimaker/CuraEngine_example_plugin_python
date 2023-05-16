from grpc_tools import protoc
import os

if __name__ == "__main__":
    if not os.path.exists("autogen"):
        os.mkdir("autogen")
    """Run protoc with the gRPC plugin to generate messages and gRPC stubs."""
    protoc.main(("",
                 "-I.",
                 "--python_out=./autogen",
                 "--grpc_python_out=./autogen",
                 "--mypy_out=./autogen",  # Needed to generate mypy stubs
                 "plugin.proto",))
