# Utilities for pyaws


def printjson(jsondata):
    import json

    try:
        jsondata = json.loads(jsondata)
    except json.decoder.JSONDecodeError:
        pass
    except TypeError:
        pass

    try:
        output = json.dumps(jsondata, indent=4, sort_keys=True)
    except TypeError:
        output = jsondata

    print(output)
