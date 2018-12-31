# Menu Templates for PyAWS
import Ec2
import Rds
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

                if result:
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
                "function": Ec2.getinstancestatebyname,
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
                ],
                "menu": "self"
            },
        },
        3: {
            "value": "Stop an EC2 instance",
            "action": {
                "function": Ec2.stopinstancebyname,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ],
                "menu": "self"
            },
        },
        4: returnToMain
    }
}

elasticipmenu = {
    "header": "\n==== ElastiC IP ====",
    "options": {
        1: {
            "value": "Refresh dashboard",
            "action": {
                "function": Ec2.displayelasticdashboard,
                "menu": "self"
            }
        },
        2: {
            "value": "Create new Elastic IP Address",
            "action": {
                "function": Ec2.createip,
                "menu": "self"
            }
        },
        3: {
            "value": "Release an Elastic IP Address",
            "action": {
                "function": Ec2.releaseip,
                "parameters": [
                    {"prompt": "Public IP Address to release: "}
                ],
                "menu": "self"
            }
        },
        4: {
            "value": "Associate an Elastic IP Address",
            "action": {
                "function": Ec2.associateip,
                "parameters": [
                    {"prompt": "Public IP Address to associate: "},
                    {"prompt": "Instance to associate with: "}
                ],
                "menu": "self"
            }
        },
        5: returnToMain
    }
}

ec2menu = {
    "header": "\n==== EC2 ====",
    "options": {
        1: {
            "value": "Refresh dashboard",
            "action": {
                "function": Ec2.displaydashboard,
                "menu": "self"
            }
        },
        2: {
            "value": "Individual EC2 instance operations",
            "action": {
                "menu": indec2menu
            }
        },
        3: {
            "value": "Elastic IP operations",
            "action": {
                "function": Ec2.displayelasticdashboard,
                "menu": elasticipmenu
            }
        },
        4: returnToMain
    }
}

rdsmenu = {
    "header": "\n==== RDS ====",
    "options": {
        1: {
            "value": "Refresh dashboard",
            "action": {
                "function": Rds.displaydashboard,
                "menu": "self"
            }
        },
        2: {
            "value": "Start an RDS instance",
            "action": {
                "function": Rds.startdb,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ],
                "menu": "self"
            },
        },
        3: {
            "value": "Stop an RDS instance",
            "action": {
                "function": Rds.stopdb,
                "parameters": [
                    {"prompt": "Instance Name: "}
                ],
                "menu": "self"
            },
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
                "function": Ec2.displaydashboard,
                "menu": ec2menu
            }
        },
        2: {
            "value": "RDS",
            "action": {
                "function": Rds.displaydashboard,
                "menu": rdsmenu
            }
        },
        3: {
            "value": "Quit PyAWS",
            "action": {
                "function": exit
            }
        }
    }
}

