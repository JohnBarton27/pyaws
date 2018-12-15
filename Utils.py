# Utilities for pyaws


def printjson(jsondata):
    import json

    print(json.dumps(jsondata, indent=4, sort_keys=True))
