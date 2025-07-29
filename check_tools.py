import json
import sys

def main():
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    print(json.dumps(request))

if __name__ == "__main__":
    main() 