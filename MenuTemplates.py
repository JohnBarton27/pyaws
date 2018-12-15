# Menu Templates for PyAWS
import Ec2
import Utils

inputlines = "\n" \
             "Enter your selection: "


def startmenu(menu):
    """Displays/formats a menu"""
    menustr = menu["header"] + "\n"
    for option in menu["options"]:
        menustr += "\t" + str(option) + ") " + menu["options"][option]["value"] + "\n"

    menustr += inputlines

    try:
        selection = int(input(menustr))

        if selection in menu["options"]:
            option = menu["options"][selection]
            action = option["action"]
            if "function" in action:
                params = []
                if "parameters" in action:
                    for param in action["parameters"]:
                        params.append(input(param["prompt"]))

                result = action["function"](*params)
                print()
                Utils.printjson(result)

                if "menu" in action:
                    if action["menu"] == "self":
                        startmenu(menu)
                    elif action["menu"] == "main":
                        startmenu(mainmenu)
                    else:
                        startmenu(action["menu"])
            elif "menu" in action:
                if action["menu"] == "self":
                    startmenu(menu)
                elif action["menu"] == "main":
                    startmenu(mainmenu)
                else:
                    startmenu(action["menu"])
        else:
            print("\nInvalid option! Try again.")
            startmenu(menu)

    except ValueError:
        print("\nInvalid option! Try again. (ValueError)")
        startmenu(menu)


returnToMain = {
    "value": "Return to main menu",
    "action": {
        "menu": "main"
    }
}

indec2menu = {
    "header": "\n==== Individual EC2 ====",
    "options": {
        1: {
            "value": "Get the status of an EC2 instance",
            "action": {
                "function": Ec2.getinstancestatusbyname,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ],
                "menu": "self"
            }
        },
        2: {
            "value": "Start an EC2 instance",
            "action": {
                "function": Ec2.startinstancebyname,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ]
            },
            "menu": "self"
        },
        3: {
            "value": "Stop an EC2 instance",
            "action": {
                "function": Ec2.stopinstancebyname,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ]
            },
            "menu": "self"
        },
        4: returnToMain
    }
}

ec2menu = {
    "header": "\n==== EC2 ====",
    "options": {
        1: {
            "value": "Get the names of all EC2 instances",
            "action": {
                "function": Ec2.getallinstancenames,
                "menu": "self"
            }
        },
        2: {
            "value": "Get the status of all EC2 instances",
            "action": {
                "function": Ec2.getallinstancestatuses,
                "menu": "self"
            }
        },
        3: {
            "value": "Individual EC2 instance operations",
            "action": {
                "menu": indec2menu
            }
        },
        4: returnToMain
    }
}


mainmenu = {
    "header": "\n==== PyAWS ====\nWelcome to PyAWS! What service would you like to use?",
    "options": {
        1: {
            "value": "EC2",
            "action": {
                "menu": ec2menu
            }
        },
        2: {
            "value": "Quit PyAWS",
            "action": {
                "function": exit
            }
        }
    }
}

