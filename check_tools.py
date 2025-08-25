"""Utility script to test MCP tool discovery by generating a tools/list JSON-RPC request."""
import json


def main():
    """Generate a JSON-RPC request to list available MCP tools."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }

    print(json.dumps(request))


if __name__ == "__main__":
    main()
