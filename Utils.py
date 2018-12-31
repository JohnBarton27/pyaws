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


def createdashcol(title, data, leftborder=False):
    """Create a data for the dashboard"""
    rows = []
    maxdatalen = len(max(data, key=len))
    maxdatalen = max(maxdatalen, len(title))

    # Header
    rows.append(pad(title, maxdatalen, leftborder=leftborder))

    # Header line
    rows.append(pad("", maxdatalen, padchar="-", leftborder=leftborder))

    # Data
    for dataval in data:
        rows.append(pad(dataval, maxdatalen, leftborder=leftborder))

    return rows


def pad(content, maxlength, padchar=" ", leftborder=False):
    """Pad a cell for dashboard display"""
    if leftborder:
        data = "|"
    else:
        data = ""
    data += content
    spacesneeded = maxlength - len(content)
    for x in range(0, spacesneeded):
        data += padchar
    return data + "|"
