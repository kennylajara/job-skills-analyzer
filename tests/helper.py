import json


def mock_api(filename):
    with open (f"tests/data/{filename}.json", "r") as f:
        data = json.loads(f.read())
    
    return 200, data