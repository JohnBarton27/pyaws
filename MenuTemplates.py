# Menu Templates for PyAWS

inputlines = "\n" \
             "Enter your selection: "

mainmenu = {
    "header": "Welcome to PyAWS! What service would you like to use?",
    "options": [
        {
            "key": 1,
            "value": "EC2"
        }
    ]
}

ec2menu = {
    "header": "==== EC2 ====",
    "options": [
        {
            "key": 1,
            "value": "Get the names of all EC2 instances"
        }
    ]
}


def getmenu(menu):
    """Displays/formats a menu"""
    menustr = menu["header"] + "\n"
    for option in menu["options"]:
        menustr += "\t" + str(option["key"]) + ") " + option["value"] + "\n"

    menustr += inputlines

    return menustr
